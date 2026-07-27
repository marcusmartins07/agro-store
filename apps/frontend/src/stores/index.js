import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { api } from '@/services/api.js'

export const useCarrinhoStore = defineStore('carrinho', () => {
  const carrinhos = ref([])
  const carregando = ref(false)
  const erro = ref('')

  const itens = computed(() =>
    carrinhos.value.flatMap(carrinho =>
      carrinho.itens.map(item => ({
        ...item,
        carrinho_id: carrinho.carrinho_id,
        loja: carrinho.loja,
        loja_nome: carrinho.loja_nome,
      }))
    )
  )

  const totalItens = computed(() =>
    itens.value.reduce((acc, item) => acc + Number(item.quantidade || 0), 0)
  )

  const total = computed(() =>
    itens.value.reduce((acc, item) => acc + Number(item.subtotal || 0), 0)
  )

  const porFornecedor = computed(() => {
    const grupos = {}
    for (const item of itens.value) {
      const fornecedor = item.loja_nome || 'Fornecedor'
      if (!grupos[fornecedor]) grupos[fornecedor] = []
      grupos[fornecedor].push(item)
    }
    return grupos
  })

  async function carregar() {
    if (!localStorage.getItem('access_token')) {
      limparLocal()
      return
    }

    carregando.value = true
    erro.value = ''
    try {
      carrinhos.value = await api.carrinhos.listar()
    } catch (e) {
      erro.value = extrairMensagemErro(e)
      throw e
    } finally {
      carregando.value = false
    }
  }

  async function adicionar(produtoId, quantidade = 1) {
    erro.value = ''
    try {
      await api.carrinhos.adicionar(produtoId, quantidade)
      await carregar()
    } catch (e) {
      erro.value = extrairMensagemErro(e)
      throw e
    }
  }

  async function alterarQuantidade(itemId, quantidade) {
    erro.value = ''
    try {
      await api.carrinhos.atualizarItem(itemId, quantidade)
      await carregar()
    } catch (e) {
      erro.value = extrairMensagemErro(e)
      throw e
    }
  }

  async function remover(itemId) {
    erro.value = ''
    try {
      await api.carrinhos.removerItem(itemId)
      await carregar()
    } catch (e) {
      erro.value = extrairMensagemErro(e)
      throw e
    }
  }

  async function finalizar(carrinhoProdutoIds) {
    erro.value = ''
    try {
      const pedidos = await api.pedidos.finalizarCarrinho(carrinhoProdutoIds)
      await carregar()
      return pedidos
    } catch (e) {
      erro.value = extrairMensagemErro(e)
      throw e
    }
  }

  function limparLocal() {
    carrinhos.value = []
    erro.value = ''
  }

  return {
    carrinhos,
    carregando,
    erro,
    itens,
    total,
    porFornecedor,
    totalItens,
    carregar,
    adicionar,
    alterarQuantidade,
    remover,
    finalizar,
    limparLocal,
  }
})

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

  const ordenados = computed(() =>
    [...itens.value].sort((a, b) => new Date(b.adicionadoEm) - new Date(a.adicionadoEm))
  )

  return { itens, alternar, isFavorito, ordenados }
})

function extrairMensagemErro(error) {
  if (error?.data?.detail) return error.data.detail

  const primeiroCampo = error?.data && Object.keys(error.data)[0]
  if (primeiroCampo) {
    const valor = error.data[primeiroCampo]
    return Array.isArray(valor) ? valor[0] : String(valor)
  }

  return 'Não foi possível concluir a operação.'
}
