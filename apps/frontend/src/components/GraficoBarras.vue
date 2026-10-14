<template>
  <figure class="mb-0">
    <figcaption class="small text-body-secondary mb-3">{{ descricao }}</figcaption>

    <div class="grafico d-flex" aria-hidden="true">
      <div class="eixo-y d-flex flex-column justify-content-between text-end small text-body-secondary">
        <span v-for="marca in marcasEixo" :key="marca">{{ formatarValor(marca) }}</span>
      </div>

      <div class="area-plot flex-grow-1 position-relative">
        <span
          v-for="(marca, indice) in marcasEixo"
          :key="marca"
          class="linha-grade position-absolute start-0 end-0"
          :style="{ bottom: `${(marcasEixo.length - 1 - indice) / (marcasEixo.length - 1) * 100}%` }"
        ></span>

        <div class="colunas d-flex h-100 position-relative">
          <div v-for="(item, indice) in dados" :key="item.chave" class="coluna d-flex flex-column align-items-center justify-content-end h-100">
            <span
              v-if="item === maiorItem && item.valor > 0"
              class="rotulo-valor small fw-semibold"
              :style="{ bottom: `${altura(item.valor)}%` }"
            >{{ formatarValor(item.valor) }}</span>
            <span class="barra" :style="{ height: `${altura(item.valor)}%` }"></span>
            <span
              class="dica small rounded-3 sombra-suave"
              :class="{ 'dica-inicio': indice === 0, 'dica-fim': indice === dados.length - 1 }"
              :style="{ bottom: `calc(${altura(item.valor)}% + 0.375rem)` }"
            >
              <strong class="d-block">{{ formatarValor(item.valor) }}</strong>
              {{ item.rotulo }}, {{ item.detalhe }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="d-flex rotulos-x small text-body-secondary" aria-hidden="true">
      <span v-for="item in dados" :key="item.chave" class="flex-fill text-center text-capitalize">{{ item.rotulo }}</span>
    </div>

    <p v-if="semValores" class="small text-body-secondary text-center mt-2 mb-0">{{ mensagemVazia }}</p>

    <!-- A tabela fica dentro de um div oculto: em <table>, a largura de 1px do .visually-hidden não é respeitada -->
    <div class="visually-hidden">
      <table>
        <caption>{{ descricao }}</caption>
        <thead>
          <tr><th scope="col">Dia</th><th scope="col">Valor</th></tr>
        </thead>
        <tbody>
          <tr v-for="item in dados" :key="item.chave">
            <th scope="row">{{ item.rotulo }}, {{ item.detalhe }}</th>
            <td>{{ formatarValor(item.valor) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </figure>
</template>

<script setup>
import { computed } from 'vue'

// Gráfico de colunas de uma única série; a tabela oculta oferece os mesmos valores para leitores de tela.
const props = defineProps({
  dados: { type: Array, required: true }, // [{ chave, rotulo, detalhe, valor }]
  descricao: { type: String, required: true },
  formatarValor: { type: Function, default: valor => String(valor) },
  mensagemVazia: { type: String, default: 'Nenhum valor no período.' },
})

const maiorItem = computed(() => props.dados.reduce((maior, item) => (item.valor > (maior?.valor ?? -1) ? item : maior), null))
const semValores = computed(() => !props.dados.some(item => item.valor > 0))

// Topo do eixo arredondado para um número "redondo" (1, 2, 2,5 ou 5 × 10ⁿ)
const topoEixo = computed(() => {
  const maior = maiorItem.value?.valor || 0
  if (maior <= 0) return 1
  const potencia = 10 ** Math.floor(Math.log10(maior))
  const passo = [1, 2, 2.5, 5, 10].find(fator => fator * potencia >= maior)
  return passo * potencia
})

const marcasEixo = computed(() => [topoEixo.value, topoEixo.value / 2, 0])

function altura(valor) {
  return Math.min(100, (valor / topoEixo.value) * 100)
}
</script>

<style scoped>
.grafico {
  height: 12rem;
  gap: 0.75rem;
}
.eixo-y {
  min-width: 4.5rem;
  font-variant-numeric: tabular-nums;
  /* Alinha o texto de cada marca ao centro da sua linha de grade */
  margin: -0.6rem 0;
}
.linha-grade {
  height: 1px;
  background-color: var(--cor-borda);
}
.colunas {
  gap: 2px;
}
.coluna {
  flex: 1 1 0;
  position: relative;
}
.barra {
  width: min(1.5rem, 60%);
  min-height: 0;
  border-radius: 4px 4px 0 0;
  background-color: var(--cor-primaria);
}
.coluna:hover .barra {
  background-color: var(--cor-primaria-hover);
}
.rotulo-valor {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 0.25rem;
  color: var(--cor-texto);
  white-space: nowrap;
}
/* Escondida com display (e não visibility) para não ampliar a largura da página no celular */
.dica {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
  padding: 0.375rem 0.625rem;
  white-space: nowrap;
  background-color: var(--cor-superficie);
  border: 1px solid var(--cor-borda);
  color: var(--cor-texto);
  display: none;
  pointer-events: none;
}
.dica-inicio {
  left: 0;
  transform: none;
}
.dica-fim {
  left: auto;
  right: 0;
  transform: none;
}
.coluna:hover .dica {
  display: block;
}
.rotulos-x {
  margin-left: 5.25rem;
  margin-top: 0.5rem;
}
</style>
