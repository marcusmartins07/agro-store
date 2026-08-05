import { defineStore } from 'pinia'
import { ref } from 'vue'

const TIPOS_VALIDOS = ['success', 'info', 'warning', 'danger']

export const useNotificacoesStore = defineStore('notificacoes', () => {
  const notificacoes = ref([])
  const temporizadores = new Map()
  let proximoId = 1

  function notificar({ tipo = 'info', mensagem, tempo } = {}) {
    const id = proximoId++
    const notificacao = {
      id,
      tipo: TIPOS_VALIDOS.includes(tipo) ? tipo : 'info',
      mensagem,
    }
    notificacoes.value.push(notificacao)

    if (Number.isFinite(tempo) && tempo > 0) {
      temporizadores.set(id, window.setTimeout(() => remover(id), tempo * 1000))
    }
    return id
  }

  function remover(id) {
    const temporizador = temporizadores.get(id)
    if (temporizador) window.clearTimeout(temporizador)
    temporizadores.delete(id)
    const indice = notificacoes.value.findIndex(notificacao => notificacao.id === id)
    if (indice !== -1) notificacoes.value.splice(indice, 1)
  }

  function limpar() {
    notificacoes.value.forEach(notificacao => remover(notificacao.id))
  }

  return { notificacoes, notificar, remover, limpar }
})
