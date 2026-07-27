<template>
  <div>
    <h2 class="fw-bold mb-4" style="color: #1b5e35;">Meu Carrinho</h2>

    <div v-if="!authStore.estaLogado" class="card border text-center py-5 carrinho-card">
      <div class="card-body">
        <div class="carrinho-icone">🛒</div>
        <h5 class="fw-bold mb-2" style="color:#1b5e35;">Entre para usar o carrinho</h5>
        <p class="text-muted mb-3">Seu carrinho fica salvo na sua conta.</p>
        <RouterLink to="/login" class="btn btn-success rounded-pill px-4">Fazer login</RouterLink>
      </div>
    </div>

    <div v-else-if="carrinhoStore.carregando" class="card border text-center py-5 carrinho-card">
      <div class="card-body text-muted">Carregando carrinho...</div>
    </div>

    <div v-else-if="carrinhoStore.totalItens === 0" class="card border text-center py-5 carrinho-card">
      <div class="card-body">
        <div class="carrinho-icone">🛒</div>
        <h5 class="fw-bold mb-2" style="color:#1b5e35;">Seu carrinho está vazio</h5>
        <p class="text-muted mb-3">Você ainda não adicionou nenhum produto ao carrinho.</p>
        <RouterLink to="/" class="btn btn-success rounded-pill px-4">Voltar ao Mercado</RouterLink>
      </div>
    </div>

    <div v-else class="row g-4">
      <div class="col-12 col-lg-8">
        <div v-if="mensagemErro" class="alert alert-danger">{{ mensagemErro }}</div>

        <div v-for="(itens, fornecedor) in carrinhoStore.porFornecedor" :key="fornecedor" class="mb-3">
          <p class="text-muted small fw-bold text-uppercase mb-2">🏪 {{ fornecedor }}</p>

          <div v-for="item in itens" :key="item.carrinho_produto_id" class="card border mb-2 carrinho-card">
            <div class="card-body p-3 d-flex align-items-center gap-3">
              <input
                class="form-check-input item-checkbox"
                type="checkbox"
                :checked="selecionados.has(item.carrinho_produto_id)"
                @change="alternarSelecao(item.carrinho_produto_id)"
              />

              <div class="produto-img-mini">{{ emojiCategoria(item.produto_nome) }}</div>

              <div class="flex-grow-1">
                <p class="fw-bold mb-0 small" style="color:#1b5e35;">{{ item.produto_nome }}</p>
                <p class="fw-bold mb-0" style="color:#2E8B57;">{{ formatarPreco(item.valor_unitario - item.valor_desconto) }}</p>
              </div>

              <div class="d-flex align-items-center gap-2">
                <button
                  class="btn btn-outline-secondary btn-sm"
                  :disabled="salvando"
                  @click="alterarQuantidade(item, item.quantidade - 1)"
                >
                  −
                </button>
                <span class="fw-bold quantidade">{{ item.quantidade }}</span>
                <button
                  class="btn btn-outline-secondary btn-sm"
                  :disabled="salvando"
                  @click="alterarQuantidade(item, item.quantidade + 1)"
                >
                  +
                </button>
              </div>

              <span class="fw-bold ms-2 subtotal">{{ formatarPreco(item.subtotal) }}</span>
              <button class="btn btn-link text-danger p-0 ms-1" :disabled="salvando" @click="remover(item.carrinho_produto_id)">✕</button>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-lg-4">
        <div class="card border carrinho-card">
          <div class="card-body p-4">
            <h6 class="fw-bold mb-3" style="color:#1b5e35;">Resumo do pedido</h6>

            <div v-for="grupo in resumoPorFornecedor" :key="grupo.fornecedor" class="d-flex justify-content-between small text-muted mb-1">
              <span>{{ grupo.fornecedor }}</span>
              <span>{{ formatarPreco(grupo.total) }}</span>
            </div>

            <hr style="border-color:#d1e7d8;" />

            <div class="d-flex justify-content-between fw-bold mb-2" style="color:#1b5e35;">
              <span>Selecionados</span><span>{{ totalSelecionados }} item(ns)</span>
            </div>
            <div class="d-flex justify-content-between fw-bold mb-4" style="color:#1b5e35;">
              <span>Total</span><span>{{ formatarPreco(totalSelecionado) }}</span>
            </div>

            <button class="btn btn-success w-100 fw-bold py-2" :disabled="finalizando || totalSelecionados === 0" @click="finalizarPedido">
              {{ finalizando ? 'Finalizando...' : 'Finalizar Pedido' }}
            </button>
            <RouterLink to="/" class="btn btn-outline-secondary w-100 mt-2">Continuar comprando</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import { useCarrinhoStore } from '@/stores/index.js'

const router = useRouter()
const authStore = useAuthStore()
const carrinhoStore = useCarrinhoStore()
const selecionados = ref(new Set())
const salvando = ref(false)
const finalizando = ref(false)
const mensagemErro = ref('')

const totalSelecionado = computed(() =>
  carrinhoStore.itens
    .filter(item => selecionados.value.has(item.carrinho_produto_id))
    .reduce((acc, item) => acc + Number(item.subtotal || 0), 0)
)

const totalSelecionados = computed(() =>
  carrinhoStore.itens
    .filter(item => selecionados.value.has(item.carrinho_produto_id))
    .reduce((acc, item) => acc + Number(item.quantidade || 0), 0)
)

const resumoPorFornecedor = computed(() => {
  const grupos = {}
  for (const item of carrinhoStore.itens) {
    if (!selecionados.value.has(item.carrinho_produto_id)) continue
    const fornecedor = item.loja_nome || 'Fornecedor'
    grupos[fornecedor] = (grupos[fornecedor] || 0) + Number(item.subtotal || 0)
  }
  return Object.entries(grupos).map(([fornecedor, total]) => ({ fornecedor, total }))
})

onMounted(async () => {
  if (authStore.estaLogado) await carregarCarrinho()
})

watch(() => carrinhoStore.itens, () => {
  const idsAtuais = carrinhoStore.itens.map(item => item.carrinho_produto_id)
  selecionados.value = new Set(idsAtuais.filter(id => selecionados.value.has(id)))
})

async function carregarCarrinho() {
  mensagemErro.value = ''
  try {
    await carrinhoStore.carregar()
    selecionados.value = new Set(carrinhoStore.itens.map(item => item.carrinho_produto_id))
  } catch (e) {
    mensagemErro.value = carrinhoStore.erro
  }
}

function alternarSelecao(itemId) {
  const proximos = new Set(selecionados.value)
  if (proximos.has(itemId)) {
    proximos.delete(itemId)
  } else {
    proximos.add(itemId)
  }
  selecionados.value = proximos
}

async function alterarQuantidade(item, quantidade) {
  if (quantidade < 1) return

  mensagemErro.value = ''
  salvando.value = true
  try {
    await carrinhoStore.alterarQuantidade(item.carrinho_produto_id, quantidade)
  } catch (e) {
    mensagemErro.value = carrinhoStore.erro
  } finally {
    salvando.value = false
  }
}

async function remover(itemId) {
  mensagemErro.value = ''
  salvando.value = true
  try {
    await carrinhoStore.remover(itemId)
    const proximos = new Set(selecionados.value)
    proximos.delete(itemId)
    selecionados.value = proximos
  } catch (e) {
    mensagemErro.value = carrinhoStore.erro
  } finally {
    salvando.value = false
  }
}

async function finalizarPedido() {
  mensagemErro.value = ''
  finalizando.value = true
  try {
    await carrinhoStore.finalizar([...selecionados.value])
    selecionados.value = new Set()
    router.push({ name: 'pedidos' })
  } catch (e) {
    mensagemErro.value = carrinhoStore.erro
  } finally {
    finalizando.value = false
  }
}

function formatarPreco(valor) {
  return Number(valor || 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function emojiCategoria(nome) {
  const texto = String(nome || '').toLowerCase()
  if (texto.includes('maçã') || texto.includes('fruta')) return '🍎'
  if (texto.includes('alface') || texto.includes('verdura')) return '🥬'
  if (texto.includes('cenoura')) return '🥕'
  return '🌱'
}
</script>

<style scoped>
.carrinho-card { border-color:#d1e7d8 !important;border-radius:14px; }
.carrinho-icone {
  width:80px;height:80px;background:#c8e6c9;border-radius:50%;
  display:flex;align-items:center;justify-content:center;font-size:34px;margin:0 auto 1rem;
}
.produto-img-mini {
  width:52px;height:52px;background:#E8F5E9;border-radius:10px;
  display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0;
}
.item-checkbox { width:18px;height:18px; }
.quantidade { min-width:20px;text-align:center; }
.subtotal { min-width:80px;text-align:right;color:#1b5e35; }
.btn-success { background-color:#2E8B57 !important;border-color:#2E8B57 !important; }
.btn-success:hover { background-color:#1e6b40 !important;border-color:#1e6b40 !important; }
</style>
