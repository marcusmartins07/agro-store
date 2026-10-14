<template>
  <div>
    <div v-if="carregando" class="row g-4">
      <span class="visually-hidden" role="status">Carregando produto...</span>
      <div class="col-12 col-md-6" aria-hidden="true">
        <div class="ratio ratio-1x1 rounded-5 overflow-hidden placeholder-glow"><span class="placeholder"></span></div>
      </div>
      <div class="col-12 col-md-6 placeholder-glow" aria-hidden="true">
        <span class="placeholder col-4 d-block mb-3"></span>
        <span class="placeholder placeholder-lg col-10 d-block mb-3"></span>
        <span class="placeholder col-6 d-block mb-4"></span>
        <span class="placeholder col-12 d-block rounded-4 caixa-preco-placeholder"></span>
      </div>
    </div>

    <div v-else-if="naoEncontrado" class="card rounded-4 text-center py-5">
      <div class="card-body">
        <IconeSvg nome="busca" :tamanho="40" class="text-body-secondary mb-3" />
        <h1 class="h3 fw-semibold mb-2">Produto não encontrado ou indisponível</h1>
        <p class="text-body-secondary mb-3">O produto pode ter sido retirado do catálogo ou a loja pode estar inativa.</p>
        <RouterLink :to="{ name: 'produtos' }" class="btn btn-primary rounded-pill px-4">Voltar ao catálogo</RouterLink>
      </div>
    </div>

    <div v-else-if="erro" class="alert alert-danger d-flex flex-wrap align-items-center gap-2" role="alert">
      <span><strong>Não foi possível carregar o produto.</strong> Verifique se o backend está em execução.</span>
      <button type="button" class="btn btn-sm btn-outline-danger" @click="carregarPagina">Tentar novamente</button>
    </div>

    <template v-else-if="produto">
      <nav aria-label="Navegação estrutural" class="mb-3">
        <ol class="breadcrumb small mb-0">
          <li class="breadcrumb-item"><RouterLink :to="{ name: 'produtos' }" class="link-primary">Catálogo</RouterLink></li>
          <li class="breadcrumb-item active" aria-current="page">{{ produto.nome }}</li>
        </ol>
      </nav>

      <div class="row g-4">
        <div class="col-12 col-md-6">
          <GaleriaProduto :slides="galeria" :nome-produto="produto.nome" />
        </div>

        <div class="col-12 col-md-6 d-flex flex-column gap-4">
          <div>
            <p class="d-flex align-items-center gap-2 small text-body-secondary mb-2">
              <IconeSvg nome="loja" :tamanho="16" />
              <span><span class="visually-hidden">Loja:</span> {{ produto.loja_nome }}</span>
            </p>
            <h1 class="fw-semibold mb-2 titulo-produto">{{ produto.nome }}</h1>
            <RouterLink
              v-if="!carregandoAvaliacoes && !erroAvaliacoes"
              :to="{ hash: '#avaliacoes' }"
              class="d-inline-flex align-items-center gap-2 small text-reset"
            >
              <AvaliacaoEstrelas :nota="mediaAvaliacoes" />
              <span class="text-body-secondary">{{ textoResumoAvaliacoes }}</span>
            </RouterLink>
          </div>

          <div class="bg-apoio rounded-4 p-4">
            <div v-if="temDesconto(produto)" class="d-flex align-items-center gap-2 small mb-1">
              <span class="text-body-secondary text-decoration-line-through">
                <span class="visually-hidden">Preço sem desconto:</span>
                {{ formatarPreco(produto.preco_original) }}
              </span>
              <span class="badge rounded-pill badge-destaque">-{{ produto.desconto }}%</span>
            </div>
            <p class="fw-bold text-primary mb-0 preco-destaque">
              <span class="visually-hidden">Preço:</span>
              {{ formatarPreco(produto.preco) }}
            </p>
            <p class="small fw-semibold mt-2 mb-0" :class="podeComprar ? 'text-success-emphasis' : 'text-warning-emphasis'">
              {{ textoDisponibilidade }}
            </p>
          </div>

          <div class="d-flex flex-wrap align-items-center gap-3">
            <SeletorQuantidade
              v-model="quantidade"
              :max="estoqueDisponivel"
              :disabled="!podeComprar || adicionando"
              :rotulo="produto.nome"
            />
            <button
              type="button"
              class="btn btn-primary btn-lg rounded-pill flex-grow-1 d-inline-flex align-items-center justify-content-center gap-2"
              :disabled="!podeComprar || adicionando"
              @click="adicionarAoCarrinho"
            >
              <span v-if="adicionando" class="spinner-border spinner-border-sm" aria-hidden="true"></span>
              <IconeSvg v-else nome="cesta" />
              {{ adicionando ? 'Adicionando...' : 'Adicionar ao carrinho' }}
            </button>
            <button
              type="button"
              class="btn btn-outline-secondary btn-lg rounded-pill d-inline-flex align-items-center gap-2"
              :disabled="favoritoDesabilitado"
              @click="alternarFavorito"
            >
              <IconeSvg nome="coracao" :preenchido="favorito" :class="{ 'coracao-ativo': favorito }" />
              {{ favorito ? 'Favoritado' : 'Favoritar' }}
            </button>
          </div>

          <p class="d-flex align-items-start gap-2 small text-body-secondary mb-0">
            <IconeSvg nome="local" :tamanho="16" />
            <span>{{ textoRetirada() }}</span>
          </p>

          <section aria-labelledby="titulo-descricao">
            <h2 id="titulo-descricao" class="h4 fw-semibold mb-2">Descrição</h2>
            <p class="text-body-secondary mb-0 descricao">
              {{ produto.descricao || 'O produtor ainda não cadastrou uma descrição para este produto.' }}
            </p>
          </section>
        </div>
      </div>

      <section id="avaliacoes" class="mt-5 pt-lg-3" aria-labelledby="titulo-avaliacoes">
        <h2 id="titulo-avaliacoes" class="h3 fw-semibold mb-3">Avaliações</h2>

        <p v-if="carregandoAvaliacoes" class="small text-body-secondary mb-0" role="status">Carregando avaliações...</p>

        <div v-else-if="erroAvaliacoes" class="alert alert-warning d-flex flex-wrap align-items-center gap-2" role="alert">
          <span>Não foi possível carregar as avaliações deste produto.</span>
          <button type="button" class="btn btn-sm btn-outline-secondary" @click="carregarAvaliacoes">Tentar novamente</button>
        </div>

        <div v-else-if="avaliacoes.length === 0" class="card rounded-4">
          <div class="card-body text-body-secondary">Este produto ainda não possui avaliações.</div>
        </div>

        <div v-else class="row row-cols-1 row-cols-md-3 g-3">
          <div v-for="avaliacao in avaliacoes" :key="avaliacao.avaliacao_id" class="col">
            <article class="card h-100 rounded-4">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center gap-2 mb-2">
                  <p class="fw-semibold mb-0">{{ nomeAvaliador(avaliacao.usuario_nome) }}</p>
                  <AvaliacaoEstrelas :nota="Number(avaliacao.nota)" />
                </div>
                <p class="small text-body-secondary mb-0">{{ avaliacao.comentario || 'Avaliação sem comentário.' }}</p>
              </div>
            </article>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import AvaliacaoEstrelas from '@/components/AvaliacaoEstrelas.vue'
import GaleriaProduto from '@/components/GaleriaProduto.vue'
import IconeSvg from '@/components/IconeSvg.vue'
import SeletorQuantidade from '@/components/SeletorQuantidade.vue'
import { textoRetirada } from '@/data/feira.js'
import { montarGaleriaProduto } from '@/data/mockGaleria.js'
import { api } from '@/services/api.js'
import { useAuthStore } from '@/stores/auth.js'
import { useCarrinhoStore, useFavoritosStore } from '@/stores/index.js'
import { useNotificacoesStore } from '@/stores/notificacoes.js'
import { formatarPreco, temDesconto } from '@/utils/formatacao.js'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const carrinhoStore = useCarrinhoStore()
const favoritosStore = useFavoritosStore()
const notificacoesStore = useNotificacoesStore()

// ── Estado ──────────────────────────────────────────────────────────────────
const produto = ref(null)
const carregando = ref(true)
const erro = ref(false)
const naoEncontrado = ref(false)
const avaliacoes = ref([])
const carregandoAvaliacoes = ref(true)
const erroAvaliacoes = ref(false)
const quantidade = ref(1)
const adicionando = ref(false)

// ── Produto ──────────────────────────────────────────────────────────────────
const produtoId = computed(() => route.params.id)
const galeria = computed(() => (produto.value ? montarGaleriaProduto(produto.value) : []))
const estoqueDisponivel = computed(() => Math.max(1, Number(produto.value?.estoque || 0)))

const podeComprar = computed(() =>
  Boolean(produto.value)
  && produto.value.ativo !== false
  && produto.value.preco !== null
  && Number(produto.value.estoque || 0) > 0
)

const textoDisponibilidade = computed(() => {
  if (podeComprar.value) return `Disponível: ${produto.value.estoque} em estoque`
  if (produto.value?.ativo === false) return 'Produto inativo'
  if (produto.value?.preco === null) return 'Preço indisponível no momento'
  return 'Sem estoque'
})

const favorito = computed(() => Boolean(produto.value) && favoritosStore.isFavorito(produto.value.produto_id))

const favoritoDesabilitado = computed(() =>
  authStore.estaLogado && (favoritosStore.carregando || favoritosStore.isOperando(produto.value?.produto_id))
)

// ── Avaliações ───────────────────────────────────────────────────────────────
// Média calculada só para exibição; as notas vêm do backend
const mediaAvaliacoes = computed(() => {
  if (avaliacoes.value.length === 0) return 0
  const soma = avaliacoes.value.reduce((total, avaliacao) => total + Number(avaliacao.nota || 0), 0)
  return soma / avaliacoes.value.length
})

const textoResumoAvaliacoes = computed(() => {
  const total = avaliacoes.value.length
  if (total === 0) return 'Sem avaliações'
  const media = mediaAvaliacoes.value.toLocaleString('pt-BR', { maximumFractionDigits: 1 })
  return `${media} (${total} ${total === 1 ? 'avaliação' : 'avaliações'})`
})

// O watcher também roda ao sair da tela; só carrega enquanto a rota for a de produto
watch(produtoId, () => {
  if (route.name === 'produto') carregarPagina()
}, { immediate: true })

function carregarPagina() {
  quantidade.value = 1
  carregarProduto()
  carregarAvaliacoes()
}

// As respostas de um produto anterior são descartadas se o usuário já navegou para outro
async function carregarProduto() {
  const id = produtoId.value
  carregando.value = true
  erro.value = false
  naoEncontrado.value = false
  try {
    const dados = await api.produtos.obter(id)
    if (id === produtoId.value) produto.value = dados
  } catch (e) {
    if (id !== produtoId.value) return
    produto.value = null
    if (e?.status === 404) {
      naoEncontrado.value = true
    } else {
      console.error(e)
      erro.value = true
    }
  } finally {
    if (id === produtoId.value) carregando.value = false
  }
}

async function carregarAvaliacoes() {
  const id = produtoId.value
  carregandoAvaliacoes.value = true
  erroAvaliacoes.value = false
  try {
    const dados = await api.avaliacoes.listarPorProduto(id)
    if (id === produtoId.value) avaliacoes.value = dados
  } catch (e) {
    if (id !== produtoId.value) return
    console.error(e)
    avaliacoes.value = []
    erroAvaliacoes.value = true
  } finally {
    if (id === produtoId.value) carregandoAvaliacoes.value = false
  }
}

// ── Ações ────────────────────────────────────────────────────────────────────
function redirecionarParaLogin() {
  router.push({ name: 'login', query: { retorno: route.fullPath } })
}

async function adicionarAoCarrinho() {
  if (!authStore.estaLogado) {
    redirecionarParaLogin()
    return
  }

  adicionando.value = true
  try {
    await carrinhoStore.adicionar(produto.value.produto_id, quantidade.value)
    notificacoesStore.notificar({ tipo: 'success', mensagem: 'Produto adicionado ao carrinho.', tempo: 4 })
    quantidade.value = 1
  } catch (e) {
    notificacoesStore.notificar({ tipo: 'danger', mensagem: carrinhoStore.erro })
  } finally {
    adicionando.value = false
  }
}

async function alternarFavorito() {
  if (!authStore.estaLogado) {
    redirecionarParaLogin()
    return
  }

  const jaFavorito = favorito.value
  try {
    await favoritosStore.alternar(produto.value.produto_id)
    notificacoesStore.notificar({
      tipo: 'success',
      mensagem: jaFavorito ? 'Produto removido dos favoritos.' : 'Produto adicionado aos favoritos.',
      tempo: 4,
    })
  } catch (e) {
    notificacoesStore.notificar({ tipo: 'danger', mensagem: favoritosStore.erro })
  }
}

// Exibe o primeiro nome e a inicial do último sobrenome para não expor o nome completo do cliente
function nomeAvaliador(nomeCompleto) {
  const partes = (nomeCompleto || '').trim().split(/\s+/).filter(Boolean)
  if (partes.length === 0) return 'Cliente'
  if (partes.length === 1) return partes[0]
  return `${partes[0]} ${partes[partes.length - 1][0]}.`
}
</script>

<style scoped>
.titulo-produto {
  font-size: clamp(2rem, 4vw, 2.5rem);
}
.preco-destaque {
  font-size: 2.25rem;
  line-height: 1.2;
}
.descricao {
  white-space: pre-line;
  line-height: 1.7;
}
.caixa-preco-placeholder {
  height: 7rem;
}
.coracao-ativo {
  color: var(--cor-destaque);
}
</style>
