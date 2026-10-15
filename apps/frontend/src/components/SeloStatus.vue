<template>
  <span class="badge rounded-pill selo-status" :class="classe">{{ rotulo || status }}</span>
</template>

<script setup>
import { computed } from 'vue'
import { infoStatus } from '@/utils/statusPedido.js'

// Selo com texto sempre visível; a cor apenas reforça o status.
const props = defineProps({
  status: { type: String, required: true },
  rotulo: { type: String, default: '' },
  // Classe explícita para selos que não são de pedido (ex.: produto ativo/inativo)
  variante: { type: String, default: '' },
})

const classe = computed(() => props.variante ? `selo-${props.variante}` : infoStatus(props.status).classe)
</script>
