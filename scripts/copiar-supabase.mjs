import { spawnSync } from 'node:child_process'
import { closeSync, existsSync, mkdirSync, openSync, readFileSync, renameSync, rmSync, statSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { parseEnv } from 'node:util'

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const ENV_PATH = path.join(RAIZ, '.env')
const PASTA_BACKUPS = path.join(RAIZ, 'backups')
const PROJETO_LOCAL = 'agro-store'
const IMAGEM_POSTGRES = 'postgres:17'
const SERVICO_BANCO = 'db'
const BANCO_LOCAL = 'agrostore'
const BANCO_TEMPORARIO = 'agrostore_restauracao'
const BANCO_MANUTENCAO = 'postgres'
const USUARIO_LOCAL = 'agrostore'
const SOCKET_LOCAL = '/var/run/postgresql'
const ROLES_SUPABASE = ['supabase_admin', 'authenticator', 'anon']

function executar(argumentos, opcoes = {}) {
  const processo = spawnSync('docker', argumentos, { cwd: RAIZ, stdio: 'inherit', ...opcoes })
  if (processo.error) throw new Error(`Não foi possível executar o Docker: ${processo.error.message}`)
  if (processo.status !== 0) throw new Error(`Falha em: docker ${argumentos[0]} ${argumentos[1] ?? ''} (código ${processo.status}).`)
  return processo
}

function capturar(argumentos) {
  const processo = executar(argumentos, { stdio: ['ignore', 'pipe', 'inherit'], encoding: 'utf8' })
  return processo.stdout.trim()
}

function compose(...argumentos) {
  return executar(['compose', ...argumentos])
}

function psqlLocal(comando, banco = BANCO_LOCAL) {
  return ['compose', 'exec', '-T', SERVICO_BANCO, 'psql', `--host=${SOCKET_LOCAL}`, `--username=${USUARIO_LOCAL}`,
    `--dbname=${banco}`, '--no-psqlrc', '--tuples-only', '--no-align', '--set=ON_ERROR_STOP=1', `--command=${comando}`]
}

function conferirConfiguracaoLocal() {
  const config = JSON.parse(capturar(['compose', 'config', '--format', 'json']))
  const ambiente = config.services?.backend?.environment ?? {}
  const urlBackend = URL.parse(ambiente.DATABASE_URL ?? '')

  if (config.name !== PROJETO_LOCAL) throw new Error('Destino recusado: o projeto Compose não é o local.')
  if (config.services?.[SERVICO_BANCO]?.image !== IMAGEM_POSTGRES) throw new Error('Destino recusado: o serviço db não usa a imagem esperada.')
  if (urlBackend?.hostname !== SERVICO_BANCO) throw new Error('Destino recusado: o backend não aponta para o serviço db.')
  if (ambiente.SUPABASE_STORAGE_BUCKET) throw new Error('Destino recusado: o backend está configurado com um bucket.')
}

function conferirBancoLocal() {
  const roles = ROLES_SUPABASE.map((role) => `'${role}'`).join(', ')
  const consulta = `select current_database() || '|' || current_user || '|' || count(*) from pg_roles where rolname in (${roles})`
  const identidade = capturar(psqlLocal(consulta))

  if (identidade !== `${BANCO_LOCAL}|${USUARIO_LOCAL}|0`) throw new Error('Destino recusado: o serviço db não é o banco local esperado.')
}

function lerConexaoOrigem() {
  if (!existsSync(ENV_PATH)) throw new Error('Arquivo .env não encontrado na raiz do projeto.')

  const origem = URL.parse(parseEnv(readFileSync(ENV_PATH, 'utf8')).DATABASE_URL ?? '')
  if (!origem || !['postgres:', 'postgresql:'].includes(origem.protocol)) {
    throw new Error('DATABASE_URL do .env precisa ser uma URL postgresql://.')
  }

  return {
    PGHOST: origem.hostname,
    PGPORT: origem.port || '5432',
    PGUSER: decodeURIComponent(origem.username),
    PGPASSWORD: decodeURIComponent(origem.password),
    PGDATABASE: decodeURIComponent(origem.pathname.slice(1)),
    PGSSLMODE: 'require',
  }
}

function gerarDump() {
  const conexao = lerConexaoOrigem()
  const carimbo = new Date().toISOString().replace(/[-:]/g, '').replace('T', '-').slice(0, 15)
  const nome = `agro-store-supabase-${carimbo}.dump`
  const parcial = `${nome}.parcial`
  const caminhoParcial = path.join(PASTA_BACKUPS, parcial)
  const destino = path.join(PASTA_BACKUPS, nome)

  mkdirSync(PASTA_BACKUPS, { recursive: true })
  console.log(`Gerando ${nome} (somente leitura)...`)
  try {
    executar([
      'run', '--rm',
      ...Object.keys(conexao).flatMap((variavel) => ['--env', variavel]),
      '--volume', `${PASTA_BACKUPS}:/backups`,
      IMAGEM_POSTGRES,
      'pg_dump', '--format=custom', '--schema=public', '--no-owner', '--no-privileges', `--file=/backups/${parcial}`,
    ], { env: { ...process.env, ...conexao } })
    renameSync(caminhoParcial, destino)
  } finally {
    rmSync(caminhoParcial, { force: true })
  }

  return destino
}

function restaurar(arquivo) {
  conferirBancoLocal()
  console.log(`Restaurando ${path.basename(arquivo)} no serviço db local...`)
  capturar(psqlLocal(`drop database if exists ${BANCO_TEMPORARIO} with (force)`, BANCO_MANUTENCAO))
  capturar(psqlLocal(`create database ${BANCO_TEMPORARIO}`, BANCO_MANUTENCAO))
  capturar(psqlLocal('set client_min_messages = warning; drop schema public cascade', BANCO_TEMPORARIO))

  const entrada = openSync(arquivo, 'r')
  try {
    executar([
      'compose', 'exec', '-T', SERVICO_BANCO, 'pg_restore', `--host=${SOCKET_LOCAL}`, `--username=${USUARIO_LOCAL}`,
      `--dbname=${BANCO_TEMPORARIO}`, '--no-owner', '--no-privileges', '--exit-on-error', '--single-transaction',
    ], { stdio: [entrada, 'inherit', 'inherit'] })
  } finally {
    closeSync(entrada)
  }

  capturar(psqlLocal(`drop database ${BANCO_LOCAL} with (force)`, BANCO_MANUTENCAO))
  capturar(psqlLocal(`alter database ${BANCO_TEMPORARIO} rename to ${BANCO_LOCAL}`, BANCO_MANUTENCAO))
}

function resolverArquivoInformado(caminho) {
  const arquivo = path.resolve(caminho)
  if (!existsSync(arquivo) || !statSync(arquivo).isFile()) throw new Error('Arquivo de dump não encontrado.')
  return arquivo
}

function main() {
  conferirConfiguracaoLocal()

  const caminhoInformado = process.argv[2]
  const arquivo = caminhoInformado ? resolverArquivoInformado(caminhoInformado) : gerarDump()

  compose('stop', 'backend', 'frontend')
  try {
    compose('up', '--detach', '--wait', SERVICO_BANCO)
    restaurar(arquivo)
    compose('run', '--rm', 'backend', 'python', 'manage.py', 'migrate', '--noinput')
  } finally {
    compose('up', '--detach', 'backend', 'frontend')
  }

  console.log(`Cópia concluída a partir de ${path.relative(RAIZ, arquivo)}.`)
}

try {
  main()
} catch (erro) {
  console.error(erro.message)
  process.exitCode = 1
}
