<template>
  <section>
    <div class="d-flex justify-content-between align-items-start flex-wrap gap-3 mb-4">
      <div>
        <h1 class="fw-semibold mb-1">Área do produtor</h1>
        <p class="text-body-secondary mb-2">Acompanhe sua loja, produtos e pedidos para retirada.</p>
        <p v-if="produtorStore.loja" class="d-flex flex-wrap align-items-center gap-2 small mb-0">
          <IconeSvg nome="loja" :tamanho="16" class="text-body-secondary" />
          <span class="fw-semibold">{{ produtorStore.loja.nome }}</span>
          <span class="badge rounded-pill selo-status" :class="produtorStore.loja.ativa ? 'selo-entregue' : 'selo-cancelado'">
            {{ produtorStore.loja.ativa ? 'Loja ativa' : 'Loja inativa' }}
          </span>
        </p>
      </div>
      <button
        v-if="produtorStore.loja"
        type="button"
        class="btn btn-primary rounded-pill px-4 d-inline-flex align-items-center gap-2"
        @click="novoProduto"
      >
        <IconeSvg nome="mais" :tamanho="18" /> Novo produto
      </button>
    </div>

    <div v-if="produtorStore.carregando && !produtorStore.carregado" class="row row-cols-2 row-cols-md-3 row-cols-lg-5 g-3" aria-hidden="true">
      <div v-for="n in 5" :key="n" class="col">
        <div class="cartao-indicador rounded-4 p-3 placeholder-glow">
          <span class="placeholder col-8 d-block mb-2"></span>
          <span class="placeholder col-4 d-block"></span>
        </div>
      </div>
      <span class="visually-hidden" role="status">Carregando área do produtor...</span>
    </div>

    <div v-else-if="produtorStore.erro" class="alert alert-danger d-flex flex-wrap align-items-center gap-2" role="alert">
      <span><strong>{{ produtorStore.erro }}</strong> Verifique sua conexão e tente novamente.</span>
      <button type="button" class="btn btn-sm btn-outline-danger" @click="carregar">Tentar novamente</button>
    </div>

    <div v-else-if="produtorStore.semLoja" class="card rounded-4 text-center py-5">
      <div class="card-body">
        <span class="icone-estado mb-3"><IconeSvg nome="loja" :tamanho="32" /></span>
        <h2 class="h4 fw-semibold mb-2">Você ainda não possui uma loja</h2>
        <p class="text-body-secondary mb-3">Crie sua loja para cadastrar produtos e receber pedidos para retirada na feira.</p>
        <RouterLink :to="{ name: 'criar-loja' }" class="btn btn-primary rounded-pill px-4">Criar minha loja</RouterLink>
      </div>
    </div>

    <template v-else-if="produtorStore.loja">
      <ul class="row row-cols-2 row-cols-md-3 row-cols-lg-5 g-3 list-unstyled mb-4" aria-label="Resumo da loja">
        <li v-for="indicador in indicadores" :key="indicador.rotulo" class="col">
          <div class="cartao-indicador rounded-4 p-3 h-100">
            <span class="small text-body-secondary d-flex align-items-center gap-2 mb-1">
              <IconeSvg :nome="indicador.icone" :tamanho="16" />
              {{ indicador.rotulo }}
            </span>
            <strong class="d-block fs-3 fw-semibold">{{ indicador.valor }}</strong>
          </div>
        </li>
      </ul>

      <nav class="mb-4 border-bottom" aria-label="Seções da área do produtor">
        <ul class="nav nav-underline flex-nowrap overflow-x-auto">
          <li v-for="secao in secoes" :key="secao.rota" class="nav-item flex-shrink-0">
            <RouterLink :to="{ name: secao.rota }" class="nav-link px-1" exact-active-class="active">{{ secao.rotulo }}</RouterLink>
          </li>
        </ul>
      </nav>

      <RouterView />
    </template>
  </section>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import IconeSvg from '@/components/IconeSvg.vue'
import { useProdutorStore } from '@/stores/produtor.js'
import { formatarPreco } from '@/utils/formatacao.js'

const router = useRouter()
const produtorStore = useProdutorStore()

const secoes = [
  { rota: 'minha-loja', rotulo: 'Painel' },
  { rota: 'pedidos-produtor', rotulo: 'Pedidos' },
  { rota: 'produtos-produtor', rotulo: 'Produtos' },
  { rota: 'dados-loja', rotulo: 'Minha loja' },
]

const indicadores = computed(() => [
  { rotulo: 'Produtos ativos', valor: produtorStore.produtosAtivos, icone: 'pacote' },
  { rotulo: 'Produtos inativos', valor: produtorStore.produtosInativos, icone: 'pacote' },
  { rotulo: 'Pedidos pendentes', valor: produtorStore.quantidadePendentes, icone: 'relogio' },
  { rotulo: 'Em andamento', valor: produtorStore.quantidadeEmAndamento, icone: 'recibo' },
  { rotulo: 'Vendas do mês', valor: formatarPreco(produtorStore.vendasDoMes), icone: 'grafico' },
])

// Sempre busca dados novos ao entrar na área; trocar de aba reaproveita o que já foi carregado
onMounted(carregar)

function carregar() {
  produtorStore.carregar({ forcar: true })
}

function novoProduto() {
  router.push({ name: 'produtos-produtor', query: { novo: '1' } })
}
</script>
