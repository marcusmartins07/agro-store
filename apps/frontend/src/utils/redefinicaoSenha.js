// Erros gerais das telas de redefinição de senha (RN-020) que não pertencem a um campo
export const MENSAGEM_ERRO_CONEXAO = 'Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente.'
export const MENSAGEM_LIMITE = 'Muitas solicitações. Tente novamente mais tarde.'
const MENSAGEM_ERRO_INESPERADO = 'Não foi possível concluir a solicitação. Tente novamente.'

// Recebe o erro lançado pelo service ({ status, data }) ou a falha de rede do fetch (sem status)
export function erroGeralRedefinicao(erro) {
  if (!erro?.status) return { tipo: 'danger', mensagem: MENSAGEM_ERRO_CONEXAO }
  if (erro.status === 429) return { tipo: 'warning', mensagem: erro.data?.detail || MENSAGEM_LIMITE }
  return { tipo: 'danger', mensagem: erro.data?.detail || MENSAGEM_ERRO_INESPERADO }
}
