export const STATUS_PEDIDO = {
  Pendente: {
    classe: 'selo-pendente',
    proximo: 'Em preparo',
    acaoAvancar: 'Iniciar preparo',
    podeCancelar: true,
  },
  'Em preparo': {
    classe: 'selo-preparo',
    proximo: 'Pronto para retirada',
    acaoAvancar: 'Marcar como pronto',
    podeCancelar: true,
  },
  'Pronto para retirada': {
    classe: 'selo-pronto',
    proximo: 'Entregue',
    acaoAvancar: 'Confirmar entrega',
    podeCancelar: false,
  },
  Entregue: { classe: 'selo-entregue', proximo: null, podeCancelar: false },
  Cancelado: { classe: 'selo-cancelado', proximo: null, podeCancelar: false },
}

export const ORDEM_STATUS = Object.keys(STATUS_PEDIDO)

// Colunas do quadro do produtor; cancelados ficam numa seção à parte
export const STATUS_KANBAN = ['Pendente', 'Em preparo', 'Pronto para retirada', 'Entregue']

export const STATUS_EM_ANDAMENTO = ['Em preparo', 'Pronto para retirada']

export function infoStatus(status) {
  return STATUS_PEDIDO[status] || { classe: 'selo-neutro', proximo: null, podeCancelar: false }
}

export function ordenarPorMaisRecente(pedidos) {
  return [...pedidos].sort((a, b) => {
    const diferenca = new Date(b.data_criacao || 0) - new Date(a.data_criacao || 0)
    return diferenca || b.pedido_id - a.pedido_id
  })
}
