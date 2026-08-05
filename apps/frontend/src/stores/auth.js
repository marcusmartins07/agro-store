import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/services/api.js'

export const useAuthStore = defineStore('auth', () => {
  // Recupera tokens salvos ao recarregar a página
  const accessToken  = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)
  const usuario      = ref(JSON.parse(localStorage.getItem('usuario') || 'null'))

  const estaLogado = computed(() => !!accessToken.value)

  function salvarSessao(dados) {
    accessToken.value = dados.access
    refreshToken.value = dados.refresh
    usuario.value = dados.usuario || null

    localStorage.setItem('access_token', dados.access)
    localStorage.setItem('refresh_token', dados.refresh)
    if (dados.usuario) localStorage.setItem('usuario', JSON.stringify(dados.usuario))
  }

  async function login(cpf, password) {
    const dados = await api.auth.login(cpf, password)
    salvarSessao(dados)
  }

  async function cadastrar(dadosCadastro) {
    const dados = await api.auth.cadastrar(dadosCadastro)
    salvarSessao(dados)
  }

  function logout() {
    accessToken.value  = null
    refreshToken.value = null
    usuario.value      = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('usuario')
  }

  function atualizarUsuario(dados) {
    usuario.value = dados
    localStorage.setItem('usuario', JSON.stringify(dados))
  }

  return { accessToken, refreshToken, usuario, estaLogado, login, cadastrar, logout, atualizarUsuario }
})
