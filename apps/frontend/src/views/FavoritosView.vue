<template>
  <section>
    <div class="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-4">
      <div>
        <h1 class="fw-bold mb-1 titulo">Meus Favoritos</h1>
        <p class="text-muted mb-0">Produtos salvos para consultar e comprar depois.</p>
      </div>
      <RouterLink to="/" class="btn btn-outline-success">Ver catálogo</RouterLink>
    </div>

    <div v-if="!authStore.estaLogado" class="card border text-center py-5 painel">
      <div class="card-body">
        <div class="fs-1 mb-3">♡</div>
        <h4 class="fw-bold mb-2 titulo">Entre para ver seus favoritos</h4>
        <p class="text-muted mb-3">Salve produtos para encontrá-los facilmente em sua próxima visita.</p>
        <RouterLink :to="{ name: 'login', query: { retorno: route.fullPath } }" class="btn btn-success">Entrar</RouterLink>
      </div>
    </div>

    <div v-else-if="favoritosStore.carregando" class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-3">
      <div v-for="n in 3" :key="n" class="col">
        <div class="card border h-100 painel placeholder-glow">
          <div class="placeholder w-100 d-block" style="height:160px;"></div>
          <div class="card-body"><span class="placeholder col-8"></span></div>
        </div>
      </div>
    </div>

    <div v-else-if="favoritosStore.erro" class="alert alert-danger" role="alert">
      <strong>Não foi possível carregar os favoritos.</strong> {{ favoritosStore.erro }}
      <button class="btn btn-sm btn-outline-danger ms-2" @click="carregarNovamente">Tentar novamente</button>
    </div>

    <div v-else-if="favoritosStore.ordenados.length === 0" class="card border text-center py-5 painel">
      <div class="card-body">
        <div class="fs-1 mb-3">♡</div>
        <h4 class="fw-bold mb-2 titulo">Nenhum favorito ainda</h4>
        <p class="text-muted mb-3">Use o coração no catálogo para salvar os produtos que mais gostar.</p>
        <RouterLink to="/" class="btn btn-success">Explorar produtos</RouterLink>
      </div>
    </div>

    <div v-else class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-3">
      <div v-for="favorito in favoritosStore.ordenados" :key="favorito.favorito_id" class="col">
        <ProductCard :produto="favorito.dados_produto" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'

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

<style scoped>
.titulo { color: #1b5e35; }
.painel { border-color: #d1e7d8 !important; border-radius: 14px; }
</style>
