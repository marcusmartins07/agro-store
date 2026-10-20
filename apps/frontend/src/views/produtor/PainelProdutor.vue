<template>
  <div>
    <h2 class="visually-hidden">Painel</h2>

    <div class="row row-cols-1 row-cols-sm-3 g-3 mb-4">
      <div v-for="cartao in cartoesDoMes" :key="cartao.rotulo" class="col">
        <div class="card rounded-4 h-100">
          <div class="card-body p-3 p-md-4">
            <p class="small text-body-secondary mb-1">{{ cartao.rotulo }}</p>
            <p class="fs-3 fw-semibold mb-0">{{ cartao.valor }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-12 col-lg-7">
        <section class="card rounded-4 h-100" aria-labelledby="titulo-vendas-semana">
          <div class="card-body p-3 p-md-4">
            <h3 id="titulo-vendas-semana" class="h5 fw-semibold mb-1">Vendas dos últimos 7 dias</h3>
            <GraficoBarras
              :dados="produtorStore.vendasUltimosDias"
              descricao="Valor total dos pedidos não cancelados recebidos em cada dia."
              :formatar-valor="formatarMoedaCurta"
              mensagem-vazia="Nenhuma venda registrada nos últimos 7 dias."
            />
          </div>
        </section>
      </div>

      <div class="col-12 col-lg-5">
        <section class="card rounded-4 h-100" aria-labelledby="titulo-mais-vendidos">
          <div class="card-body p-3 p-md-4">
            <h3 id="titulo-mais-vendidos" class="h5 fw-semibold mb-1">Produtos mais vendidos</h3>
            <p class="small text-body-secondary mb-3">Quantidade vendida em pedidos não cancelados.</p>

            <ol v-if="produtorStore.produtosMaisVendidos.length" class="list-unstyled mb-0">
              <li
                v-for="(produto, indice) in produtorStore.produtosMaisVendidos"
                :key="produto.chave"
                class="item-ranking d-flex align-items-center gap-3 py-2"
              >
                <span class="posicao rounded-circle d-inline-flex align-items-center justify-content-center small fw-semibold flex-shrink-0">
                  {{ indice + 1 }}
                </span>
                <span class="flex-grow-1 text-truncate">
                  {{ produto.nome }}
                  <span v-if="!produto.produto" class="text-body-secondary small">(produto removido)</span>
                </span>
                <span class="small text-body-secondary text-nowrap">{{ produto.quantidade }} un.</span>
                <span class="small fw-semibold text-nowrap valor">{{ formatarPreco(produto.total) }}</span>
              </li>
            </ol>
            <p v-else class="small text-body-secondary mb-0">Os produtos aparecerão aqui assim que a loja receber pedidos.</p>
          </div>
        </section>
      </div>
    </div>

    <p class="small text-body-secondary mt-3 mb-0">
      Indicadores calculados com base nos pedidos não cancelados, apenas para acompanhamento.
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import GraficoBarras from '@/components/GraficoBarras.vue'
import { useProdutorStore } from '@/stores/produtor.js'
import { formatarPreco } from '@/utils/formatacao.js'

const produtorStore = useProdutorStore()

const cartoesDoMes = computed(() => [
  { rotulo: 'Vendas do mês', valor: formatarPreco(produtorStore.vendasDoMes) },
  { rotulo: 'Pedidos no mês', valor: produtorStore.pedidosDoMes.length },
  { rotulo: 'Ticket médio', valor: formatarPreco(produtorStore.ticketMedio) },
])

function formatarMoedaCurta(valor) {
  return Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: valor % 1 ? 2 : 0 })
}
</script>

<style scoped>
.item-ranking + .item-ranking {
  border-top: 1px solid var(--cor-borda);
}
.posicao {
  width: 1.75rem;
  height: 1.75rem;
  background-color: var(--cor-apoio);
  color: var(--cor-primaria);
}
.valor {
  min-width: 5.5rem;
  text-align: end;
}
</style>
