<template>
  <span class="d-inline-flex align-items-center gap-1">
    <IconeSvg
      v-for="posicao in 5"
      :key="posicao"
      nome="estrela"
      :tamanho="tamanho"
      :preenchido="posicao <= notaArredondada"
      :class="posicao <= notaArredondada ? 'estrela-cheia' : 'estrela-vazia'"
    />
    <span class="visually-hidden">Nota {{ notaFormatada }} de 5</span>
  </span>
</template>

<script setup>
import { computed } from 'vue'
import IconeSvg from '@/components/IconeSvg.vue'

const props = defineProps({
  nota: { type: Number, required: true },
  tamanho: { type: Number, default: 16 },
})

const notaArredondada = computed(() => Math.round(props.nota))
const notaFormatada = computed(() => props.nota.toLocaleString('pt-BR', { maximumFractionDigits: 1 }))
</script>

<style scoped>
.estrela-cheia { color: var(--cor-destaque); }
.estrela-vazia { color: var(--cor-texto-secundario); }
</style>
