export const API_BASE_URL = (import.meta.env.VITE_API_URL || '/api/v1').replace(/\/$/, '')
export const BACKEND_URL = (import.meta.env.VITE_BACKEND_URL || '').replace(/\/$/, '')

// ── Refresh do token ─────────────────────────────────────────────────────────
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

// ── GET com retry automático no 401 ──────────────────────────────────────────
async function request(endpoint) {
  const fazerRequisicao = async (token) => {
    const headers = { 'Content-Type': 'application/json' }
    if (token) headers['Authorization'] = `Bearer ${token}`
    return fetch(`${API_BASE_URL}${endpoint}`, { headers })
  }

  let token = localStorage.getItem('access_token')
  let response = await fazerRequisicao(token)

  if (response.status === 401) {
    token = await refreshAccessToken()
    response = await fazerRequisicao(token)
  }

  if (!response.ok) throw new Error(`Erro na API: ${response.status} ${response.statusText}`)
  return response.json()
}

// ── POST ─────────────────────────────────────────────────────────────────────
async function post(endpoint, body) {
  const token = localStorage.getItem('access_token')
  const headers = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  })

  if (!response.ok) {
    const erro = await response.json().catch(() => ({}))
    throw { status: response.status, data: erro }
  }
  return response.json()
}

// ── PATCH ────────────────────────────────────────────────────────────────────
async function patch(endpoint, body) {
  const token = localStorage.getItem('access_token')
  const headers = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'PATCH',
    headers,
    body: JSON.stringify(body),
  })

  if (!response.ok) {
    const erro = await response.json().catch(() => ({}))
    throw { status: response.status, data: erro }
  }
  return response.json()
}

// ── POST multipart (para upload de imagem) ────────────────────────────────────
async function postForm(endpoint, formData) {
  const token = localStorage.getItem('access_token')
  const headers = {}
  if (token) headers['Authorization'] = `Bearer ${token}`

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'POST',
    headers,
    body: formData,
  })

  if (!response.ok) {
    const erro = await response.json().catch(() => ({}))
    throw { status: response.status, data: erro }
  }
  return response.json()
}

// ── Endpoints ─────────────────────────────────────────────────────────────────
export const api = {
  produtos: {
    listar: () => request('/produtos/'),
  },
  categorias: {
    listar: () => request('/produtos/categorias/?ativo=true'),
  },
  auth: {
    login:   (cpf, password) => post('/usuarios/login/', { cpf, password }),
    refresh: (refresh)       => post('/usuarios/token/refresh/', { refresh }),
  },
  usuarios: {
    me:              ()           => request('/usuarios/me'),
    tornarProdutor:  (id)         => patch(`/usuarios/usuarios/${id}/`, { is_produtor: true }),
  },
  lojas: {
    criar: (body) => post('/lojas/lojas/', body),
    me:    ()     => request('/lojas/me/'),
  },
}
