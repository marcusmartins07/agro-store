export const API_BASE_URL = (import.meta.env.VITE_API_URL || '/api/v1').replace(/\/$/, '')
export const BACKEND_URL = (import.meta.env.VITE_BACKEND_URL || '').replace(/\/$/, '')

async function refreshAccessToken() {
  const refresh = localStorage.getItem('refresh_token')
  if (!refresh) throw new Error('Sem refresh token')

  const response = await fetch(`${API_BASE_URL}/usuarios/token/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  })

  if (!response.ok) {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    window.location.href = '/login'
    throw new Error('Sessão expirada')
  }

  const dados = await response.json()
  localStorage.setItem('access_token', dados.access)
  return dados.access
}

async function request(endpoint, options = {}, retry = true) {
  const token = localStorage.getItem('access_token')
  const headers = { ...(options.headers || {}) }

  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json'
  }
  if (token) headers.Authorization = `Bearer ${token}`

  let response = await fetch(`${API_BASE_URL}${endpoint}`, { ...options, headers })

  if (response.status === 401 && retry) {
    const novoToken = await refreshAccessToken()
    response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: { ...headers, Authorization: `Bearer ${novoToken}` },
    })
  }

  if (!response.ok) {
    const erro = await response.json().catch(() => ({}))
    throw { status: response.status, data: erro }
  }

  if (response.status === 204) return null
  return response.json()
}

const jsonBody = (body) => JSON.stringify(body)

export const api = {
  produtos: {
    listar: () => request('/produtos/'),
    listarMeus: () => request('/produtos/meus/'),
    criar: (body) => request('/produtos/', { method: 'POST', body: jsonBody(body) }),
    atualizar: (produtoId, body) => request(`/produtos/${produtoId}/`, { method: 'PATCH', body: jsonBody(body) }),
    criarPreco: (body) => request('/produtos/precos/', { method: 'POST', body: jsonBody(body) }),
  },
  categorias: {
    listar: () => request('/produtos/categorias/?ativo=true'),
  },
  auth: {
    login: (cpf, password) => request('/usuarios/login/', { method: 'POST', body: jsonBody({ cpf, password }) }, false),
    cadastrar: (body) => request('/usuarios/cadastro/', { method: 'POST', body: jsonBody(body) }, false),
    refresh: (refresh) => request('/usuarios/token/refresh/', { method: 'POST', body: jsonBody({ refresh }) }, false),
  },
  usuarios: {
    me: () => request('/usuarios/me'),
  },
  lojas: {
    criar: (body) => request('/lojas/lojas/', { method: 'POST', body: jsonBody(body) }),
    me: () => request('/lojas/me/'),
    atualizarMinha: (body) => request('/lojas/me/', { method: 'PATCH', body: jsonBody(body) }),
  },
  carrinhos: {
    listar: () => request('/carrinhos/'),
    adicionar: (produto, quantidade = 1) => request('/carrinhos/', {
      method: 'POST',
      body: jsonBody({ produto, quantidade }),
    }),
    atualizarItem: (itemId, quantidade) => request(`/carrinhos/itens/${itemId}/`, {
      method: 'PATCH',
      body: jsonBody({ quantidade }),
    }),
    removerItem: (itemId) => request(`/carrinhos/itens/${itemId}/`, { method: 'DELETE' }),
  },
  favoritos: {
    listar: () => request('/favoritos/'),
    adicionar: (produto) => request('/favoritos/', { method: 'POST', body: jsonBody({ produto }) }),
    remover: (favoritoId) => request(`/favoritos/${favoritoId}/`, { method: 'DELETE' }),
  },
  pedidos: {
    listar: () => request('/pedidos/'),
    finalizarCarrinho: (carrinhoProdutoIds) => request('/pedidos/', {
      method: 'POST',
      body: jsonBody({ carrinho_produto_ids: carrinhoProdutoIds }),
    }),
    listarMinhaLoja: () => request('/pedidos/minha-loja/'),
    listarStatusDisponiveis: () => request('/pedidos/status-disponiveis/'),
    atualizarStatus: (pedidoId, status) => request(`/pedidos/${pedidoId}/status/`, {
      method: 'PATCH',
      body: jsonBody({ status }),
    }),
  },
}
