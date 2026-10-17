<template>
  <form novalidate @submit.prevent="enviar">
    <p v-if="primeiro" class="small text-body-secondary mb-3">Este será seu telefone principal.</p>
    <div class="row g-3">
      <div class="col-12 col-sm-5">
        <label :for="idTipo" class="form-label">Tipo de telefone <span class="text-danger">*</span></label>
        <select
          :id="idTipo"
          ref="campoTipo"
          v-model="tipo"
          class="form-select"
          :class="{ 'is-invalid': erroTipo }"
          :disabled="enviando"
          :aria-describedby="erroTipo ? `${idTipo}-erro` : null"
          required
        >
          <option disabled value="">Selecione</option>
          <option v-for="opcao in tipos" :key="opcao.id" :value="opcao.id">{{ opcao.descricao }}</option>
        </select>
        <div :id="`${idTipo}-erro`" class="invalid-feedback">{{ erroTipo }}</div>
      </div>
      <div class="col-12 col-sm-7">
        <label :for="idNumero" class="form-label">Número do telefone <span class="text-danger">*</span></label>
        <input
          :id="idNumero"
          ref="campoNumero"
          v-model="numero"
          class="form-control"
          :class="{ 'is-invalid': erroNumero }"
          inputmode="numeric"
          autocomplete="tel-national"
          maxlength="15"
          :placeholder="placeholderTelefone(descricaoTipo)"
          :disabled="enviando"
          :aria-describedby="erroNumero ? `${idNumero}-ajuda ${idNumero}-erro` : `${idNumero}-ajuda`"
          required
          @input="numero = mascaraTelefone(numero)"
        >
        <div :id="`${idNumero}-erro`" class="invalid-feedback">{{ erroNumero }}</div>
        <div :id="`${idNumero}-ajuda`" class="form-text">{{ ajudaTelefone(descricaoTipo) }}</div>
      </div>
    </div>

    <div v-if="erros.geral" class="alert alert-danger small mt-3 mb-0" role="alert">{{ erros.geral }}</div>

    <div class="d-flex flex-wrap justify-content-end gap-2 mt-3">
      <button type="button" class="btn btn-outline-secondary rounded-pill px-4" :disabled="enviando" @click="emit('cancelar')">Cancelar</button>
      <button type="submit" class="btn btn-primary rounded-pill px-4" :disabled="enviando">
        <span v-if="enviando" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
        {{ enviando ? 'Salvando...' : 'Salvar' }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import {
  ajudaTelefone, mascaraTelefone, placeholderTelefone, somenteDigitos, validarTelefonePorTipo,
} from '@/utils/formatacao.js'

// Formulário de apresentação de um telefone (RN-021): não chama a API; quem o usa coordena o envio
const props = defineProps({
  // Sufixo dos ids dos campos: id do telefone ou "novo"
  idSufixo: { type: [String, Number], required: true },
  tipos: { type: Array, required: true },
  // Telefone em edição ({ numero, tipo }) ou null para um novo
  telefone: { type: Object, default: null },
  // Tipo pré-selecionado em um telefone novo
  tipoPadrao: { type: [Number, String], default: '' },
  // Erros vindos do backend: { numero, tipo, geral }
  erros: { type: Object, default: () => ({}) },
  enviando: { type: Boolean, default: false },
  primeiro: { type: Boolean, default: false },
})

const emit = defineEmits(['salvar', 'cancelar'])

const idTipo = computed(() => `perfil-telefone-tipo-${props.idSufixo}`)
const idNumero = computed(() => `perfil-telefone-numero-${props.idSufixo}`)
const campoTipo = ref(null)
const campoNumero = ref(null)
const tipo = ref(props.telefone?.tipo ?? props.tipoPadrao ?? '')
const numero = ref(mascaraTelefone(props.telefone?.numero || ''))
const errosLocais = ref({})

const descricaoTipo = computed(() => props.tipos.find(opcao => opcao.id === tipo.value)?.descricao || '')
const erroTipo = computed(() => errosLocais.value.tipo || props.erros.tipo || '')
const erroNumero = computed(() => errosLocais.value.numero || props.erros.numero || '')

// Erro do backend chega depois do envio: leva o foco ao primeiro campo inválido
watch(() => props.erros, async () => {
  await nextTick()
  focarPrimeiroInvalido()
})

function focarPrimeiroInvalido() {
  if (erroTipo.value) campoTipo.value?.focus()
  else if (erroNumero.value) campoNumero.value?.focus()
}

// Espelho de exibição; a validação final é do backend
function enviar() {
  const mensagem = validarTelefonePorTipo(numero.value, descricaoTipo.value)
  errosLocais.value = {}
  if (mensagem) {
    errosLocais.value = descricaoTipo.value ? { numero: mensagem } : { tipo: mensagem }
    focarPrimeiroInvalido()
    return
  }
  emit('salvar', { tipo: tipo.value, numero: somenteDigitos(numero.value) })
}

function focar() {
  campoTipo.value?.focus()
}

defineExpose({ focar })
</script>
