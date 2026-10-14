<template>
  <div
    class="seletor-quantidade d-inline-flex align-items-center rounded-pill border"
    :class="{ compacto }"
    role="group"
    :aria-label="rotulo ? `Quantidade de ${rotulo}` : 'Quantidade'"
  >
    <button
      type="button"
      class="btn rounded-circle botao-quantidade"
      :disabled="disabled || modelValue <= min"
      aria-label="Diminuir quantidade"
      @click="alterar(-1)"
    >
      <IconeSvg nome="menos" :tamanho="compacto ? 12 : 16" />
    </button>
    <output class="valor fw-semibold text-center" aria-live="polite">{{ modelValue }}</output>
    <button
      type="button"
      class="btn rounded-circle botao-quantidade"
      :disabled="disabled || modelValue >= max"
      aria-label="Aumentar quantidade"
      @click="alterar(1)"
    >
      <IconeSvg nome="mais" :tamanho="compacto ? 12 : 16" />
    </button>
  </div>
</template>

<script setup>
import IconeSvg from '@/components/IconeSvg.vue'

const props = defineProps({
  modelValue: { type: Number, required: true },
  min: { type: Number, default: 1 },
  max: { type: Number, default: Infinity },
  disabled: { type: Boolean, default: false },
  rotulo: { type: String, default: '' },
  compacto: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue'])

function alterar(passo) {
  const proximo = Math.min(props.max, Math.max(props.min, props.modelValue + passo))
  if (proximo !== props.modelValue) emit('update:modelValue', proximo)
}
</script>

<style scoped>
.seletor-quantidade {
  background-color: var(--cor-superficie);
  padding: 0.25rem;
}
.botao-quantidade {
  width: 2.5rem;
  height: 2.5rem;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 0;
}
.botao-quantidade:hover:not(:disabled) {
  background-color: var(--cor-apoio);
}
.valor {
  min-width: 2rem;
}
.compacto .botao-quantidade {
  width: 2rem;
  height: 2rem;
}
.compacto .valor {
  min-width: 1.5rem;
  font-size: 0.875rem;
}
</style>
