<template>
  <div>
    <!-- Cabeçalho -->
    <div class="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-4">
      <div>
        <h1 class="fw-bold mb-1" style="color: #1b5e35;">Nosso Mercado</h1>
        <p class="text-muted mb-0">Encontre o melhor da produção rural local.</p>
      </div>
      <div class="input-group" style="max-width: 240px;">
        <span class="input-group-text bg-white">🔍</span>
        <input v-model="busca" type="text" class="form-control" placeholder="Pesquisar produtos..." />
      </div>
    </div>

    <!-- ERRO -->
    <div v-if="erro" class="alert alert-danger d-flex align-items-center gap-2" role="alert">
      <span>⚠️</span>
      <div>
        <strong>Não foi possível carregar os produtos.</strong>
        Verifique se o backend está em execução.
        <button class="btn btn-sm btn-outline-danger ms-2" @click="carregarDados">Tentar novamente</button>
      </div>
    </div>

    <div v-else class="row g-3">
      <!-- SIDEBAR -->
      <div class="col-12 col-md-3 col-lg-2">

        <!-- Categorias geradas a partir dos dados da API -->
        <div class="card border mb-3" style="border-color: #d1e7d8 !important; border-radius: 12px;">
          <div class="card-body p-3">
            <p class="fw-bold small mb-2" style="color: #1b5e35;">⊟ Categorias</p>
            <div class="d-grid gap-1">
              <button
                v-for="cat in categorias"
                :key="cat"
                class="btn btn-sm text-start"
                :class="categoriaAtiva === cat ? 'btn-success' : 'btn-light'"
                @click="categoriaAtiva = cat"
              >
                {{ cat }}
              </button>
            </div>
          </div>
        </div>

        <!-- Ordenação -->
        <div class="card border mb-3" style="border-color: #d1e7d8 !important; border-radius: 12px;">
          <div class="card-body p-3">
            <p class="fw-bold small mb-2" style="color: #1b5e35;">↕ Ordenar por</p>
            <div class="d-grid gap-1">
              <button
                v-for="op in opcoesOrdem"
                :key="op.valor"
                class="btn btn-sm text-start"
                :class="ordem === op.valor ? 'btn-success' : 'btn-light'"
                @click="ordem = op.valor"
              >
                {{ op.label }}
              </button>
            </div>
          </div>
        </div>

        <!-- Ofertas -->
        <div class="card border" style="background: #fffde7; border-color: #fde68a !important; border-radius: 12px;">
          <div class="card-body p-3">
            <p class="fw-bold small mb-1" style="color: #856404;">Ofertas do Dia</p>
            <p class="small mb-2" style="color: #92740a;">Assine nossa newsletter e receba ofertas exclusivas.</p>
            <button class="btn btn-success btn-sm w-100">Saber mais</button>
          </div>
        </div>
      </div>

      <!-- GRID -->
      <div class="col-12 col-md-9 col-lg-10">

        <!-- Loading -->
        <div v-if="carregando" class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-3">
          <div class="col" v-for="n in 6" :key="n">
            <div class="card border h-100" style="border-color:#d1e7d8 !important; border-radius:14px;">
              <div class="card-img-top placeholder-glow" style="height:160px; background:#E8F5E9;">
                <span class="placeholder w-100 h-100 d-block" style="background:#c8e6c9;"></span>
              </div>
              <div class="card-body p-3">
                <p class="placeholder-glow mb-2"><span class="placeholder col-4"></span></p>
                <p class="placeholder-glow mb-1"><span class="placeholder col-8"></span></p>
                <p class="placeholder-glow mb-3"><span class="placeholder col-6"></span></p>
                <span class="placeholder col-12 btn btn-success disabled"></span>
              </div>
            </div>
          </div>
        </div>

        <!-- Sem resultados -->
        <div v-else-if="produtosFiltrados.length === 0" class="card border text-center py-5" style="border-color:#d1e7d8 !important; border-radius:14px;">
          <div class="card-body">
            <div class="fs-1 mb-3">🌾</div>
            <p class="text-muted mb-3">Nenhum produto encontrado.</p>
            <button class="btn btn-success" @click="limparFiltros">Limpar filtros</button>
          </div>
        </div>

        <!-- Resultado -->
        <template v-else>
          <p class="text-muted small mb-3">
            {{ produtosFiltrados.length }} produto(s) encontrado(s)
            <span v-if="busca"> para "<strong>{{ busca }}</strong>"</span>
          </p>
          <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-3">
            <div class="col" v-for="produto in produtosFiltrados" :key="produto.produto_id">
              <ProductCard :produto="produto" />
            </div>
          </div>
        </template>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import ProductCard from '@/components/ProductCard.vue'
import { api } from '@/services/api.js'

// ── Estado ──────────────────────────────────────────────────────────────────
const produtos        = ref([])
const categorias      = ref([])
const carregando      = ref(true)
const erro            = ref(false)
const busca           = ref('')
const categoriaAtiva  = ref('Todos')
const ordem           = ref('relevancia')

const opcoesOrdem = [
  { valor: 'relevancia',   label: 'Relevância'   },
  { valor: 'menor-preco',  label: 'Menor preço'  },
  { valor: 'maior-preco',  label: 'Maior preço'  },
  { valor: 'com-desconto', label: 'Com desconto' },
]

// ── Busca da API ─────────────────────────────────────────────────────────────
async function carregarDados() {
  carregando.value = true
  erro.value = false
  try {
    // Busca produtos e categorias em paralelo
    const [listaProdutos, listaCategorias] = await Promise.all([
      api.produtos.listar(),
      api.categorias.listar(),
    ])
    produtos.value   = listaProdutos
    // Adapte "nome" abaixo se o campo da API for diferente (ex: categoria_nome)
    // Filtra ativo=true no frontend enquanto a API ainda retorna todos
    // Quando a API estiver correta, pode remover o .filter()
    categorias.value = ['Todos', ...listaCategorias.filter(c => c.ativo).map(c => c.nome)]
  } catch (e) {
    console.error(e)
    erro.value = true
  } finally {
    carregando.value = false
  }
}

onMounted(carregarDados)

// ── Filtro + Ordenação ───────────────────────────────────────────────────────
const produtosFiltrados = computed(() => {
  let lista = [...produtos.value]

  if (categoriaAtiva.value !== 'Todos') {
    lista = lista.filter(p => p.categoria_nome === categoriaAtiva.value)
  }

  if (busca.value.trim()) {
    const termo = busca.value.toLowerCase()
    lista = lista.filter(p =>
      p.nome.toLowerCase().includes(termo) ||
      p.loja_nome.toLowerCase().includes(termo) ||
      p.categoria_nome.toLowerCase().includes(termo)
    )
  }

  switch (ordem.value) {
    case 'menor-preco':  lista.sort((a, b) => a.preco - b.preco); break
    case 'maior-preco':  lista.sort((a, b) => b.preco - a.preco); break
    case 'com-desconto':
      lista = lista.filter(p => p.desconto > 0)
      lista.sort((a, b) => b.desconto - a.desconto)
      break
  }

  return lista
})

function limparFiltros() {
  busca.value = ''
  categoriaAtiva.value = 'Todos'
  ordem.value = 'relevancia'
}
</script>

<style scoped>
.btn-success { background-color: #2E8B57 !important; border-color: #2E8B57 !important; }
.btn-success:hover { background-color: #1e6b40 !important; border-color: #1e6b40 !important; }
</style>
