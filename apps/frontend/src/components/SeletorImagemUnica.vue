<template>
  <div class="seletor-imagem" role="group" :aria-labelledby="`${id}-rotulo`">
    <p :id="`${id}-rotulo`" class="form-label fw-semibold mb-2" :class="{ 'visually-hidden': rotuloOculto }">{{ rotulo }}</p>

    <div class="d-flex gap-3" :class="empilhado ? 'flex-column align-items-center text-center' : 'flex-wrap align-items-center'">
      <AvatarImagem
        :src="srcExibida"
        :nome="nome"
        :tamanho="tamanho"
        :forma="forma"
        :quantidade-iniciais="quantidadeIniciais"
      />

      <!-- No modo empilhado, conteúdo entre a imagem e os botões (ex.: nome e e-mail no perfil) -->
      <slot name="apos-imagem" />

      <div class="d-flex flex-column gap-2 flex-grow-1 acoes-seletor" :class="{ 'align-items-center': empilhado }">
        <input
          :id="id"
          ref="campoArquivo"
          type="file"
          class="d-none"
          :accept="TIPOS_ACEITOS.join(',')"
          tabindex="-1"
          aria-hidden="true"
          @change="aoEscolherArquivo"
        >
        <div class="d-flex flex-wrap gap-2" :class="{ 'justify-content-center': empilhado }">
          <button
            ref="botaoEscolher"
            type="button"
            class="btn btn-outline-primary btn-sm rounded-pill px-3"
            :disabled="bloqueado"
            :aria-describedby="idsDescricao"
            @click="campoArquivo?.click()"
          >
            {{ temImagem ? 'Trocar imagem' : 'Escolher imagem' }}
          </button>
          <button
            v-if="imagemAtual && !modelValue"
            type="button"
            class="btn btn-outline-danger btn-sm rounded-pill px-3"
            :disabled="bloqueado"
            @click="emit('remover')"
          >
            Remover imagem
          </button>
        </div>
        <!-- Região sempre presente para o leitor de tela anunciar a escolha -->
        <p class="small text-body-secondary text-break mb-0" aria-live="polite">
          <template v-if="modelValue">{{ textoPendente }} {{ modelValue.name }}</template>
        </p>
        <slot name="acoes" />
      </div>
    </div>

    <div v-if="ajuda" :id="`${id}-ajuda`" class="form-text">{{ ajuda }}</div>
    <div v-if="mensagemErro" :id="`${id}-erro`" class="invalid-feedback d-block" role="alert">{{ mensagemErro }}</div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import AvatarImagem from '@/components/AvatarImagem.vue'

const TIPOS_ACEITOS = ['image/jpeg', 'image/png', 'image/webp']
const EXTENSOES_ACEITAS = ['jpg', 'jpeg', 'png', 'webp']
const TAMANHO_MAXIMO = 5 * 1024 * 1024
const MENSAGEM_TIPO = 'Envie uma imagem JPG, PNG ou WEBP válida.'
const MENSAGEM_TAMANHO = 'A imagem deve ter no máximo 5 MB.'

const props = defineProps({
  modelValue: { type: File, default: null },
  imagemAtual: { type: String, default: null },
  nome: { type: String, default: '' },
  id: { type: String, required: true },
  rotulo: { type: String, required: true },
  // Para quando um título visível da seção já nomeia o campo; o grupo continua rotulado para leitores de tela
  rotuloOculto: { type: Boolean, default: false },
  // Texto antes do nome do arquivo escolhido e ainda não enviado
  textoPendente: { type: String, default: 'Selecionada (ainda não salva):' },
  // Imagem, conteúdo do slot apos-imagem e botões em coluna, centralizados
  empilhado: { type: Boolean, default: false },
  ajuda: { type: String, default: '' },
  forma: { type: String, default: 'circulo' },
  tamanho: { type: String, default: 'xl' },
  quantidadeIniciais: { type: Number, default: 2 },
  desabilitado: { type: Boolean, default: false },
  enviando: { type: Boolean, default: false },
  erro: { type: String, default: '' },
})

const emit = defineEmits(['update:modelValue', 'selecionar', 'remover', 'erro'])

const campoArquivo = ref(null)
const botaoEscolher = ref(null)
const erroLocal = ref('')
const urlPrevia = ref(null)

const bloqueado = computed(() => props.desabilitado || props.enviando)
const srcExibida = computed(() => urlPrevia.value || props.imagemAtual)
const temImagem = computed(() => !!srcExibida.value)
const mensagemErro = computed(() => erroLocal.value || props.erro)
const idsDescricao = computed(() =>
  [props.ajuda && `${props.id}-ajuda`, mensagemErro.value && `${props.id}-erro`].filter(Boolean).join(' ') || undefined
)

// A prévia usa uma URL temporária do navegador, liberada ao trocar de arquivo ou desmontar
watch(() => props.modelValue, (arquivo) => {
  liberarPrevia()
  if (arquivo) urlPrevia.value = URL.createObjectURL(arquivo)
}, { immediate: true })

onBeforeUnmount(liberarPrevia)

function liberarPrevia() {
  if (urlPrevia.value) URL.revokeObjectURL(urlPrevia.value)
  urlPrevia.value = null
}

function validar(arquivo) {
  const extensao = arquivo.name.split('.').pop()?.toLowerCase()
  const tipoValido = !arquivo.type || TIPOS_ACEITOS.includes(arquivo.type)
  if (!tipoValido || !EXTENSOES_ACEITAS.includes(extensao)) return MENSAGEM_TIPO
  if (arquivo.size > TAMANHO_MAXIMO) return MENSAGEM_TAMANHO
  return ''
}

function aoEscolherArquivo(evento) {
  const arquivo = evento.target.files?.[0]
  evento.target.value = ''
  if (!arquivo) return

  const mensagem = validar(arquivo)
  if (mensagem) {
    // A imagem atual (ou a prévia anterior) é mantida
    erroLocal.value = mensagem
    emit('erro', mensagem)
    return
  }
  erroLocal.value = ''
  emit('update:modelValue', arquivo)
  emit('selecionar', arquivo)
}

function focar() {
  botaoEscolher.value?.focus()
}

function limparErro() {
  erroLocal.value = ''
}

defineExpose({ focar, limparErro })
</script>

<style scoped>
.acoes-seletor {
  min-width: 0;
}
</style>
