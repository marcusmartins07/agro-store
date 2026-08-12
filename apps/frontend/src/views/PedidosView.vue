<template>
  <div>
    <h2 class="fw-bold mb-4" style="color: #1b5e35;">Meus Pedidos</h2>

    <div v-if="!authStore.estaLogado" class="card border text-center py-5 pedidos-card">
      <div class="card-body">
        <h5 class="fw-bold mb-2" style="color:#1b5e35;">Entre para ver seus pedidos</h5>
        <p class="text-muted mb-3">Os pedidos ficam vinculados à sua conta.</p>
        <RouterLink to="/login" class="btn btn-success rounded-pill px-4">Fazer login</RouterLink>
      </div>
    </div>

    <div v-else-if="carregando" class="card border text-center py-5 pedidos-card">
      <div class="card-body text-muted">Carregando pedidos...</div>
    </div>

    <div v-else-if="erro" class="alert alert-danger">{{ erro }}</div>

    <div v-else-if="pedidos.length === 0" class="card border text-center py-5 pedidos-card">
      <div class="card-body">
        <h5 class="fw-bold mb-2" style="color:#1b5e35;">Nenhum pedido encontrado</h5>
        <p class="text-muted mb-3">Finalize um carrinho para acompanhar a retirada presencial.</p>
        <RouterLink to="/" class="btn btn-success rounded-pill px-4">Ver produtos</RouterLink>
      </div>
    </div>

    <div v-else class="d-grid gap-3">
      <div v-for="pedido in pedidos" :key="pedido.pedido_id" class="card border pedidos-card">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start flex-wrap gap-2 mb-3">
            <div>
              <h5 class="fw-bold mb-1" style="color:#1b5e35;">Pedido #{{ pedido.pedido_id }}</h5>
              <p class="text-muted small mb-0">🏪 {{ pedido.loja_nome }}</p>
            </div>
            <span class="badge bg-success-subtle text-success-emphasis">{{ pedido.status_nome }}</span>
          </div>

          <div class="table-responsive">
            <table class="table table-sm align-middle mb-3">
              <thead>
                <tr>
                  <th>Produto</th>
                  <th class="text-center">Qtd.</th>
                  <th class="text-end">Subtotal</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in pedido.itens" :key="item.pedido_produto_id">
                  <td>{{ item.nome_produto }}</td>
                  <td class="text-center">{{ item.quantidade }}</td>
                  <td class="text-end">{{ formatarPreco(item.subtotal) }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="d-flex justify-content-end">
            <div class="resumo-total">
              <div class="d-flex justify-content-between text-muted small">
                <span>Bruto</span><span>{{ formatarPreco(pedido.valor_bruto) }}</span>
              </div>
              <div class="d-flex justify-content-between text-muted small">
                <span>Desconto</span><span>{{ formatarPreco(pedido.valor_desconto) }}</span>
              </div>
              <div class="d-flex justify-content-between fw-bold" style="color:#1b5e35;">
                <span>Total</span><span>{{ formatarPreco(pedido.valor_liquido) }}</span>
              </div>
            </div>
          </div>

          <div v-if="pedido.status_nome === 'Pendente'" class="d-flex justify-content-end mt-3">
            <button
              class="btn btn-outline-danger"
              :disabled="cancelando === pedido.pedido_id"
              @click="cancelarPedido(pedido)"
            >
              {{ cancelando === pedido.pedido_id ? 'Cancelando...' : 'Cancelar pedido' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/services/api.js'
import { useAuthStore } from '@/stores/auth.js'
import { useNotificacoesStore } from '@/stores/notificacoes.js'

const authStore = useAuthStore()
const pedidos = ref([])
const carregando = ref(false)
const erro = ref('')
const cancelando = ref(null)
const notificacoes = useNotificacoesStore()

onMounted(async () => {
  if (!authStore.estaLogado) return

  carregando.value = true
  try {
    pedidos.value = await api.pedidos.listar()
  } catch (e) {
    erro.value = e?.data?.detail || 'Não foi possível carregar os pedidos.'
  } finally {
    carregando.value = false
  }
})

function formatarPreco(valor) {
  return Number(valor || 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

async function cancelarPedido(pedido) {
  if (!window.confirm('Cancelar este pedido?')) return

  cancelando.value = pedido.pedido_id
  try {
    await api.pedidos.cancelar(pedido.pedido_id)
    notificacoes.notificar({ tipo: 'success', mensagem: 'Pedido cancelado com sucesso.', tempo: 4 })
    pedidos.value = await api.pedidos.listar()
  } catch (falha) {
    notificacoes.notificar({
      tipo: 'danger',
      mensagem: falha?.data?.detail || 'Não foi possível cancelar o pedido.',
    })
  } finally {
    cancelando.value = null
  }
}
</script>

<style scoped>
.pedidos-card { border-color:#d1e7d8 !important;border-radius:14px; }
.resumo-total { min-width: 220px; }
.btn-success { background-color:#2E8B57 !important;border-color:#2E8B57 !important; }
.btn-success:hover { background-color:#1e6b40 !important;border-color:#1e6b40 !important; }
</style>
