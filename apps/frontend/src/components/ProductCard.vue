<template>
  <article class="card h-100 rounded-4 overflow-hidden sombra-suave card-produto">
    <RouterLink :to="{ name: 'produto', params: { id: produto.produto_id } }" class="d-flex flex-column h-100 text-reset link-produto">
      <div class="ratio ratio-1x1 imagem-produto">
        <img v-if="produto.imagem" :src="produto.imagem" :alt="produto.nome" class="object-fit-cover" loading="lazy">
        <div v-else class="imagem-placeholder">
          <IconeSvg nome="imagem" :tamanho="40" />
          <span class="small">Sem foto</span>
        </div>
      </div>

      <span v-if="temDesconto(produto)" class="badge rounded-pill badge-destaque position-absolute top-0 start-0 m-3 badge-desconto">
        -{{ produto.desconto }}%
      </span>

      <div class="card-body d-flex flex-column gap-2 p-3 p-lg-4">
        <p class="loja-nome text-uppercase text-body-secondary mb-0">{{ produto.loja_nome }}</p>
        <h3 class="h5 fw-semibold lh-sm mb-0">{{ produto.nome }}</h3>
        <p v-if="produto.descricao" class="small text-body-secondary mb-0 descricao">{{ produto.descricao }}</p>
        <p v-if="!podeComprar" class="small fw-semibold text-warning-emphasis mb-0">{{ mensagemIndisponibilidade }}</p>

        <div class="d-flex align-items-baseline flex-wrap gap-2 mt-auto pt-1">
          <span class="fs-5 fw-bold text-primary">{{ formatarPreco(produto.preco) }}</span>
          <span v-if="temDesconto(produto)" class="small text-body-secondary text-decoration-line-through">
            <span class="visually-hidden">Preço sem desconto:</span>
            {{ formatarPreco(produto.preco_original) }}
          </span>
        </div>
      </div>
    </RouterLink>

    <button
      type="button"
      class="btn rounded-circle position-absolute top-0 end-0 m-3 botao-favorito"
      :disabled="botaoFavoritoDesabilitado"
      :aria-label="textoAcaoFavorito"
      :title="textoAcaoFavorito"
      @click="alternarFavorito"
    >
      <IconeSvg nome="coracao" :tamanho="18" :preenchido="favorito" :class="{ 'coracao-ativo': favorito }" />
    </button>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import IconeSvg from '@/components/IconeSvg.vue'
import { useFavoritosStore } from '@/stores/index.js'
import { useAuthStore } from '@/stores/auth.js'
import { useNotificacoesStore } from '@/stores/notificacoes.js'
import { formatarPreco, temDesconto } from '@/utils/formatacao.js'

const props = defineProps({
  produto: { type: Object, required: true },
})

const route = useRoute()
const router = useRouter()
const favoritosStore = useFavoritosStore()
const authStore = useAuthStore()
const notificacoesStore = useNotificacoesStore()

const favorito = computed(() => favoritosStore.isFavorito(props.produto.produto_id))

const podeComprar = computed(() =>
  props.produto.disponivel !== false && props.produto.ativo !== false && Number(props.produto.estoque || 0) > 0
)

const mensagemIndisponibilidade = computed(() => {
  if (props.produto.ativo === false) return 'Produto inativo'
  if (Number(props.produto.estoque || 0) <= 0) return 'Sem estoque'
  return 'Produto indisponível'
})

const botaoFavoritoDesabilitado = computed(() =>
  authStore.estaLogado && (favoritosStore.carregando || favoritosStore.isOperando(props.produto.produto_id))
)

const textoAcaoFavorito = computed(() => {
  if (!authStore.estaLogado) return 'Entrar para favoritar'
  if (favoritosStore.isOperando(props.produto.produto_id)) return 'Atualizando favorito'
  return favorito.value ? 'Remover dos favoritos' : 'Adicionar aos favoritos'
})

async function alternarFavorito() {
  if (!authStore.estaLogado) {
    router.push({ name: 'login', query: { retorno: route.fullPath } })
    return
  }

  const jaFavorito = favorito.value
  try {
    await favoritosStore.alternar(props.produto.produto_id)
    notificacoesStore.notificar({
      tipo: 'success',
      mensagem: jaFavorito ? 'Produto removido dos favoritos.' : 'Produto adicionado aos favoritos.',
      tempo: 4,
    })
  } catch (e) {
    notificacoesStore.notificar({ tipo: 'danger', mensagem: favoritosStore.erro })
  }
}
</script>

<style scoped>
.card-produto {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card-produto:hover {
  transform: translateY(-4px);
  box-shadow: var(--sombra-elevada);
}
.imagem-produto {
  background-color: var(--cor-neutra);
}
.imagem-produto img {
  transition: transform 0.5s ease;
}
.card-produto:hover .imagem-produto img {
  transform: scale(1.05);
}
.link-produto:focus-visible {
  outline-offset: -3px;
}
.badge-desconto {
  font-size: 0.75rem;
}
.loja-nome {
  font-size: 0.75rem;
  letter-spacing: 0.05em;
}
.descricao {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.botao-favorito {
  width: 2.25rem;
  height: 2.25rem;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 0;
  background-color: var(--cor-superficie);
  box-shadow: var(--sombra-suave);
  transition: transform 0.15s ease;
}
.botao-favorito:hover:not(:disabled) {
  transform: scale(1.1);
  background-color: var(--cor-superficie);
}
.coracao-ativo {
  color: var(--cor-destaque);
}

@media (prefers-reduced-motion: reduce) {
  .card-produto,
  .imagem-produto img,
  .botao-favorito {
    transition: none;
  }
  .card-produto:hover,
  .card-produto:hover .imagem-produto img {
    transform: none;
  }
}
</style>
