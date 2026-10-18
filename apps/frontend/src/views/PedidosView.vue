<template>
  <section>
    <div class="mb-4">
      <h1 ref="titulo" class="fw-semibold mb-1" tabindex="-1">Meus pedidos</h1>
      <p class="text-body-secondary mb-2">Acompanhe o andamento dos pedidos feitos nas lojas da feira.</p>
      <p class="d-flex align-items-start gap-2 small text-body-secondary mb-0">
        <IconeSvg nome="local" :tamanho="16" />
        <span>{{ textoRetirada() }}</span>
      </p>
    </div>

    <div v-if="!authStore.estaLogado" class="card rounded-4 text-center py-5">
      <div class="card-body">
        <span class="icone-estado mb-3"><IconeSvg nome="recibo" :tamanho="32" /></span>
        <h2 class="h4 fw-semibold mb-2">Entre para ver seus pedidos</h2>
        <p class="text-body-secondary mb-3">Os pedidos ficam vinculados à sua conta.</p>
        <RouterLink :to="{ name: 'login', query: { retorno: route.fullPath } }" class="btn btn-primary rounded-pill px-4">Entrar</RouterLink>
      </div>
    </div>

    <div v-else-if="carregando" class="d-grid gap-3">
      <span class="visually-hidden" role="status">Carregando pedidos...</span>
      <div v-for="n in 2" :key="n" class="card rounded-4 placeholder-glow" aria-hidden="true">
        <div class="card-body p-4">
          <span class="placeholder col-3 d-block mb-3"></span>
          <span class="placeholder col-6 d-block mb-2"></span>
          <span class="placeholder col-8 d-block"></span>
        </div>
      </div>
    </div>

    <div v-else-if="erro" class="alert alert-danger d-flex flex-wrap align-items-center gap-2" role="alert">
      <span><strong>Não foi possível carregar os pedidos.</strong> {{ erro }}</span>
      <button type="button" class="btn btn-sm btn-outline-danger" @click="carregar">Tentar novamente</button>
    </div>

    <div v-else-if="pedidos.length === 0" class="card rounded-4 text-center py-5">
      <div class="card-body">
        <span class="icone-estado mb-3"><IconeSvg nome="recibo" :tamanho="32" /></span>
        <h2 class="h4 fw-semibold mb-2">Você ainda não fez pedidos</h2>
        <p class="text-body-secondary mb-3">Finalize um carrinho para acompanhar a preparação e a retirada aqui.</p>
        <RouterLink :to="{ name: 'produtos' }" class="btn btn-primary rounded-pill px-4">Explorar produtos</RouterLink>
      </div>
    </div>

    <template v-else>
      <div class="d-flex gap-2 overflow-x-auto pb-1 mb-4" role="group" aria-label="Filtrar pedidos por status">
        <button
          v-for="opcao in opcoesFiltro"
          :key="opcao.valor"
          type="button"
          class="btn btn-sm rounded-pill px-3 flex-shrink-0"
          :class="opcao.valor === filtro ? 'btn-primary' : 'btn-outline-secondary'"
          :aria-pressed="opcao.valor === filtro"
          @click="filtro = opcao.valor"
        >
          {{ opcao.rotulo }} <span class="opacity-75">({{ opcao.quantidade }})</span>
        </button>
      </div>

      <div v-if="pedidosFiltrados.length === 0" class="card rounded-4 text-center py-5">
        <div class="card-body">
          <p class="text-body-secondary mb-3">Nenhum pedido com o status "{{ filtro }}".</p>
          <button type="button" class="btn btn-outline-primary rounded-pill px-4" @click="filtro = TODOS">Ver todos os pedidos</button>
        </div>
      </div>

      <div v-else class="d-grid gap-3">
        <article
          v-for="pedido in pedidosFiltrados"
          :key="pedido.pedido_id"
          class="card rounded-4"
          :aria-labelledby="`titulo-pedido-${pedido.pedido_id}`"
        >
          <div class="card-body p-3 p-md-4">
            <div class="d-flex justify-content-between align-items-start flex-wrap gap-2 mb-3">
              <div>
                <h2 :id="`titulo-pedido-${pedido.pedido_id}`" class="h5 fw-semibold mb-1">Pedido #{{ pedido.pedido_id }}</h2>
                <p class="small text-body-secondary d-flex flex-wrap align-items-center column-gap-3 row-gap-1 mb-0">
                  <span v-if="pedido.data_criacao" class="d-inline-flex align-items-center gap-1">
                    <IconeSvg nome="calendario" :tamanho="14" />
                    <span class="visually-hidden">Feito em</span>
                    <time :datetime="pedido.data_criacao">{{ formatarData(pedido.data_criacao) }}</time>
                  </span>
                  <RouterLink :to="{ name: 'loja', params: { id: pedido.loja } }" class="link-loja d-inline-flex align-items-center gap-1">
                    <IconeSvg nome="loja" :tamanho="14" />
                    <span class="visually-hidden">Loja:</span>
                    {{ pedido.loja_nome }}
                  </RouterLink>
                </p>
              </div>
              <SeloStatus :status="pedido.status_nome" />
            </div>

            <p v-if="temAvaliacaoPendente(pedido)" class="small text-body-secondary mb-2">
              Conte como foi a experiência com os produtos deste pedido.
            </p>

            <div class="table-responsive">
              <table class="table table-sm align-middle mb-3">
                <caption class="visually-hidden">Produtos do pedido #{{ pedido.pedido_id }}</caption>
                <thead>
                  <tr>
                    <th scope="col">Produto</th>
                    <th scope="col" class="text-center">Qtd.</th>
                    <th scope="col" class="text-end">Subtotal</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in pedido.itens" :key="item.pedido_produto_id">
                    <td>
                      <span class="d-block text-break">{{ item.nome_produto }}</span>
                      <span v-if="!item.produto && pedido.status_nome !== STATUS_ENTREGUE" class="small text-body-secondary">
                        Produto não está mais disponível
                      </span>
                      <template v-if="pedido.status_nome === STATUS_ENTREGUE">
                        <button
                          v-if="podeAvaliar(item)"
                          type="button"
                          class="btn btn-sm btn-outline-primary rounded-pill px-3 mt-1"
                          :aria-label="`Avaliar ${item.nome_produto}`"
                          @click="abrirAvaliacao(pedido, item)"
                        >
                          Avaliar
                        </button>
                        <div
                          v-else-if="item.avaliacao"
                          :id="`avaliado-${item.pedido_produto_id}`"
                          class="bloco-avaliado d-flex flex-wrap align-items-center column-gap-2 row-gap-1 small mt-1"
                          tabindex="-1"
                        >
                          <AvaliacaoEstrelas :nota="Number(item.avaliacao.nota)" :tamanho="14" />
                          <span class="text-body-secondary">Avaliado</span>
                          <RouterLink v-if="item.produto" :to="{ name: 'produto', params: { id: item.produto }, hash: '#avaliacoes' }">
                            Ver no produto<span class="visually-hidden">: {{ item.nome_produto }}</span>
                          </RouterLink>
                        </div>
                        <span v-else-if="!item.produto" class="small text-body-secondary">Produto não está mais disponível</span>
                      </template>
                    </td>
                    <td class="text-center">{{ item.quantidade }}</td>
                    <td class="text-end">{{ formatarPreco(item.subtotal) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="d-flex flex-column flex-sm-row justify-content-between align-items-sm-end gap-3">
              <div>
                <button
                  v-if="pedido.status_nome === 'Pendente'"
                  type="button"
                  class="btn btn-sm btn-outline-danger rounded-pill px-3"
                  :disabled="cancelando === pedido.pedido_id"
                  @click="cancelarPedido(pedido)"
                >
                  <span v-if="cancelando === pedido.pedido_id" class="spinner-border spinner-border-sm me-1" aria-hidden="true"></span>
                  {{ cancelando === pedido.pedido_id ? 'Cancelando...' : 'Cancelar pedido' }}
                </button>
              </div>

              <dl class="resumo-valores bg-apoio rounded-4 p-3 mb-0">
                <div class="d-flex justify-content-between gap-3 small mb-1">
                  <dt class="fw-normal">Valor bruto</dt>
                  <dd class="mb-0">{{ formatarPreco(pedido.valor_bruto) }}</dd>
                </div>
                <div class="d-flex justify-content-between gap-3 small mb-2">
                  <dt class="fw-normal">Desconto</dt>
                  <dd class="mb-0">- {{ formatarPreco(pedido.valor_desconto) }}</dd>
                </div>
                <div class="d-flex justify-content-between gap-3 fw-bold border-top pt-2">
                  <dt>Total</dt>
                  <dd class="mb-0 text-primary">{{ formatarPreco(pedido.valor_liquido) }}</dd>
                </div>
              </dl>
            </div>
          </div>
        </article>
      </div>
    </template>

    <ModalConfirmacao
      ref="modalAvaliacao"
      titulo="Avaliar produto"
      texto-confirmar="Enviar avaliação"
      texto-carregando="Enviando..."
      variante="primary"
      rolavel
      :carregando="enviandoAvaliacao"
      @confirmar="enviarAvaliacao"
      @fechado="aoFecharAvaliacao"
    >
      <FormularioAvaliacao
        v-if="avaliando"
        ref="formularioAvaliacao"
        v-model:nota="notaAvaliacao"
        v-model:comentario="comentarioAvaliacao"
        :nome-produto="avaliando.item.nome_produto"
        :pedido-id="avaliando.pedido.pedido_id"
        :loja-nome="avaliando.pedido.loja_nome"
        :desabilitado="enviandoAvaliacao"
        :erro="erroAvaliacao"
        :erro-nota="erroNota"
        @enviar="enviarAvaliacao"
      />
    </ModalConfirmacao>
  </section>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import AvaliacaoEstrelas from '@/components/AvaliacaoEstrelas.vue'
import FormularioAvaliacao from '@/components/FormularioAvaliacao.vue'
import IconeSvg from '@/components/IconeSvg.vue'
import ModalConfirmacao from '@/components/ModalConfirmacao.vue'
import SeloStatus from '@/components/SeloStatus.vue'
import { api } from '@/services/api.js'
import { useAuthStore } from '@/stores/auth.js'
import { extrairMensagemErro } from '@/stores/index.js'
import { useNotificacoesStore } from '@/stores/notificacoes.js'
import { textoRetirada } from '@/data/feira.js'
import { formatarData, formatarPreco } from '@/utils/formatacao.js'
import { ORDEM_STATUS, ordenarPorMaisRecente } from '@/utils/statusPedido.js'

const TODOS = 'Todos'
const STATUS_ENTREGUE = 'Entregue'
const MENSAGEM_JA_AVALIADO = 'Este item já foi avaliado.'
const MENSAGEM_FALHA_ENVIO = 'Não foi possível enviar a avaliação. Verifique sua conexão e tente novamente.'

const route = useRoute()
const authStore = useAuthStore()
const notificacoes = useNotificacoesStore()
const pedidos = ref([])
const carregando = ref(false)
const erro = ref('')
const cancelando = ref(null)
const filtro = ref(TODOS)

const titulo = ref(null)
const modalAvaliacao = ref(null)
const formularioAvaliacao = ref(null)
const avaliando = ref(null)
const notaAvaliacao = ref(null)
const comentarioAvaliacao = ref('')
const erroAvaliacao = ref('')
const erroNota = ref('')
const enviandoAvaliacao = ref(false)
// Para onde levar o foco quando o modal terminar de fechar: id do bloco "Avaliado" ou o título da página
let focoAposFechar = null

const pedidosOrdenados = computed(() => ordenarPorMaisRecente(pedidos.value))

const opcoesFiltro = computed(() => [
  { valor: TODOS, rotulo: TODOS, quantidade: pedidos.value.length },
  ...ORDEM_STATUS.map(status => ({
    valor: status,
    rotulo: status,
    quantidade: pedidos.value.filter(pedido => pedido.status_nome === status).length,
  })),
])

const pedidosFiltrados = computed(() =>
  filtro.value === TODOS
    ? pedidosOrdenados.value
    : pedidosOrdenados.value.filter(pedido => pedido.status_nome === filtro.value)
)

// Escolher uma nota resolve o erro de validação do seletor
watch(notaAvaliacao, nota => {
  if (nota) erroNota.value = ''
})

onMounted(() => {
  if (authStore.estaLogado) carregar()
})

async function carregar() {
  carregando.value = true
  erro.value = ''
  try {
    pedidos.value = await api.pedidos.listar()
  } catch (falha) {
    erro.value = falha?.data?.detail || 'Verifique sua conexão e tente novamente.'
  } finally {
    carregando.value = false
  }
}

// O campo avaliacao vem da API (BE-019): null = item ainda não avaliado
function temAvaliacaoPendente(pedido) {
  return pedido.status_nome === STATUS_ENTREGUE && pedido.itens.some(podeAvaliar)
}

function podeAvaliar(item) {
  return item.avaliacao === null && Boolean(item.produto)
}

function abrirAvaliacao(pedido, item) {
  avaliando.value = { pedido, item }
  notaAvaliacao.value = null
  comentarioAvaliacao.value = ''
  erroAvaliacao.value = ''
  erroNota.value = ''
  focoAposFechar = null
  modalAvaliacao.value.abrir()
}

async function enviarAvaliacao() {
  if (enviandoAvaliacao.value || !avaliando.value) return
  erroAvaliacao.value = ''

  if (!notaAvaliacao.value) {
    erroNota.value = 'Escolha uma nota de 1 a 5 estrelas.'
    formularioAvaliacao.value?.focarNota()
    return
  }
  erroNota.value = ''

  const { item } = avaliando.value
  enviandoAvaliacao.value = true
  try {
    const avaliacao = await api.avaliacoes.criar({
      pedido_produto: item.pedido_produto_id,
      nota: notaAvaliacao.value,
      comentario: comentarioAvaliacao.value.trim(),
    })
    item.avaliacao = { avaliacao_id: avaliacao.avaliacao_id, nota: avaliacao.nota, comentario: avaliacao.comentario }
    focoAposFechar = `avaliado-${item.pedido_produto_id}`
    enviandoAvaliacao.value = false
    modalAvaliacao.value.fechar()
    notificacoes.notificar({ tipo: 'success', mensagem: 'Avaliação enviada. Obrigado por ajudar outros clientes.', tempo: 5 })
  } catch (falha) {
    enviandoAvaliacao.value = false
    const mensagem = mensagemErroAvaliacao(falha)
    if (mensagem === MENSAGEM_JA_AVALIADO) {
      focoAposFechar = 'titulo'
      modalAvaliacao.value.fechar()
      notificacoes.notificar({ tipo: 'warning', mensagem, tempo: 6 })
      await carregar()
    } else {
      erroAvaliacao.value = mensagem
    }
  }
}

function mensagemErroAvaliacao(falha) {
  // Sem status, a requisição nem chegou ao servidor
  if (!falha?.status) return MENSAGEM_FALHA_ENVIO
  const dados = falha.data || {}
  const campo = ['pedido_produto', 'nota', 'comentario'].find(nome => Array.isArray(dados[nome]) && dados[nome].length)
  return campo ? dados[campo][0] : extrairMensagemErro(falha)
}

async function aoFecharAvaliacao() {
  const destino = focoAposFechar
  focoAposFechar = null
  avaliando.value = null
  if (!destino) return
  await nextTick()
  const elemento = destino === 'titulo' ? titulo.value : document.getElementById(destino)
  elemento?.focus()
}

async function cancelarPedido(pedido) {
  if (!window.confirm(`Cancelar o pedido #${pedido.pedido_id}? Os produtos voltam ao estoque da loja.`)) return

  cancelando.value = pedido.pedido_id
  try {
    const atualizado = await api.pedidos.cancelar(pedido.pedido_id)
    pedidos.value = pedidos.value.map(item => item.pedido_id === atualizado.pedido_id ? atualizado : item)
    notificacoes.notificar({ tipo: 'success', mensagem: `Pedido #${pedido.pedido_id} cancelado.`, tempo: 4 })
  } catch (falha) {
    notificacoes.notificar({ tipo: 'danger', mensagem: extrairMensagemErro(falha) })
  } finally {
    cancelando.value = null
  }
}
</script>

<style scoped>
.link-loja:hover {
  color: var(--cor-primaria);
  text-decoration: underline;
}
.bloco-avaliado:focus-visible {
  outline: 2px solid var(--cor-foco);
  outline-offset: 2px;
  border-radius: var(--bs-border-radius-sm);
}
.resumo-valores {
  min-width: min(100%, 16rem);
}
</style>
