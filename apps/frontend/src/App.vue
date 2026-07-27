<template>
  <div>
    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg bg-white border-bottom shadow-sm sticky-top">
      <div class="container">
        <RouterLink to="/" class="navbar-brand d-flex align-items-center gap-2 fw-bold text-success">
          <div class="logo-icon">🌿</div>
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
          <RouterLink to="/" class="btn btn-link text-secondary text-decoration-none d-none d-lg-inline">
            Catálogo
          </RouterLink>

          <RouterLink to="/carrinho" class="btn btn-outline-secondary rounded-circle position-relative p-2 lh-1">
            🛒
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
import { useRouter } from 'vue-router'
import { useCarrinhoStore } from '@/stores/index.js'
import { useAuthStore } from '@/stores/auth.js'

const router        = useRouter()
const carrinhoStore = useCarrinhoStore()
const authStore     = useAuthStore()
const busca         = ref('')

onMounted(() => {
  if (authStore.estaLogado) carrinhoStore.carregar()
})

watch(() => authStore.estaLogado, (estaLogado) => {
  if (estaLogado) {
    carrinhoStore.carregar()
  } else {
    carrinhoStore.limparLocal()
  }
})

function irParaProdutos() {
  router.push({ name: 'produtos', query: { q: busca.value } })
}

function sair() {
  authStore.logout()
  carrinhoStore.limparLocal()
  router.push({ name: 'login' })
}
</script>

<style scoped>
.logo-icon {
  width: 30px; height: 30px;
  background: #2E8B57;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
}
.nav-link.active {
  color: #2E8B57 !important;
  border-bottom: 2px solid #2E8B57;
  font-weight: 600;
}
.nav-link:not(.active) { color: #6b7280; }
.btn-success { background-color: #2E8B57 !important; border-color: #2E8B57 !important; }
.btn-success:hover { background-color: #1e6b40 !important; }
</style>
