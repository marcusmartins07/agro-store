import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/services/api.js'

export const useGenerosStore = defineStore('generos', () => {
  const generos = ref([])
  const carregando = ref(false)
  const erro = ref(false)
  let requisicao = null

  async function carregar() {
    if (generos.value.length) return generos.value
    if (requisicao) return requisicao

    carregando.value = true
    erro.value = false
    requisicao = api.generos.listar()
      .then(dados => {
        generos.value = Array.isArray(dados) ? dados : []
        if (!generos.value.length) erro.value = true
        return generos.value
      })
      .catch(falha => {
        console.error(falha)
        erro.value = true
        return []
      })
      .finally(() => {
        carregando.value = false
        requisicao = null
      })
    return requisicao
  }

  function nomeDoGenero(codigo) {
    return generos.value.find(genero => genero.codigo === codigo)?.nome || ''
  }

  return { generos, carregando, erro, carregar, nomeDoGenero }
})
