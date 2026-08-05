<template>
  <section>
    <div class="d-flex justify-content-between align-items-start flex-wrap gap-3 mb-4">
      <div>
        <h1 class="h2 fw-bold mb-1">Área do produtor</h1>
        <p class="text-body-secondary mb-0">Acompanhe sua loja, produtos e pedidos para retirada.</p>
      </div>
      <RouterLink v-if="loja" :to="{ name: 'produtos-produtor' }" class="btn btn-success">Gerenciar produtos</RouterLink>
    </div>

    <div v-if="carregando" class="row g-3">
      <div v-for="indice in 3" :key="indice" class="col-12 col-md-4"><div class="card p-4 placeholder-glow"><span class="placeholder col-8"></span></div></div>
    </div>

    <div v-else-if="erro" class="alert alert-danger" role="alert">
      {{ erro }} <button class="btn btn-sm btn-outline-danger ms-2" @click="carregarPainel">Tentar novamente</button>
    </div>

    <div v-else-if="!loja" class="card text-center p-5">
      <h2 class="h5 fw-bold">Você ainda não possui uma loja</h2>
      <p class="text-body-secondary">Crie sua loja para cadastrar produtos e receber pedidos.</p>
      <RouterLink to="/criar-loja" class="btn btn-success align-self-center">Criar minha loja</RouterLink>
    </div>

    <template v-else>
      <div class="row g-3 mb-4">
        <div class="col-12 col-md-4"><article class="card h-100 p-3"><span class="text-body-secondary small">Produtos ativos</span><strong class="display-6">{{ produtosAtivos }}</strong></article></div>
        <div class="col-12 col-md-4"><article class="card h-100 p-3"><span class="text-body-secondary small">Produtos inativos</span><strong class="display-6">{{ produtosInativos }}</strong></article></div>
        <div class="col-12 col-md-4"><article class="card h-100 p-3"><span class="text-body-secondary small">Pedidos em andamento</span><strong class="display-6">{{ pedidosEmAndamento }}</strong></article></div>
      </div>

      <div class="row g-4">
        <div class="col-12 col-lg-7">
          <div class="card h-100"><div class="card-body p-4">
            <h2 class="h5 fw-bold">Operação da loja</h2>
            <p class="text-body-secondary">{{ loja.nome }} está {{ loja.ativa ? 'ativa' : 'inativa' }}.</p>
            <div class="d-flex flex-wrap gap-2">
              <RouterLink :to="{ name: 'produtos-produtor' }" class="btn btn-success">Meus produtos</RouterLink>
              <RouterLink :to="{ name: 'pedidos-produtor' }" class="btn btn-outline-success">Pedidos da loja</RouterLink>
            </div>
          </div></div>
        </div>
        <div class="col-12 col-lg-5">
          <div class="card h-100"><div class="card-body p-4">
            <h2 class="h5 fw-bold">Configurações da loja</h2>
            <label for="descricao-loja" class="form-label">Descrição</label>
            <textarea id="descricao-loja" v-model="descricao" class="form-control mb-3" rows="3" :disabled="salvando"></textarea>
            <button class="btn btn-outline-success w-100 mb-2" :disabled="salvando" @click="salvarDescricao">Salvar descrição</button>
            <button v-if="loja.ativa" class="btn btn-outline-danger w-100" :disabled="salvando" @click="desativarLoja">Desativar loja</button>
            <p v-else class="small text-body-secondary mb-0">A loja está inativa e não aceita novas compras.</p>
          </div></div>
        </div>
      </div>
    </template>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { api } from '@/services/api.js'
import { useNotificacoesStore } from '@/stores/notificacoes.js'

const loja = ref(null)
const produtos = ref([])
const pedidos = ref([])
const descricao = ref('')
const carregando = ref(true)
const salvando = ref(false)
const erro = ref('')
const notificacoes = useNotificacoesStore()
const produtosAtivos = computed(() => produtos.value.filter(produto => produto.ativo).length)
const produtosInativos = computed(() => produtos.value.filter(produto => !produto.ativo).length)
const pedidosEmAndamento = computed(() => pedidos.value.filter(pedido => ['Pendente', 'Em preparo'].includes(pedido.status_nome)).length)

async function carregarPainel() {
  carregando.value = true
  erro.value = ''
  try {
    loja.value = await api.lojas.me()
    descricao.value = loja.value.descricao || ''
    ;[produtos.value, pedidos.value] = await Promise.all([api.produtos.listarMeus(), api.pedidos.listarMinhaLoja()])
  } catch (falha) {
    if (falha?.status === 404) loja.value = null
    else erro.value = falha?.data?.detail || 'Não foi possível carregar a área do produtor.'
  } finally {
    carregando.value = false
  }
}

async function salvarDescricao() {
  salvando.value = true
  try {
    loja.value = await api.lojas.atualizarMinha({ descricao: descricao.value })
    notificacoes.notificar({ tipo: 'success', mensagem: 'Descrição da loja atualizada.', tempo: 4 })
  } catch (falha) {
    notificacoes.notificar({ tipo: 'danger', mensagem: falha?.data?.detail || 'Não foi possível atualizar a loja.' })
  } finally { salvando.value = false }
}

async function desativarLoja() {
  if (!window.confirm('Desativar a loja impedirá novas compras. Deseja continuar?')) return
  salvando.value = true
  try {
    loja.value = await api.lojas.atualizarMinha({ ativa: false })
    notificacoes.notificar({ tipo: 'warning', mensagem: 'Loja desativada. Produtos e pedidos foram preservados.' })
  } catch (falha) {
    notificacoes.notificar({ tipo: 'danger', mensagem: falha?.data?.detail || 'Não foi possível desativar a loja.' })
  } finally { salvando.value = false }
}

onMounted(carregarPainel)
</script>
