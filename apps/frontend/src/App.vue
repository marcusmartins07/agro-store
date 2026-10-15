<template>
  <div>
    <NotificacoesGlobais />

    <header class="cabecalho sticky-top border-bottom">
      <div class="container app-container d-flex flex-wrap align-items-center gap-2 gap-md-3 py-2 py-md-3">
        <RouterLink :to="{ name: 'produtos' }" class="marca d-inline-flex align-items-center gap-2 flex-shrink-0 rounded-pill">
          <span class="marca-icone rounded-circle d-inline-flex align-items-center justify-content-center">
            <IconeSvg nome="broto" :tamanho="20" />
          </span>
          <span class="fonte-titulo fs-4 fw-semibold marca-texto">Agro Store</span>
        </RouterLink>

        <form class="busca order-last order-md-0" role="search" @submit.prevent="buscar">
          <label for="busca-cabecalho" class="visually-hidden">Buscar produtos</label>
          <div class="position-relative">
            <IconeSvg nome="busca" :tamanho="16" class="busca-icone position-absolute top-50 translate-middle-y text-body-secondary" />
            <input
              id="busca-cabecalho"
              v-model="busca"
              type="search"
              class="form-control rounded-pill busca-campo"
              placeholder="Buscar cenoura, maçã, cuca, lojas..."
            />
          </div>
        </form>

        <nav class="d-flex align-items-center gap-1 ms-auto" aria-label="Acessos rápidos">
          <RouterLink :to="{ name: 'favoritos' }" class="link-acesso position-relative d-inline-flex align-items-center gap-2 rounded-pill">
            <IconeSvg nome="coracao" />
            <span class="rotulo-responsivo">Favoritos</span>
            <span v-if="quantidadeFavoritos > 0" class="contador badge rounded-pill badge-destaque">
              {{ quantidadeFavoritos }}<span class="visually-hidden"> produtos</span>
            </span>
          </RouterLink>

          <RouterLink :to="{ name: 'carrinho' }" class="link-acesso position-relative d-inline-flex align-items-center gap-2 rounded-pill">
            <IconeSvg nome="cesta" />
            <span class="rotulo-responsivo">Carrinho</span>
            <span v-if="carrinhoStore.totalItens > 0" class="contador badge rounded-pill badge-destaque">
              {{ carrinhoStore.totalItens }}<span class="visually-hidden"> itens</span>
            </span>
          </RouterLink>

          <div v-if="authStore.estaLogado" class="dropdown ms-1">
            <button
              class="btn btn-primary rounded-pill d-inline-flex align-items-center gap-2 px-3 dropdown-toggle"
              type="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <IconeSvg nome="usuario" :tamanho="18" />
              <span class="rotulo-conta">Minha conta</span>
            </button>
            <ul class="dropdown-menu dropdown-menu-end rounded-4 sombra-suave p-2 menu-conta">
              <li>
                <RouterLink :to="{ name: 'perfil' }" class="dropdown-item rounded-3 d-flex align-items-center gap-2">
                  <IconeSvg nome="usuario" :tamanho="16" /> Meu perfil
                </RouterLink>
              </li>
              <li v-if="temLoja">
                <RouterLink :to="{ name: 'minha-loja' }" class="dropdown-item rounded-3 d-flex align-items-center gap-2">
                  <IconeSvg nome="loja" :tamanho="16" /> Minha loja
                </RouterLink>
              </li>
              <li>
                <RouterLink :to="{ name: 'pedidos' }" class="dropdown-item rounded-3 d-flex align-items-center gap-2">
                  <IconeSvg nome="recibo" :tamanho="16" /> Meus pedidos
                </RouterLink>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li>
                <button type="button" class="dropdown-item rounded-3 d-flex align-items-center gap-2 text-danger" @click="sair">
                  <IconeSvg nome="sair" :tamanho="16" /> Sair
                </button>
              </li>
            </ul>
          </div>

          <RouterLink v-else :to="{ name: 'login' }" class="btn btn-primary rounded-pill d-inline-flex align-items-center gap-2 px-3 ms-1">
            <IconeSvg nome="usuario" :tamanho="18" />
            <span class="rotulo-conta">Entrar</span>
          </RouterLink>
        </nav>
      </div>
    </header>

    <main class="container app-container py-4">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCarrinhoStore, useFavoritosStore } from '@/stores/index.js'
import { useAuthStore } from '@/stores/auth.js'
import { useProdutorStore } from '@/stores/produtor.js'
import { api } from '@/services/api.js'
import IconeSvg from '@/components/IconeSvg.vue'
import NotificacoesGlobais from '@/components/NotificacoesGlobais.vue'

const router        = useRouter()
const route         = useRoute()
const carrinhoStore = useCarrinhoStore()
const favoritosStore = useFavoritosStore()
const authStore     = useAuthStore()
const produtorStore = useProdutorStore()
const busca         = ref('')
const temLoja       = ref(false)

const quantidadeFavoritos = computed(() => favoritosStore.itens.length)

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
    produtorStore.limpar()
  }
})

watch(() => route.name, (name) => {
  if (authStore.estaLogado && ['perfil', 'minha-loja'].includes(name)) {
    carregarStatusLoja()
  }
})

// Mantém o campo igual ao termo da URL (ex.: ao voltar no histórico ou limpar filtros)
watch(() => route.query.q, (termo) => {
  busca.value = (termo || '').toString()
}, { immediate: true })

function buscar() {
  const termo = busca.value.trim()
  router.push({ name: 'produtos', query: termo ? { q: termo } : {} })
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
  produtorStore.limpar()
  router.push({ name: 'login' })
}
</script>

<style scoped>
.cabecalho {
  background-color: var(--cor-fundo);
  background-color: color-mix(in srgb, var(--cor-fundo) 90%, transparent);
  backdrop-filter: blur(8px);
}
.marca-icone {
  width: 2.25rem;
  height: 2.25rem;
  background-color: var(--cor-primaria);
  color: var(--cor-primaria-texto);
}
.marca-texto {
  color: var(--cor-primaria);
}

/* Celular: busca ocupa a segunda linha inteira; a partir de md fica entre a marca e os acessos */
.busca {
  flex: 1 1 100%;
}
@media (min-width: 768px) {
  .busca {
    flex: 1 1 auto;
  }
}
.busca-campo {
  height: 2.75rem;
  padding-left: 2.75rem;
}
.busca-icone {
  left: 1rem;
}

.link-acesso {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
}
.link-acesso:hover,
.link-acesso.router-link-active {
  background-color: var(--cor-apoio);
}
.menu-conta {
  min-width: 13rem;
}
.contador {
  position: absolute;
  top: -0.125rem;
  right: -0.125rem;
  min-width: 1.25rem;
  font-size: 0.625rem;
}

/* Rótulos escondidos visualmente em telas menores, mas mantidos para leitores de tela */
@media (max-width: 991.98px) {
  .rotulo-responsivo {
    position: absolute;
    width: 1px;
    height: 1px;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
}
@media (max-width: 575.98px) {
  .rotulo-conta {
    position: absolute;
    width: 1px;
    height: 1px;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
}
</style>
