import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/services/api.js'

export const useTiposTelefoneStore = defineStore('tiposTelefone', () => {
  const tipos = ref([])
  const carregando = ref(false)
  const erro = ref(false)
  let requisicao = null

  async function carregar() {
    if (tipos.value.length) return tipos.value
    if (requisicao) return requisicao

    carregando.value = true
    erro.value = false
    requisicao = api.tiposTelefone.listar()
      .then(dados => {
        tipos.value = Array.isArray(dados) ? dados : []
        if (!tipos.value.length) erro.value = true
        return tipos.value
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

  function descricaoDoTipo(tipoId) {
    return tipos.value.find(tipo => tipo.id === tipoId)?.descricao || ''
  }

  function idPorDescricao(descricao) {
    return tipos.value.find(tipo => tipo.descricao === descricao)?.id ?? null
  }

  return { tipos, carregando, erro, carregar, descricaoDoTipo, idPorDescricao }
})
