import { createRouter, createWebHistory } from 'vue-router'
import ProdutosView    from '@/views/ProdutosView.vue'
import CarrinhoView    from '@/views/CarrinhoView.vue'
import FavoritosView   from '@/views/FavoritosView.vue'
import PedidosView     from '@/views/PedidosView.vue'
import LojaView        from '@/views/LojaView.vue'
import AvaliacoesView  from '@/views/AvaliacoesView.vue'
import ClienteView     from '@/views/ClienteView.vue'
import EmpRuralView    from '@/views/EmpRuralView.vue'
import LoginView       from '@/views/LoginView.vue'
import CriarLojaView   from '@/views/CriarLojaView.vue'
import ProdutosProdutorView from '@/views/ProdutosProdutorView.vue'
import PedidosProdutorView from '@/views/PedidosProdutorView.vue'
import { api } from '@/services/api.js'
import { useAuthStore } from '@/stores/auth.js'

const routes = [
  { path: '/',             name: 'produtos',    component: ProdutosView   },
  { path: '/carrinho',     name: 'carrinho',    component: CarrinhoView   },
  { path: '/favoritos',    name: 'favoritos',   component: FavoritosView  },
  { path: '/pedidos',      name: 'pedidos',     component: PedidosView    },
  { path: '/loja/:id',     name: 'loja',        component: LojaView       },
  { path: '/avaliacoes/:id', name: 'avaliacoes', component: AvaliacoesView },
  { path: '/cliente',      name: 'cliente',     component: ClienteView    },
  { path: '/vendedor',     name: 'emprural',    component: EmpRuralView, meta: { produtor: true } },
  { path: '/vendedor/produtos', name: 'produtos-produtor', component: ProdutosProdutorView, meta: { produtor: true, loja: true } },
  { path: '/vendedor/pedidos', name: 'pedidos-produtor', component: PedidosProdutorView, meta: { produtor: true, loja: true } },
  { path: '/login',        name: 'login',       component: LoginView      },
  { path: '/criar-loja',   name: 'criar-loja',  component: CriarLojaView  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach(async (to) => {
  if (!to.matched.some(route => route.meta.produtor)) return true

  const authStore = useAuthStore()
  if (!authStore.estaLogado) {
    return { name: 'login', query: { retorno: to.fullPath } }
  }

  try {
    const usuario = await api.usuarios.me()
    authStore.atualizarUsuario(usuario)
    if (!usuario.is_produtor) return { name: 'produtos' }
    if (to.matched.some(route => route.meta.loja) && !usuario.tem_loja) return { name: 'emprural' }
  } catch {
    return { name: 'login', query: { retorno: to.fullPath } }
  }

  return true
})

export default router
