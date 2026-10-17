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

// autenticar: false não envia o JWT (endpoints públicos que não devem depender da sessão salva)
async function request(endpoint, options = {}, retry = true, { autenticar = true } = {}) {
  const token = autenticar ? localStorage.getItem('access_token') : null
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

// Monta o multipart com um arquivo e, opcionalmente, campos de texto (valores vazios não são enviados)
function comArquivo(campo, arquivo, campos = {}) {
  const formData = new FormData()
  for (const [chave, valor] of Object.entries(campos)) {
    if (valor !== undefined && valor !== null && valor !== '') formData.append(chave, valor)
  }
  formData.append(campo, arquivo)
  return formData
}

export const api = {
  produtos: {
    listar: () => request('/produtos/'),
    obter: (produtoId) => request(`/produtos/${produtoId}/`),
    listarMeus: () => request('/produtos/meus/'),
    criar: (body) => request('/produtos/', { method: 'POST', body: jsonBody(body) }),
    atualizar: (produtoId, body) => request(`/produtos/${produtoId}/`, { method: 'PATCH', body: jsonBody(body) }),
    enviarImagem: (produtoId, arquivo, ePrincipal = false) => {
      const formData = new FormData()
      formData.append('imagem', arquivo)
      if (ePrincipal) formData.append('e_principal', 'true')
      return request(`/produtos/${produtoId}/imagens/`, { method: 'POST', body: formData })
    },
    definirImagemPrincipal: (produtoId, imagemId) => request(`/produtos/${produtoId}/imagens/${imagemId}/`, {
      method: 'PATCH',
      body: jsonBody({ e_principal: true }),
    }),
    removerImagem: (produtoId, imagemId) => request(`/produtos/${produtoId}/imagens/${imagemId}/`, { method: 'DELETE' }),
    reordenarImagens: (produtoId, imagemIds) => request(`/produtos/${produtoId}/imagens/reordenar/`, {
      method: 'POST',
      body: jsonBody({ imagens: imagemIds }),
    }),
    criarPreco: (body) => request('/produtos/precos/', { method: 'POST', body: jsonBody(body) }),
  },
  categorias: {
    listar: () => request('/produtos/categorias/?ativo=true'),
  },
  auth: {
    login: (cpf, password) => request('/usuarios/login/', { method: 'POST', body: jsonBody({ cpf, password }) }, false),
    cadastrar: (body) => request('/usuarios/cadastro/', { method: 'POST', body: jsonBody(body) }, false),
    refresh: (refresh) => request('/usuarios/token/refresh/', { method: 'POST', body: jsonBody({ refresh }) }, false),
    solicitarRedefinicaoSenha: (email) => request('/usuarios/redefinir-senha/', {
      method: 'POST',
      body: jsonBody({ email }),
    }, false, { autenticar: false }),
    confirmarRedefinicaoSenha: ({ token, password, password_confirmacao }) => request('/usuarios/redefinir-senha/confirmar/', {
      method: 'POST',
      body: jsonBody({ token, password, password_confirmacao }),
    }, false, { autenticar: false }),
  },
  usuarios: {
    me: () => request('/usuarios/me/'),
    atualizar: (body) => request('/usuarios/me/', { method: 'PATCH', body: jsonBody(body) }),
    // Remoção da foto só pelo DELETE: enviar valor vazio no PATCH é recusado (RN-018)
    atualizarFoto: (arquivo) => request('/usuarios/me/', { method: 'PATCH', body: comArquivo('foto_perfil', arquivo) }),
    removerFoto: () => request('/usuarios/me/foto/', { method: 'DELETE' }),
  },
  // Pública (RN-021): usada no cadastro, feito sem login
  tiposTelefone: {
    listar: () => request('/tipos-telefone/', {}, false, { autenticar: false }),
  },
  telefones: {
    listar: () => request('/usuarios/me/telefones/'),
    criar: (body) => request('/usuarios/me/telefones/', { method: 'POST', body: jsonBody(body) }),
    atualizar: (telefoneId, body) => request(`/usuarios/me/telefones/${telefoneId}/`, { method: 'PATCH', body: jsonBody(body) }),
    excluir: (telefoneId) => request(`/usuarios/me/telefones/${telefoneId}/`, { method: 'DELETE' }),
  },
  lojas: {
    // Com imagem, a criação vai em multipart (o navegador define o Content-Type); sem imagem, continua em JSON
    criar: (body, imagem = null) => request('/lojas/lojas/', {
      method: 'POST',
      body: imagem ? comArquivo('imagem_perfil', imagem, body) : jsonBody(body),
    }),
    // Pública: sem JWT, para nunca disparar refresh nem redirecionar ao login a partir do detalhe do produto
    obter: (lojaId) => request(`/lojas/lojas/${lojaId}/`, {}, false, { autenticar: false }),
    me: () => request('/lojas/me/'),
    atualizarMinha: (body) => request('/lojas/me/', { method: 'PATCH', body: jsonBody(body) }),
    atualizarImagem: (arquivo) => request('/lojas/me/', { method: 'PATCH', body: comArquivo('imagem_perfil', arquivo) }),
    removerImagem: () => request('/lojas/me/imagem/', { method: 'DELETE' }),
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
  avaliacoes: {
    listarPorProduto: (produtoId) => request(`/avaliacoes/?produto=${encodeURIComponent(produtoId)}`),
    criar: (body) => request('/avaliacoes/', { method: 'POST', body: jsonBody(body) }),
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
    cancelar: (pedidoId) => request(`/pedidos/${pedidoId}/cancelar/`, { method: 'PATCH' }),
  },
}
