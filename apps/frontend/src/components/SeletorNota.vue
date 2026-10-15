<template>
  <fieldset class="seletor-nota" :aria-describedby="idDescricao" :disabled="desabilitado">
    <legend class="form-label fs-6 fw-semibold mb-1">Sua nota (obrigatória)</legend>

    <div class="d-flex flex-wrap align-items-center gap-1">
      <template v-for="valor in NOTAS" :key="valor">
        <input
          :id="`${idGrupo}-${valor}`"
          ref="opcoes"
          class="visually-hidden opcao-nota"
          type="radio"
          :name="idGrupo"
          :value="valor"
          :checked="modelValue === valor"
          @change="emit('update:modelValue', valor)"
        />
        <label :for="`${idGrupo}-${valor}`" class="rotulo-estrela">
          <IconeSvg
            nome="estrela"
            :tamanho="28"
            :preenchido="valor <= (modelValue || 0)"
            :class="valor <= (modelValue || 0) ? 'estrela-cheia' : 'estrela-vazia'"
          />
          <span class="visually-hidden">{{ valor }} {{ valor === 1 ? 'estrela' : 'estrelas' }}</span>
        </label>
      </template>
    </div>

    <p :id="idDescricao" class="small mb-0" :class="modelValue ? 'fw-semibold' : 'text-body-secondary'">{{ textoNota }}</p>
  </fieldset>
</template>

<script setup>
import { computed, ref, useId } from 'vue'
import IconeSvg from '@/components/IconeSvg.vue'

const NOTAS = [1, 2, 3, 4, 5]
const TEXTOS_NOTA = { 1: 'Ruim', 2: 'Regular', 3: 'Bom', 4: 'Muito bom', 5: 'Excelente' }

const props = defineProps({
  modelValue: { type: Number, default: null },
  desabilitado: { type: Boolean, default: false },
  invalido: { type: Boolean, default: false },
  // id da mensagem de erro externa, somada à descrição do grupo
  idErro: { type: String, default: '' },
})

const emit = defineEmits(['update:modelValue'])

const idGrupo = useId()
const idTexto = useId()
const opcoes = ref([])

const textoNota = computed(() => TEXTOS_NOTA[props.modelValue] || 'Selecione uma nota')
const idDescricao = computed(() => [idTexto, props.invalido && props.idErro].filter(Boolean).join(' '))

function focar() {
  const marcada = opcoes.value.find(opcao => opcao.checked)
  ;(marcada || opcoes.value[0])?.focus()
}

defineExpose({ focar })
</script>

<style scoped>
.seletor-nota {
  min-width: 0;
}
.rotulo-estrela {
  width: 2.75rem;
  height: 2.75rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  cursor: pointer;
}
fieldset:enabled .rotulo-estrela:hover {
  background-color: var(--cor-apoio);
}
.opcao-nota:focus-visible + .rotulo-estrela {
  outline: 2px solid var(--cor-foco);
  outline-offset: 2px;
}
fieldset:disabled .rotulo-estrela {
  cursor: not-allowed;
  opacity: 0.65;
}
.estrela-cheia {
  color: var(--cor-destaque);
  stroke: var(--cor-destaque-forte);
}
.estrela-vazia {
  color: var(--cor-texto-secundario);
}
</style>
