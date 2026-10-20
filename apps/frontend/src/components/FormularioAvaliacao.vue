<template>
  <form novalidate @submit.prevent="emit('enviar')">
    <div class="mb-3">
      <p class="fw-semibold mb-0 text-break">{{ nomeProduto }}</p>
      <p class="small text-body-secondary mb-0">Pedido #{{ pedidoId }} · {{ lojaNome }}</p>
    </div>

    <div v-if="erro" class="alert alert-danger small py-2" role="alert">{{ erro }}</div>

    <div class="mb-3">
      <SeletorNota
        ref="seletor"
        :model-value="nota"
        :desabilitado="desabilitado"
        :invalido="Boolean(erroNota)"
        :id-erro="idErroNota"
        @update:model-value="emit('update:nota', $event)"
      />
      <p v-if="erroNota" :id="idErroNota" class="small text-danger mb-0 mt-1">{{ erroNota }}</p>
    </div>

    <div class="mb-3">
      <label :for="idComentario" class="form-label">Comentário (opcional)</label>
      <textarea
        :id="idComentario"
        class="form-control"
        rows="3"
        :maxlength="LIMITE_COMENTARIO"
        :value="comentario"
        :disabled="desabilitado"
        :aria-describedby="`${idAjuda} ${idContador}`"
        @input="emit('update:comentario', $event.target.value)"
      ></textarea>
      <div class="d-flex justify-content-between gap-2 small text-body-secondary mt-1">
        <span :id="idAjuda">Conte como foi o produto: qualidade, frescor, sabor.</span>
        <span :id="idContador" class="flex-shrink-0">{{ comentario.length }}/{{ LIMITE_COMENTARIO }}</span>
      </div>
    </div>

    <div class="alert alert-info small mb-0">
      Atenção: depois de enviada, a avaliação não pode ser editada nem removida por você.
      Ela aparece publicamente no produto, com seu nome abreviado.
    </div>
  </form>
</template>

<script setup>
import { ref, useId } from 'vue'
import SeletorNota from '@/components/SeletorNota.vue'

const LIMITE_COMENTARIO = 500

defineProps({
  nomeProduto: { type: String, required: true },
  pedidoId: { type: [Number, String], required: true },
  lojaNome: { type: String, default: '' },
  nota: { type: Number, default: null },
  comentario: { type: String, default: '' },
  desabilitado: { type: Boolean, default: false },
  erro: { type: String, default: '' },
  erroNota: { type: String, default: '' },
})

const emit = defineEmits(['update:nota', 'update:comentario', 'enviar'])

const idComentario = useId()
const idAjuda = useId()
const idContador = useId()
const idErroNota = useId()
const seletor = ref(null)

function focarNota() {
  seletor.value?.focar()
}

defineExpose({ focarNota })
</script>
