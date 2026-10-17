export function formatarPreco(valor) {
  if (valor === null || valor === undefined || valor === '') return 'Preço indisponível'
  return Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

export function temDesconto(produto) {
  return Number(produto?.desconto) > 0
}

export function somenteDigitos(valor) {
  return String(valor ?? '').replace(/\D/g, '')
}

export function mascaraCpf(valor) {
  return somenteDigitos(valor)
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d{1,2})$/, '$1-$2')
    .slice(0, 14)
}

// Máscara pela quantidade de dígitos (máx. 11): até 10 vira (XX) XXXX-XXXX e 11 vira (XX) XXXXX-XXXX, sem hífen solto
export function mascaraTelefone(valor) {
  const digitos = somenteDigitos(valor).slice(0, 11)
  if (digitos.length <= 2) return digitos
  const ddd = `(${digitos.slice(0, 2)}) `
  const numero = digitos.slice(2)
  const tamanhoPrefixo = digitos.length === 11 ? 5 : 4
  if (numero.length <= tamanhoPrefixo) return ddd + numero
  return `${ddd}${numero.slice(0, tamanhoPrefixo)}-${numero.slice(tamanhoPrefixo)}`
}

// Espelho de exibição da RN-021 (o backend continua validando): dígitos aceitos por tipo, com DDD
const FORMATOS_TELEFONE = {
  Celular: {
    digitos: [11],
    placeholder: '(00) 00000-0000',
    ajuda: 'Celular com DDD (11 dígitos).',
    erro: 'Informe um celular com DDD (11 dígitos).',
  },
  Fixo: {
    digitos: [10],
    placeholder: '(00) 0000-0000',
    ajuda: 'Telefone fixo com DDD (10 dígitos).',
    erro: 'Informe um telefone fixo com DDD (10 dígitos).',
  },
  Comercial: {
    digitos: [10, 11],
    placeholder: '(00) 00000-0000',
    ajuda: 'Telefone comercial com DDD (10 ou 11 dígitos).',
    erro: 'Informe um telefone comercial com DDD (10 ou 11 dígitos).',
  },
}

export function placeholderTelefone(tipoDescricao) {
  return FORMATOS_TELEFONE[tipoDescricao]?.placeholder || '(00) 00000-0000'
}

export function ajudaTelefone(tipoDescricao) {
  if (!tipoDescricao) return 'Escolha o tipo para ver o formato.'
  return FORMATOS_TELEFONE[tipoDescricao]?.ajuda || 'Telefone com DDD.'
}

// Retorna a mensagem de erro ou '' quando o número é aceito para o tipo
export function validarTelefonePorTipo(numero, tipoDescricao) {
  if (!tipoDescricao) return 'Selecione o tipo de telefone.'
  const digitos = somenteDigitos(numero)
  if (!digitos) return 'Informe o telefone.'
  const formato = FORMATOS_TELEFONE[tipoDescricao]
  if (formato && !formato.digitos.includes(digitos.length)) return formato.erro
  return ''
}

export function mascaraCnpj(valor) {
  return somenteDigitos(valor)
    .replace(/(\d{2})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1/$2')
    .replace(/(\d{4})(\d{1,2})$/, '$1-$2')
    .slice(0, 18)
}

export function formatarCpf(cpf) {
  return cpf ? mascaraCpf(cpf) : 'Não informado'
}

export function formatarTelefone(telefone) {
  return telefone ? mascaraTelefone(telefone) : 'Não informado'
}

// Aceita data (aaaa-mm-dd) ou data/hora ISO. Datas sem horário não passam por Date para não mudar de dia pelo fuso.
export function formatarData(valor) {
  if (!valor) return 'Não informada'
  const somenteData = /^\d{4}-\d{2}-\d{2}$/.test(valor)
  if (somenteData) return valor.split('-').reverse().join('/')
  return new Date(valor).toLocaleDateString('pt-BR')
}

export function calcularIdade(dataNascimento) {
  if (!dataNascimento) return null
  const [ano, mes, dia] = dataNascimento.split('-').map(Number)
  const hoje = new Date()
  const aniversarioPassou = hoje.getMonth() + 1 > mes || (hoje.getMonth() + 1 === mes && hoje.getDate() >= dia)
  return hoje.getFullYear() - ano - (aniversarioPassou ? 0 : 1)
}

// Iniciais exibidas quando não há imagem: duas para pessoas, uma para lojas (RN-018)
export function iniciaisDoNome(nome, quantidade = 2) {
  const iniciais = String(nome ?? '').trim().split(/\s+/).filter(Boolean)
    .slice(0, quantidade).map(parte => parte[0]).join('').toUpperCase()
  return iniciais || '?'
}
