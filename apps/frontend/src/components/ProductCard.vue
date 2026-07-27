<template>
  <div class="card h-100 border product-card">
    <!-- Imagem -->
    <div class="card-img-top product-img position-relative">
      <span class="emoji">{{ emojiCategoria(produto.categoria_nome) }}</span>

      <span v-if="Number(produto.desconto) > 0" class="badge position-absolute top-0 start-0 m-2 desconto-badge">
        -{{ produto.desconto }}%
      </span>

      <button
        class="btn btn-sm position-absolute top-0 end-0 m-2 rounded-circle fav-btn"
        :class="favoritosStore.isFavorito(produto.produto_id) ? 'btn-danger' : 'btn-light'"
        @click.stop="favoritosStore.alternar(produto)"
        title="Favoritar"
      >
        {{ favoritosStore.isFavorito(produto.produto_id) ? '♥' : '♡' }}
      </button>
    </div>

    <!-- Informações -->
    <div class="card-body d-flex flex-column p-3">
      <div class="d-flex justify-content-between align-items-center mb-1">
        <span class="categoria-badge">{{ produto.categoria_nome }}</span>
        <small class="text-muted">🏪 {{ produto.loja_nome }}</small>
      </div>

      <h6 class="card-title fw-bold text-success-emphasis mb-1">{{ produto.nome }}</h6>

      <p v-if="produto.descricao" class="card-text text-muted small mb-2">{{ produto.descricao }}</p>

      <div class="d-flex align-items-baseline gap-2 mb-3 mt-auto">
        <span class="fs-5 fw-bold text-success">{{ formatarPreco(produto.preco) }}</span>
        <small v-if="Number(produto.desconto) > 0" class="text-muted text-decoration-line-through">
          {{ formatarPreco(produto.preco_original) }}
        </small>
      </div>

      <button class="btn btn-success w-100" :disabled="adicionando || !podeComprar" @click="adicionarAoCarrinho">
        {{ textoBotao }}
      </button>
      <p v-if="mensagem" class="text-danger small mt-2 mb-0">{{ mensagem }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCarrinhoStore, useFavoritosStore } from '@/stores/index.js'
import { useAuthStore } from '@/stores/auth.js'

const props = defineProps({
  produto: { type: Object, required: true }
})

const router = useRouter()
const carrinhoStore  = useCarrinhoStore()
const favoritosStore = useFavoritosStore()
const authStore = useAuthStore()
const adicionando = ref(false)
const mensagem = ref('')

const podeComprar = computed(() =>
  props.produto.ativo !== false && Number(props.produto.estoque || 0) > 0
)

const textoBotao = computed(() => {
  if (adicionando.value) return 'Adicionando...'
  if (props.produto.ativo === false) return 'Produto inativo'
  if (Number(props.produto.estoque || 0) <= 0) return 'Sem estoque'
  return '🛒 Adicionar'
})

async function adicionarAoCarrinho() {
  mensagem.value = ''

  if (!authStore.estaLogado) {
    router.push({ name: 'login' })
    return
  }

  adicionando.value = true
  try {
    await carrinhoStore.adicionar(props.produto.produto_id)
  } catch (e) {
    mensagem.value = carrinhoStore.erro
  } finally {
    adicionando.value = false
  }
}

function formatarPreco(valor) {
  return Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

// Emoji automático baseado na categoria da API
function emojiCategoria(categoria) {
  const mapa = {
    'Vegetais':    '🥦',
    'Verduras':    '🥬',
    'Frutas':      '🍎',
    'Doces':       '🍯',
    'Laticínios':  '🧀',
    'Grãos':       '🌾',
    'Artesanato':  '🫒',
    'Pães':        '🍞',
    'Carnes':      '🥩',
    'Ovos':        '🥚',
  }
  return mapa[categoria] ?? '🌱'
}
</script>

<style scoped>
.product-card {
  border-radius: 14px !important;
  border-color: #d1e7d8 !important;
  transition: transform 0.15s, box-shadow 0.15s;
  overflow: hidden;
}
.product-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(46, 139, 87, 0.15) !important;
}
.product-img {
  height: 160px;
  background: #E8F5E9;
  display: flex;
  align-items: center;
  justify-content: center;
}
.emoji { font-size: 56px; line-height: 1; }
.desconto-badge {
  background-color: #a5d6a7;
  color: #1b5e35;
  font-size: 11px;
}
.fav-btn {
  width: 30px; height: 30px;
  padding: 0; font-size: 14px; line-height: 1;
}
.categoria-badge {
  font-size: 10px; font-weight: 700;
  color: #2E8B57;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.btn-success { background-color: #2E8B57 !important; border-color: #2E8B57 !important; }
.btn-success:hover { background-color: #1e6b40 !important; border-color: #1e6b40 !important; }
</style>
