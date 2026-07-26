import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/services/api.js'

export const useAuthStore = defineStore('auth', () => {
  // Recupera tokens salvos ao recarregar a página
  const accessToken  = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)
  const usuario      = ref(JSON.parse(localStorage.getItem('usuario') || 'null'))

  const estaLogado = computed(() => !!accessToken.value)

  async function login(cpf, password) {
    const dados = await api.auth.login(cpf, password)

    accessToken.value  = dados.access
    refreshToken.value = dados.refresh

    localStorage.setItem('access_token',  dados.access)
    localStorage.setItem('refresh_token', dados.refresh)
  }

  function logout() {
    accessToken.value  = null
    refreshToken.value = null
    usuario.value      = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('usuario')
  }

  return { accessToken, refreshToken, usuario, estaLogado, login, logout }
})