<template>
  <div>
    <NotificacoesGlobais />
    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg bg-white border-bottom shadow-sm sticky-top">
      <div class="container">
        <RouterLink to="/" class="navbar-brand d-flex align-items-center gap-2 fw-bold text-success">
          Agro Store
        </RouterLink>

        <div class="d-none d-md-flex flex-grow-1 mx-4">
          <div class="input-group">
            <span class="input-group-text bg-light border-end-0 text-muted">🔍</span>
            <input
              v-model="busca"
              @keyup.enter="irParaProdutos"
              type="text"
              class="form-control bg-light border-start-0"
              placeholder="O que você está procurando?"
            />
          </div>
        </div>

        <div class="d-flex align-items-center gap-2">
          <RouterLink to="/carrinho" class="btn btn-outline-secondary rounded-circle position-relative p-2 lh-1">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16" aria-hidden="true">
              <path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .49.598l-1 5a.5.5 0 0 1-.465.401l-9.397.472L4.415 11H13a.5.5 0 0 1 0 1H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5M3.102 4l.84 4.479 9.144-.459L13.89 4zM5 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4m7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4m-7 1a1 1 0 1 1 0 2 1 1 0 0 1 0-2m7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2" />
            </svg>
            <span class="visually-hidden">Carrinho</span>
            <span
              v-if="carrinhoStore.totalItens > 0"
              class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-success"
              style="font-size: 10px;"
            >
              {{ carrinhoStore.totalItens }}
            </span>
          </RouterLink>

          <!-- Logado -->
          <div v-if="authStore.estaLogado" class="dropdown">
            <button
              class="btn btn-success rounded-pill px-3 dropdown-toggle"
              data-bs-toggle="dropdown"
            >
              👤 Minha Conta
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><RouterLink to="/cliente" class="dropdown-item">Meu Perfil</RouterLink></li>
              <li v-if="temLoja"><RouterLink :to="{ name: 'minha-loja' }" class="dropdown-item">Minha Loja</RouterLink></li>
              <li><RouterLink to="/pedidos" class="dropdown-item">Meus Pedidos</RouterLink></li>
              <li><RouterLink to="/favoritos" class="dropdown-item">Favoritos</RouterLink></li>
              <li><hr class="dropdown-divider"></li>
              <li>
                <button class="dropdown-item text-danger" @click="sair">Sair</button>
              </li>
            </ul>
          </div>

          <!-- Deslogado -->
          <RouterLink v-else to="/login" class="btn btn-success rounded-pill px-3">
            👤 Login
          </RouterLink>
        </div>
      </div>
    </nav>

    <!-- CONTEÚDO -->
    <main class="container py-4">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCarrinhoStore, useFavoritosStore } from '@/stores/index.js'
import { useAuthStore } from '@/stores/auth.js'
import { api } from '@/services/api.js'
import NotificacoesGlobais from '@/components/NotificacoesGlobais.vue'

const router        = useRouter()
const route         = useRoute()
const carrinhoStore = useCarrinhoStore()
const favoritosStore = useFavoritosStore()
const authStore     = useAuthStore()
const busca         = ref('')
const temLoja       = ref(false)

onMounted(() => {
  if (authStore.estaLogado) {
    carrinhoStore.carregar()
    favoritosStore.carregar()
    carregarStatusLoja()
  }
})

watch(() => authStore.estaLogado, (estaLogado) => {
  if (estaLogado) {
    carrinhoStore.carregar()
    favoritosStore.carregar()
    carregarStatusLoja()
  } else {
    temLoja.value = false
    carrinhoStore.limparLocal()
    favoritosStore.limparLocal()
  }
})

watch(() => route.name, (name) => {
  if (authStore.estaLogado && ['cliente', 'minha-loja'].includes(name)) {
    carregarStatusLoja()
  }
})

function irParaProdutos() {
  router.push({ name: 'produtos', query: { q: busca.value } })
}

async function carregarStatusLoja() {
  try {
    const usuario = await api.usuarios.me()
    temLoja.value = !!usuario.tem_loja
  } catch (e) {
    temLoja.value = false
    console.error(e)
  }
}

function sair() {
  authStore.logout()
  temLoja.value = false
  carrinhoStore.limparLocal()
  favoritosStore.limparLocal()
  router.push({ name: 'login' })
}
</script>

<style scoped>
.nav-link.active {
  color: #2E8B57 !important;
  border-bottom: 2px solid #2E8B57;
  font-weight: 600;
}
.nav-link:not(.active) { color: #6b7280; }
.btn-success { background-color: #2E8B57 !important; border-color: #2E8B57 !important; }
.btn-success:hover { background-color: #1e6b40 !important; }
</style>
