import { createRouter, createWebHistory } from 'vue-router'
import ProdutosView    from '@/views/ProdutosView.vue'
import ProdutoDetalheView from '@/views/ProdutoDetalheView.vue'
import CarrinhoView    from '@/views/CarrinhoView.vue'
import FavoritosView   from '@/views/FavoritosView.vue'
import PedidosView     from '@/views/PedidosView.vue'
import LojaView        from '@/views/LojaView.vue'
import AvaliacoesView  from '@/views/AvaliacoesView.vue'
import PerfilView      from '@/views/PerfilView.vue'
import LoginView       from '@/views/LoginView.vue'
import CriarLojaView   from '@/views/CriarLojaView.vue'
import AreaProdutorView from '@/views/AreaProdutorView.vue'
import PainelProdutor  from '@/views/produtor/PainelProdutor.vue'
import PedidosKanban   from '@/views/produtor/PedidosKanban.vue'
import ProdutosLoja    from '@/views/produtor/ProdutosLoja.vue'
import DadosLoja       from '@/views/produtor/DadosLoja.vue'
import { api } from '@/services/api.js'
import { useAuthStore } from '@/stores/auth.js'

const routes = [
  { path: '/',             name: 'produtos',    component: ProdutosView   },
  { path: '/produto/:id',  name: 'produto',     component: ProdutoDetalheView },
  { path: '/carrinho',     name: 'carrinho',    component: CarrinhoView   },
  { path: '/favoritos',    name: 'favoritos',   component: FavoritosView  },
  { path: '/pedidos',      name: 'pedidos',     component: PedidosView    },
  { path: '/avaliacoes/:id', name: 'avaliacoes', component: AvaliacoesView },
  { path: '/perfil',       name: 'perfil',      component: PerfilView     },
  {
    path: '/minha-loja',
    component: AreaProdutorView,
    meta: { produtor: true },
    children: [
      { path: '',         name: 'minha-loja',        component: PainelProdutor },
      { path: 'pedidos',  name: 'pedidos-produtor',  component: PedidosKanban, meta: { loja: true } },
      { path: 'produtos', name: 'produtos-produtor', component: ProdutosLoja,  meta: { loja: true } },
      { path: 'loja',     name: 'dados-loja',        component: DadosLoja,     meta: { loja: true } },
    ],
  },
  // Endereços antigos continuam funcionando
  { path: '/cliente',       redirect: { name: 'perfil' } },
  { path: '/loja',          redirect: { name: 'minha-loja' } },
  { path: '/loja/produtos', redirect: { name: 'produtos-produtor' } },
  { path: '/loja/pedidos',  redirect: { name: 'pedidos-produtor' } },
  { path: '/loja/:id',     name: 'loja',        component: LojaView       },
  { path: '/login',        name: 'login',       component: LoginView      },
  { path: '/criar-loja',   name: 'criar-loja',  component: CriarLojaView, meta: { produtor: true, semLoja: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, posicaoSalva) {
    if (posicaoSalva) return posicaoSalva
    if (to.hash) return { el: to.hash, top: 96 }

    // Trocar categoria ou ordenação no catálogo mantém a rolagem; busca e paginação voltam ao topo
    const mudouSomenteFiltros = to.name === 'produtos' && from.name === 'produtos'
      && to.query.q === from.query.q && to.query.pagina === from.query.pagina
    if (mudouSomenteFiltros) return false

    return { top: 0 }
  }
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
    if (to.matched.some(route => route.meta.loja) && !usuario.tem_loja) return { name: 'minha-loja' }
    // Cada produtor possui uma única loja: quem já tem loja vai direto para a área do produtor
    if (to.matched.some(route => route.meta.semLoja) && usuario.tem_loja) return { name: 'minha-loja' }
  } catch {
    return { name: 'login', query: { retorno: to.fullPath } }
  }

  return true
})

export default router
