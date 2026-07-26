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

const routes = [
  { path: '/',             name: 'produtos',    component: ProdutosView   },
  { path: '/carrinho',     name: 'carrinho',    component: CarrinhoView   },
  { path: '/favoritos',    name: 'favoritos',   component: FavoritosView  },
  { path: '/pedidos',      name: 'pedidos',     component: PedidosView    },
  { path: '/loja/:id',     name: 'loja',        component: LojaView       },
  { path: '/avaliacoes/:id', name: 'avaliacoes', component: AvaliacoesView },
  { path: '/cliente',      name: 'cliente',     component: ClienteView    },
  { path: '/vendedor',     name: 'emprural',    component: EmpRuralView   },
  { path: '/login',        name: 'login',       component: LoginView      },
  { path: '/criar-loja',   name: 'criar-loja',  component: CriarLojaView  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

export default router