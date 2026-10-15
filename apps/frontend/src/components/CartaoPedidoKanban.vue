<template>
  <article class="card rounded-4 cartao-pedido">
    <div class="card-body p-3">
      <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
        <h3 class="h6 fw-semibold mb-0">Pedido #{{ pedido.pedido_id }}</h3>
        <time v-if="pedido.data_criacao" class="small text-body-secondary flex-shrink-0" :datetime="pedido.data_criacao">
          {{ formatarData(pedido.data_criacao) }}
        </time>
      </div>

      <p class="small d-flex align-items-center gap-2 mb-1">
        <IconeSvg nome="usuario" :tamanho="14" class="text-body-secondary" />
        <span><span class="visually-hidden">Cliente: </span>{{ pedido.cliente?.nome || 'Cliente não informado' }}</span>
      </p>
      <p v-if="pedido.cliente?.telefone" class="small mb-2">
        <a :href="`tel:+55${pedido.cliente.telefone}`" class="link-telefone d-inline-flex align-items-center gap-2">
          <IconeSvg nome="telefone" :tamanho="14" />
          <span><span class="visually-hidden">Telefone: </span>{{ formatarTelefone(pedido.cliente.telefone) }}</span>
        </a>
      </p>

      <ul class="list-unstyled small text-body-secondary mb-2" :aria-label="`Itens do pedido #${pedido.pedido_id}`">
        <li v-for="item in pedido.itens" :key="item.pedido_produto_id">{{ item.quantidade }}× {{ item.nome_produto }}</li>
      </ul>

      <div class="d-flex justify-content-between align-items-center border-top pt-2">
        <span class="small text-body-secondary">Total</span>
        <strong>{{ formatarPreco(pedido.valor_liquido) }}</strong>
      </div>

      <div v-if="info.proximo || info.podeCancelar" class="d-flex flex-wrap gap-2 mt-3">
        <button
          v-if="info.proximo"
          type="button"
          class="btn btn-sm btn-primary rounded-pill flex-grow-1 d-inline-flex align-items-center justify-content-center gap-1"
          :disabled="atualizando"
          :aria-label="`${info.acaoAvancar} do pedido #${pedido.pedido_id} (mover para ${info.proximo})`"
          @click="emit('avancar', pedido, info.proximo)"
        >
          <span v-if="atualizando" class="spinner-border spinner-border-sm" aria-hidden="true"></span>
          {{ info.acaoAvancar }}
          <IconeSvg v-if="!atualizando" nome="seta-direita" :tamanho="14" />
        </button>
        <button
          v-if="info.podeCancelar"
          type="button"
          class="btn btn-sm btn-outline-danger rounded-pill"
          :disabled="atualizando"
          :aria-label="`Cancelar pedido #${pedido.pedido_id}`"
          @click="emit('cancelar', pedido)"
        >
          Cancelar
        </button>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import IconeSvg from '@/components/IconeSvg.vue'
import { formatarData, formatarPreco, formatarTelefone } from '@/utils/formatacao.js'
import { infoStatus } from '@/utils/statusPedido.js'

const props = defineProps({
  pedido: { type: Object, required: true },
  atualizando: { type: Boolean, default: false },
})

const emit = defineEmits(['avancar', 'cancelar'])

const info = computed(() => infoStatus(props.pedido.status_nome))
</script>

<style scoped>
.link-telefone {
  color: var(--cor-primaria);
}
.link-telefone:hover {
  color: var(--cor-primaria-hover);
  text-decoration: underline;
}
</style>
