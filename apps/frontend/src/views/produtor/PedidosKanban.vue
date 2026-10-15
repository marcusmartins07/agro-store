<template>
  <div>
    <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
      <div>
        <h2 class="h4 fw-semibold mb-1">Pedidos da loja</h2>
        <p class="small text-body-secondary mb-0">Avance cada pedido até a entrega na feira. Cancelamentos devolvem os produtos ao estoque.</p>
      </div>
      <button
        type="button"
        class="btn btn-sm btn-outline-secondary rounded-pill px-3"
        :disabled="produtorStore.carregando"
        @click="produtorStore.carregar({ forcar: true })"
      >
        {{ produtorStore.carregando ? 'Atualizando...' : 'Atualizar pedidos' }}
      </button>
    </div>

    <div class="row g-3 quadro">
      <section
        v-for="status in STATUS_KANBAN"
        :key="status"
        class="col-12 col-md-6 col-xl-3"
        :aria-labelledby="`coluna-${idDoStatus(status)}`"
      >
        <div class="coluna bg-apoio rounded-4 p-2 p-md-3 h-100">
          <h3 :id="`coluna-${idDoStatus(status)}`" class="h6 d-flex align-items-center justify-content-between gap-2 mb-3 titulo-coluna">
            <SeloStatus :status="status" />
            <span class="small text-body-secondary">
              {{ pedidosDe(status).length }}<span class="visually-hidden"> pedidos</span>
            </span>
          </h3>

          <div v-if="pedidosDe(status).length" class="d-grid gap-2">
            <CartaoPedidoKanban
              v-for="pedido in pedidosDe(status)"
              :key="pedido.pedido_id"
              :pedido="pedido"
              :atualizando="atualizando === pedido.pedido_id"
              @avancar="avancar"
              @cancelar="cancelar"
            />
          </div>
          <p v-else class="small text-body-secondary text-center py-4 mb-0">Nenhum pedido nesta etapa.</p>
        </div>
      </section>
    </div>

    <section v-if="cancelados.length" class="mt-4" aria-labelledby="titulo-cancelados">
      <h3 id="titulo-cancelados" class="h6 mb-0">
        <button
          type="button"
          class="btn btn-link p-0 d-inline-flex align-items-center gap-2 botao-cancelados"
          :aria-expanded="mostrarCancelados"
          aria-controls="lista-cancelados"
          @click="mostrarCancelados = !mostrarCancelados"
        >
          <IconeSvg nome="seta-baixo" :tamanho="16" class="seta" :class="{ aberta: mostrarCancelados }" />
          Cancelados ({{ cancelados.length }})
        </button>
      </h3>
      <div v-show="mostrarCancelados" id="lista-cancelados" class="row row-cols-1 row-cols-md-2 row-cols-xl-4 g-2 mt-1">
        <div v-for="pedido in cancelados" :key="pedido.pedido_id" class="col">
          <CartaoPedidoKanban :pedido="pedido" />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import CartaoPedidoKanban from '@/components/CartaoPedidoKanban.vue'
import IconeSvg from '@/components/IconeSvg.vue'
import SeloStatus from '@/components/SeloStatus.vue'
import { useNotificacoesStore } from '@/stores/notificacoes.js'
import { useProdutorStore } from '@/stores/produtor.js'
import { STATUS_KANBAN } from '@/utils/statusPedido.js'

const produtorStore = useProdutorStore()
const notificacoes = useNotificacoesStore()
const atualizando = ref(null)
const mostrarCancelados = ref(false)

const cancelados = computed(() => produtorStore.pedidosPorStatus.Cancelado || [])

function pedidosDe(status) {
  return produtorStore.pedidosPorStatus[status] || []
}

function idDoStatus(status) {
  return status.toLowerCase().replaceAll(' ', '-')
}

async function avancar(pedido, proximoStatus) {
  await mudarStatus(pedido, proximoStatus, `Pedido #${pedido.pedido_id} movido para ${proximoStatus}.`)
}

async function cancelar(pedido) {
  if (!window.confirm(`Cancelar o pedido #${pedido.pedido_id}? Os produtos voltarão ao estoque.`)) return
  await mudarStatus(pedido, 'Cancelado', `Pedido #${pedido.pedido_id} cancelado.`)
}

// A notificação global já é anunciada por leitores de tela (aria-live)
async function mudarStatus(pedido, novoStatus, mensagem) {
  atualizando.value = pedido.pedido_id
  try {
    await produtorStore.atualizarStatus(pedido, novoStatus)
    notificacoes.notificar({ tipo: 'success', mensagem, tempo: 4 })
  } catch (falha) {
    notificacoes.notificar({ tipo: 'danger', mensagem: falha.message || 'Não foi possível atualizar o status.' })
  } finally {
    atualizando.value = null
  }
}
</script>

<style scoped>
.titulo-coluna {
  font-family: var(--fonte-texto);
}
.botao-cancelados {
  color: var(--cor-texto);
  font-weight: 600;
  text-decoration: none;
}
.botao-cancelados:hover {
  color: var(--cor-primaria);
}
.seta {
  transition: transform 0.15s ease;
}
.seta.aberta {
  transform: rotate(180deg);
}
@media (prefers-reduced-motion: reduce) {
  .seta {
    transition: none;
  }
}
</style>
