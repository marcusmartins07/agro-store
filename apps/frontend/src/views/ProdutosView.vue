<template>
  <div>
    <section class="fundo-destaque rounded-5 p-4 p-md-5 mb-4 mb-md-5" aria-labelledby="titulo-catalogo">
      <p class="text-uppercase small fw-semibold opacity-75 mb-2 sobretitulo">Do campo para sua mesa</p>
      <h1 id="titulo-catalogo" class="fw-semibold mb-3 titulo-banner">Feito com carinho por famílias agricultoras</h1>
      <p class="d-flex align-items-start gap-2 small mb-0">
        <IconeSvg nome="local" :tamanho="18" />
        <span>{{ textoRetirada() }}</span>
      </p>
    </section>

    <div class="d-flex flex-wrap align-items-end justify-content-between gap-2 mb-3">
      <h2 class="h3 fw-semibold mb-0">{{ busca ? `Resultados para "${busca}"` : 'Todos os produtos' }}</h2>
      <span v-if="!carregando && !erro" class="small text-body-secondary">{{ textoQuantidade }}</span>
    </div>

    <div v-if="erro" class="alert alert-danger d-flex flex-wrap align-items-center gap-2" role="alert">
      <span><strong>Não foi possível carregar os produtos.</strong> Verifique se o backend está em execução.</span>
      <button type="button" class="btn btn-sm btn-outline-danger" @click="carregarDados">Tentar novamente</button>
    </div>

    <template v-else>
      <div class="d-flex flex-column flex-md-row align-items-md-center justify-content-between gap-3 mb-4">
        <div class="d-flex gap-2 overflow-x-auto pb-1" role="group" aria-label="Filtrar por categoria">
          <button
            v-for="categoria in categorias"
            :key="categoria"
            type="button"
            class="btn btn-sm rounded-pill px-3 flex-shrink-0"
            :class="categoria === categoriaAtiva ? 'btn-primary' : 'btn-outline-secondary'"
            :aria-pressed="categoria === categoriaAtiva"
            @click="selecionarCategoria(categoria)"
          >
            {{ categoria }}
          </button>
        </div>

        <div class="d-flex align-items-center gap-2 flex-shrink-0">
          <label for="ordem-produtos" class="small text-body-secondary text-nowrap">Ordenar por</label>
          <select
            id="ordem-produtos"
            class="form-select form-select-sm rounded-pill"
            :value="ordem"
            @change="selecionarOrdem($event.target.value)"
          >
            <option v-for="opcao in opcoesOrdem" :key="opcao.valor" :value="opcao.valor">{{ opcao.rotulo }}</option>
          </select>
        </div>
      </div>

      <div v-if="carregando" class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-4">
        <span class="visually-hidden" role="status">Carregando produtos...</span>
        <div v-for="n in 6" :key="n" class="col" aria-hidden="true">
          <div class="card h-100 rounded-4 overflow-hidden placeholder-glow">
            <div class="ratio ratio-1x1"><span class="placeholder"></span></div>
            <div class="card-body p-3 p-lg-4">
              <span class="placeholder col-4 d-block mb-2"></span>
              <span class="placeholder col-8 d-block mb-2"></span>
              <span class="placeholder col-6 d-block"></span>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="produtosFiltrados.length === 0" class="card rounded-4 text-center py-5">
        <div class="card-body">
          <IconeSvg nome="busca" :tamanho="40" class="text-body-secondary mb-3" />
          <p class="text-body-secondary mb-3">Nenhum produto encontrado.</p>
          <button type="button" class="btn btn-primary rounded-pill px-4" @click="limparFiltros">Limpar filtros</button>
        </div>
      </div>

      <template v-else>
        <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-4">
          <div v-for="produto in produtosDaPagina" :key="produto.produto_id" class="col">
            <ProductCard :produto="produto" />
          </div>
        </div>

        <!-- O RouterLink ignora a query ao marcar o link ativo; por isso aria-current é sempre definido aqui -->
        <nav v-if="totalPaginas > 1" class="mt-5" aria-label="Páginas do catálogo">
          <ul class="pagination justify-content-center flex-wrap gap-2 mb-0 paginacao">
            <li class="page-item" :class="{ disabled: paginaAtual === 1 }">
              <RouterLink v-if="paginaAtual > 1" :to="rotaDaPagina(paginaAtual - 1)" class="page-link" :aria-current="null">
                <IconeSvg nome="seta-esquerda" :tamanho="16" />
                <span class="visually-hidden">Página anterior</span>
              </RouterLink>
              <span v-else class="page-link">
                <IconeSvg nome="seta-esquerda" :tamanho="16" />
                <span class="visually-hidden">Página anterior</span>
              </span>
            </li>

            <li v-for="pagina in totalPaginas" :key="pagina" class="page-item" :class="{ active: pagina === paginaAtual }">
              <RouterLink
                :to="rotaDaPagina(pagina)"
                class="page-link"
                :aria-current="pagina === paginaAtual ? 'page' : null"
              >
                {{ pagina }}
              </RouterLink>
            </li>

            <li class="page-item" :class="{ disabled: paginaAtual === totalPaginas }">
              <RouterLink v-if="paginaAtual < totalPaginas" :to="rotaDaPagina(paginaAtual + 1)" class="page-link" :aria-current="null">
                <IconeSvg nome="seta-direita" :tamanho="16" />
                <span class="visually-hidden">Próxima página</span>
              </RouterLink>
              <span v-else class="page-link">
                <IconeSvg nome="seta-direita" :tamanho="16" />
                <span class="visually-hidden">Próxima página</span>
              </span>
            </li>
          </ul>
        </nav>
      </template>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import IconeSvg from '@/components/IconeSvg.vue'
import ProductCard from '@/components/ProductCard.vue'
import { textoRetirada } from '@/data/feira.js'
import { api } from '@/services/api.js'

const POR_PAGINA = 9
const CATEGORIA_TODAS = 'Todos'
const ORDEM_PADRAO = 'relevancia'

const opcoesOrdem = [
  { valor: 'relevancia',   rotulo: 'Relevância'   },
  { valor: 'menor-preco',  rotulo: 'Menor preço'  },
  { valor: 'maior-preco',  rotulo: 'Maior preço'  },
  { valor: 'com-desconto', rotulo: 'Com desconto' },
]

const route  = useRoute()
const router = useRouter()

// ── Estado ──────────────────────────────────────────────────────────────────
const produtos   = ref([])
const categorias = ref([CATEGORIA_TODAS])
const carregando = ref(true)
const erro       = ref(false)

// Busca, filtros e página ficam na URL (/?q=&categoria=&ordem=&pagina=)
// para que o catálogo volte igual depois de abrir o detalhe de um produto
const busca = computed(() => textoDaConsulta(route.query.q).trim())
const categoriaAtiva = computed(() => textoDaConsulta(route.query.categoria) || CATEGORIA_TODAS)
const ordem = computed(() => {
  const valor = textoDaConsulta(route.query.ordem)
  return opcoesOrdem.some(opcao => opcao.valor === valor) ? valor : ORDEM_PADRAO
})
const paginaSolicitada = computed(() => {
  const pagina = Number.parseInt(textoDaConsulta(route.query.pagina), 10)
  return pagina > 0 ? pagina : 1
})

// ── Filtro, ordenação e paginação ───────────────────────────────────────────
const produtosFiltrados = computed(() => {
  let lista = [...produtos.value]

  if (categoriaAtiva.value !== CATEGORIA_TODAS) {
    lista = lista.filter(p => p.categoria_nome === categoriaAtiva.value)
  }

  if (busca.value) {
    const termo = busca.value.toLowerCase()
    lista = lista.filter(p =>
      [p.nome, p.descricao, p.loja_nome, p.categoria_nome].some(campo => (campo || '').toLowerCase().includes(termo))
    )
  }

  switch (ordem.value) {
    case 'menor-preco':  lista.sort((a, b) => Number(a.preco) - Number(b.preco)); break
    case 'maior-preco':  lista.sort((a, b) => Number(b.preco) - Number(a.preco)); break
    case 'com-desconto':
      lista = lista.filter(p => Number(p.desconto) > 0)
      lista.sort((a, b) => Number(b.desconto) - Number(a.desconto))
      break
  }

  return lista
})

const totalPaginas = computed(() => Math.max(1, Math.ceil(produtosFiltrados.value.length / POR_PAGINA)))
const paginaAtual = computed(() => Math.min(paginaSolicitada.value, totalPaginas.value))

const produtosDaPagina = computed(() => {
  const inicio = (paginaAtual.value - 1) * POR_PAGINA
  return produtosFiltrados.value.slice(inicio, inicio + POR_PAGINA)
})

const textoQuantidade = computed(() => {
  const total = produtosFiltrados.value.length
  return total === 1 ? '1 produto' : `${total} produtos`
})

onMounted(carregarDados)

// ── Busca da API ─────────────────────────────────────────────────────────────
async function carregarDados() {
  carregando.value = true
  erro.value = false
  try {
    const [listaProdutos, listaCategorias] = await Promise.all([
      api.produtos.listar(),
      api.categorias.listar(),
    ])
    produtos.value   = listaProdutos
    categorias.value = [CATEGORIA_TODAS, ...listaCategorias.filter(c => c.ativo).map(c => c.nome)]
  } catch (e) {
    console.error(e)
    erro.value = true
  } finally {
    carregando.value = false
  }
}

// ── Navegação pela URL ───────────────────────────────────────────────────────
function textoDaConsulta(valor) {
  if (Array.isArray(valor)) return valor[0] || ''
  return (valor || '').toString()
}

// Remove da URL os parâmetros vazios ou com valor padrão
function montarConsulta(alteracoes) {
  const consulta = { ...route.query, ...alteracoes }
  if (!consulta.q) delete consulta.q
  if (!consulta.categoria || consulta.categoria === CATEGORIA_TODAS) delete consulta.categoria
  if (!consulta.ordem || consulta.ordem === ORDEM_PADRAO) delete consulta.ordem
  if (!(Number(consulta.pagina) > 1)) delete consulta.pagina
  return consulta
}

function rotaDaPagina(pagina) {
  return { name: 'produtos', query: montarConsulta({ pagina }) }
}

function selecionarCategoria(categoria) {
  router.replace({ name: 'produtos', query: montarConsulta({ categoria, pagina: undefined }) })
}

function selecionarOrdem(valor) {
  router.replace({ name: 'produtos', query: montarConsulta({ ordem: valor, pagina: undefined }) })
}

function limparFiltros() {
  router.push({ name: 'produtos' })
}
</script>

<style scoped>
.sobretitulo {
  letter-spacing: 0.12em;
}
.titulo-banner {
  font-size: clamp(1.875rem, 4vw, 3rem);
  max-width: 40rem;
}
.paginacao .page-link {
  min-width: 2.5rem;
  height: 2.5rem;
  margin-left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50rem;
}
</style>
