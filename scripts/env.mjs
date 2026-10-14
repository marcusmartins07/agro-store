import { existsSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ENV_PATH = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '.env')

// Carrega o .env da raiz; variáveis já definidas no terminal têm prioridade.
export function carregarEnv() {
  if (existsSync(ENV_PATH)) process.loadEnvFile(ENV_PATH)
}
