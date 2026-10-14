<template>
  <section>
    <div class="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-4">
      <div>
        <h1 class="fw-semibold mb-1">Favoritos</h1>
        <p class="text-body-secondary mb-0">Produtos salvos para consultar e comprar depois.</p>
      </div>
      <RouterLink :to="{ name: 'produtos' }" class="btn btn-outline-primary rounded-pill px-4">Ver catálogo</RouterLink>
    </div>

    <div v-if="!authStore.estaLogado" class="card rounded-4 text-center py-5">
      <div class="card-body">
        <span class="icone-estado mb-3"><IconeSvg nome="coracao" :tamanho="32" /></span>
        <h2 class="h4 fw-semibold mb-2">Entre para ver seus favoritos</h2>
        <p class="text-body-secondary mb-3">Salve produtos para encontrá-los facilmente em sua próxima visita.</p>
        <RouterLink :to="{ name: 'login', query: { retorno: route.fullPath } }" class="btn btn-primary rounded-pill px-4">Entrar</RouterLink>
      </div>
    </div>

    <div v-else-if="favoritosStore.carregando" class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-4">
      <span class="visually-hidden" role="status">Carregando favoritos...</span>
      <div v-for="n in 3" :key="n" class="col" aria-hidden="true">
        <div class="card h-100 rounded-4 overflow-hidden placeholder-glow">
          <div class="ratio ratio-1x1"><span class="placeholder"></span></div>
          <div class="card-body p-3 p-lg-4"><span class="placeholder col-8 d-block"></span></div>
        </div>
      </div>
    </div>

    <div v-else-if="favoritosStore.erro" class="alert alert-danger d-flex flex-wrap align-items-center gap-2" role="alert">
      <span><strong>Não foi possível carregar os favoritos.</strong> {{ favoritosStore.erro }}</span>
      <button type="button" class="btn btn-sm btn-outline-danger" @click="carregarNovamente">Tentar novamente</button>
    </div>

    <div v-else-if="favoritosStore.ordenados.length === 0" class="card rounded-4 text-center py-5">
      <div class="card-body">
        <span class="icone-estado mb-3"><IconeSvg nome="coracao" :tamanho="32" /></span>
        <h2 class="h4 fw-semibold mb-2">Nenhum favorito ainda</h2>
        <p class="text-body-secondary mb-3">Use o coração no catálogo para salvar os produtos de que mais gostar.</p>
        <RouterLink :to="{ name: 'produtos' }" class="btn btn-primary rounded-pill px-4">Explorar produtos</RouterLink>
      </div>
    </div>

    <template v-else>
      <h2 class="visually-hidden">Produtos favoritados</h2>
      <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-4">
        <div v-for="favorito in favoritosStore.ordenados" :key="favorito.favorito_id" class="col">
          <ProductCard :produto="favorito.dados_produto" />
        </div>
      </div>
    </template>
  </section>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'

import IconeSvg from '@/components/IconeSvg.vue'
import ProductCard from '@/components/ProductCard.vue'
import { useAuthStore } from '@/stores/auth.js'
import { useFavoritosStore } from '@/stores/index.js'

const route = useRoute()
const authStore = useAuthStore()
const favoritosStore = useFavoritosStore()

onMounted(() => {
  if (authStore.estaLogado) favoritosStore.carregar()
})

function carregarNovamente() {
  favoritosStore.carregar(true)
}
</script>
