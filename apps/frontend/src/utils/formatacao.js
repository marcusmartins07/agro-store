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

export function mascaraTelefone(valor) {
  return somenteDigitos(valor)
    .replace(/^(\d{2})(\d)/, '($1) $2')
    .replace(/(\d{5})(\d)/, '$1-$2')
    .slice(0, 15)
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
