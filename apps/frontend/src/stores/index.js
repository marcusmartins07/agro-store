import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// ─── CARRINHO ────────────────────────────────────────────────────────────────
export const useCarrinhoStore = defineStore('carrinho', () => {
  const itens = ref([])

  // Adiciona produto; se já existir, incrementa quantidade
  function adicionar(produto) {
    const existente = itens.value.find(i => i.id === produto.id)
    if (existente) {
      existente.quantidade++
    } else {
      itens.value.push({ ...produto, quantidade: 1 })
    }
  }

  function remover(id) {
    itens.value = itens.value.filter(i => i.id !== id)
  }

  function alterarQuantidade(id, delta) {
    const item = itens.value.find(i => i.id === id)
    if (!item) return
    item.quantidade += delta
    if (item.quantidade <= 0) remover(id)
  }

  function limpar() {
    itens.value = []
  }

  // Total geral
  const total = computed(() =>
    itens.value.reduce((acc, i) => acc + i.preco * i.quantidade, 0)
  )

  // Agrupado por fornecedor
  const porFornecedor = computed(() => {
    const grupos = {}
    for (const item of itens.value) {
      if (!grupos[item.fornecedor]) grupos[item.fornecedor] = []
      grupos[item.fornecedor].push(item)
    }
    return grupos
  })

  const totalItens = computed(() =>
    itens.value.reduce((acc, i) => acc + i.quantidade, 0)
  )

  return { itens, adicionar, remover, alterarQuantidade, limpar, total, porFornecedor, totalItens }
})

// ─── FAVORITOS ───────────────────────────────────────────────────────────────
export const useFavoritosStore = defineStore('favoritos', () => {
  const itens = ref([])

  function alternar(produto) {
    const idx = itens.value.findIndex(i => i.id === produto.id)
    if (idx >= 0) {
      itens.value.splice(idx, 1)
    } else {
      itens.value.push({ ...produto, adicionadoEm: new Date().toISOString() })
    }
  }

  function isFavorito(id) {
    return itens.value.some(i => i.id === id)
  }

  // Ordenado do mais recente para o mais antigo
  const ordenados = computed(() =>
    [...itens.value].sort((a, b) => new Date(b.adicionadoEm) - new Date(a.adicionadoEm))
  )

  return { itens, alternar, isFavorito, ordenados }
})