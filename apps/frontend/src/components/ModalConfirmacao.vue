<template>
  <div ref="elemento" class="modal fade" tabindex="-1" :aria-labelledby="idTitulo" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" :class="{ 'modal-dialog-scrollable': rolavel }">
      <div class="modal-content rounded-4">
        <div class="modal-header">
          <h2 :id="idTitulo" class="modal-title h5 fw-semibold">{{ titulo }}</h2>
          <button type="button" class="btn-close" aria-label="Fechar" :disabled="carregando" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">
          <slot />
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-outline-secondary rounded-pill px-4" :disabled="carregando" data-bs-dismiss="modal">
            {{ textoFechar }}
          </button>
          <button type="button" class="btn rounded-pill px-4" :class="`btn-${variante}`" :disabled="carregando" @click="emit('confirmar')">
            <span v-if="carregando" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
            {{ carregando ? textoCarregando : textoConfirmar }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, useId } from 'vue'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.min.js'

const props = defineProps({
  titulo: { type: String, required: true },
  textoConfirmar: { type: String, default: 'Confirmar' },
  textoCarregando: { type: String, default: 'Processando...' },
  textoFechar: { type: String, default: 'Cancelar' },
  variante: { type: String, default: 'danger' },
  carregando: { type: Boolean, default: false },
  // Corpo com rolagem própria, mantendo cabeçalho e botões visíveis em telas baixas
  rolavel: { type: Boolean, default: false },
})

const emit = defineEmits(['confirmar', 'fechado'])

const idTitulo = useId()
const elemento = ref(null)
let modal = null
let gatilho = null

onMounted(() => {
  modal = bootstrap.Modal.getOrCreateInstance(elemento.value)
  elemento.value.addEventListener('hide.bs.modal', impedirFechamentoDuranteAcao)
  elemento.value.addEventListener('hidden.bs.modal', aoFechar)
})

onBeforeUnmount(() => {
  const instancia = modal
  elemento.value.removeEventListener('hide.bs.modal', impedirFechamentoDuranteAcao)
  elemento.value.removeEventListener('hidden.bs.modal', aoFechar)
  if (elemento.value.classList.contains('show')) {
    elemento.value.addEventListener('hidden.bs.modal', () => instancia.dispose(), { once: true })
    instancia.hide()
  } else {
    instancia.dispose()
  }
})

function abrir() {
  gatilho = document.activeElement
  modal.show()
}

// Espera o pai repassar carregando = false antes de fechar
async function fechar() {
  await nextTick()
  modal.hide()
}

// Esc e clique fora não fecham o modal enquanto a ação está em andamento
function impedirFechamentoDuranteAcao(evento) {
  if (props.carregando) evento.preventDefault()
}

function aoFechar() {
  if (gatilho?.isConnected) gatilho.focus()
  gatilho = null
  emit('fechado')
}

defineExpose({ abrir, fechar })
</script>
