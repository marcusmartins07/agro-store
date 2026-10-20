<template>
  <div class="editor-enquadramento">
    <p id="ajuda-enquadramento" class="small text-body-secondary">
      Arraste a imagem para posicioná-la dentro do quadrado. O quadrado mostra como a foto aparece no catálogo.
    </p>

    <div v-if="erro" class="alert alert-danger small" role="alert">{{ erro }}</div>

    <div v-else class="ratio ratio-1x1 rounded-4 overflow-hidden border quadro">
      <div
        ref="area"
        class="area-arraste"
        :class="{ arrastando: arraste }"
        tabindex="0"
        aria-label="Área de enquadramento. Use as setas do teclado para mover a imagem."
        aria-describedby="ajuda-enquadramento"
        @pointerdown="iniciarArraste"
        @pointermove="moverArraste"
        @pointerup="encerrarArraste"
        @pointercancel="encerrarArraste"
        @keydown="moverPorTeclado"
      >
        <div v-if="!pronta" class="d-flex h-100 align-items-center justify-content-center">
          <span class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Carregando imagem...</span>
          </span>
        </div>
        <img
          v-if="src"
          ref="imagem"
          :src="src"
          alt=""
          class="imagem-enquadrada"
          :class="{ invisible: !pronta }"
          :style="estiloImagem"
          draggable="false"
          @load="aoCarregar"
          @error="erroCarregamento = true"
        >
        <div class="grade" aria-hidden="true"></div>
      </div>
    </div>

    <div v-if="!erro" class="d-flex align-items-center gap-3 mt-3">
      <label for="zoom-enquadramento" class="form-label mb-0">Zoom</label>
      <input
        id="zoom-enquadramento"
        :value="enquadramento.zoom"
        type="range"
        class="form-range"
        :min="ZOOM_MINIMO"
        :max="ZOOM_MAXIMO"
        step="0.01"
        :disabled="!pronta"
        @input="alterarZoom"
      >
      <button type="button" class="btn btn-sm btn-outline-secondary rounded-pill px-3" :disabled="!pronta" @click="centralizar">
        Centralizar
      </button>
    </div>

    <div class="d-flex justify-content-end gap-2 mt-4">
      <button type="button" class="btn btn-outline-secondary rounded-pill px-4" :disabled="aplicando" @click="emit('cancelar')">
        Cancelar
      </button>
      <button v-if="!erro" type="button" class="btn btn-primary rounded-pill px-4" :disabled="!pronta || aplicando" @click="aplicar">
        <span v-if="aplicando" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
        {{ aplicando ? 'Aplicando...' : 'Aplicar enquadramento' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import {
  ZOOM_MAXIMO, ZOOM_MINIMO, enquadramentoCentral, ladoDoRecorte, limitarEnquadramento, recortarQuadrado,
} from '@/utils/imagem.js'

// Cada seta move o recorte 5% do lado do quadrado
const PASSO_TECLADO = 0.05
const MENSAGEM_ERRO = 'Não foi possível abrir esta imagem para ajuste. Remova-a e envie novamente.'

const props = defineProps({
  // URL blob: da imagem original; null enquanto o formulário ainda baixa uma imagem já salva
  src: { type: String, default: null },
  enquadramentoInicial: { type: Object, default: null },
  nomeArquivo: { type: String, default: 'imagem' },
  erroExterno: { type: String, default: '' },
})

const emit = defineEmits(['aplicar', 'cancelar'])

const area = ref(null)
const imagem = ref(null)
const dimensoes = ref(null)
const enquadramento = ref({ cx: 0, cy: 0, zoom: ZOOM_MINIMO })
const erroCarregamento = ref(false)
const aplicando = ref(false)
const erroAplicar = ref('')
const arraste = ref(null)

const pronta = computed(() => !!dimensoes.value)
const erro = computed(() => props.erroExterno || (erroCarregamento.value ? MENSAGEM_ERRO : '') || erroAplicar.value)

// Posição e tamanho em % do quadro
const estiloImagem = computed(() => {
  if (!dimensoes.value) return {}
  const { largura, altura } = dimensoes.value
  const { cx, cy, zoom } = enquadramento.value
  const escala = zoom / Math.min(largura, altura)
  return {
    width: `${largura * escala * 100}%`,
    height: `${altura * escala * 100}%`,
    left: `${(0.5 - cx * escala) * 100}%`,
    top: `${(0.5 - cy * escala) * 100}%`,
  }
})

watch(() => props.src, () => {
  dimensoes.value = null
  erroCarregamento.value = false
  erroAplicar.value = ''
})

function aoCarregar() {
  const largura = imagem.value.naturalWidth
  const altura = imagem.value.naturalHeight
  dimensoes.value = { largura, altura }
  enquadramento.value = limitarEnquadramento(props.enquadramentoInicial ?? enquadramentoCentral(largura, altura), largura, altura)
}

function atualizar(novo) {
  const { largura, altura } = dimensoes.value
  enquadramento.value = limitarEnquadramento(novo, largura, altura)
}

function centralizar() {
  const { largura, altura } = dimensoes.value
  enquadramento.value = enquadramentoCentral(largura, altura)
}

function alterarZoom(evento) {
  atualizar({ ...enquadramento.value, zoom: Number(evento.target.value) })
}

function iniciarArraste(evento) {
  if (!pronta.value || evento.button !== 0) return
  area.value.setPointerCapture(evento.pointerId)
  arraste.value = { x: evento.clientX, y: evento.clientY, inicio: { ...enquadramento.value } }
}

// Arrastar a imagem para um lado leva o recorte para o lado oposto
function moverArraste(evento) {
  if (!arraste.value) return
  const { largura, altura } = dimensoes.value
  const { inicio } = arraste.value
  const pixelsNaturaisPorPixelTela = ladoDoRecorte(largura, altura, inicio.zoom) / area.value.clientWidth
  atualizar({
    ...inicio,
    cx: inicio.cx - (evento.clientX - arraste.value.x) * pixelsNaturaisPorPixelTela,
    cy: inicio.cy - (evento.clientY - arraste.value.y) * pixelsNaturaisPorPixelTela,
  })
}

function encerrarArraste() {
  arraste.value = null
}

function moverPorTeclado(evento) {
  const direcoes = { ArrowLeft: [1, 0], ArrowRight: [-1, 0], ArrowUp: [0, 1], ArrowDown: [0, -1] }
  const direcao = direcoes[evento.key]
  if (!direcao || !pronta.value) return
  evento.preventDefault()
  const { largura, altura } = dimensoes.value
  const passo = ladoDoRecorte(largura, altura, enquadramento.value.zoom) * PASSO_TECLADO
  atualizar({
    ...enquadramento.value,
    cx: enquadramento.value.cx + direcao[0] * passo,
    cy: enquadramento.value.cy + direcao[1] * passo,
  })
}

async function aplicar() {
  aplicando.value = true
  try {
    const arquivo = await recortarQuadrado(imagem.value, enquadramento.value, props.nomeArquivo)
    emit('aplicar', { arquivo, enquadramento: { ...enquadramento.value } })
  } catch (falha) {
    erroAplicar.value = falha.message || MENSAGEM_ERRO
  } finally {
    aplicando.value = false
  }
}
</script>

<style scoped>
/* Limita pela altura da tela para que zoom e botões continuem visíveis em telas baixas */
.quadro {
  width: min(100%, 24rem, 55vh);
  margin-inline: auto;
  background-color: var(--cor-neutra);
}
.area-arraste {
  cursor: grab;
  touch-action: none;
  user-select: none;
}
.area-arraste.arrastando {
  cursor: grabbing;
}
.area-arraste:focus-visible {
  outline: 3px solid var(--cor-foco);
  outline-offset: -3px;
}
/* Tamanho e posição vêm do estilo dinâmico calculado a partir do enquadramento */
.imagem-enquadrada {
  position: absolute;
  max-width: none;
  pointer-events: none;
}
/* Grade 3x3 para ajudar a centralizar o produto */
.grade {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
.grade::before,
.grade::after {
  content: '';
  position: absolute;
  border: 0 solid color-mix(in srgb, var(--cor-superficie) 80%, transparent);
}
.grade::before {
  inset: 0 calc(100% / 3);
  border-inline-width: 1px;
}
.grade::after {
  inset: calc(100% / 3) 0;
  border-block-width: 1px;
}
</style>
