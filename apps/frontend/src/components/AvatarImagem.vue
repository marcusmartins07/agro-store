<template>
  <span class="avatar-imagem d-inline-flex flex-shrink-0 overflow-hidden" :class="[`avatar-${tamanho}`, classeForma]">
    <img v-if="exibirImagem" :src="src" :alt="alt" class="w-100 h-100" @error="falhouCarregar = true">
    <span
      v-else
      class="avatar-marcador w-100 h-100 d-inline-flex align-items-center justify-content-center fonte-titulo fw-semibold"
      aria-hidden="true"
    >
      {{ iniciais }}
    </span>
  </span>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { iniciaisDoNome } from '@/utils/formatacao.js'

const props = defineProps({
  src: { type: String, default: null },
  nome: { type: String, default: '' },
  tamanho: { type: String, default: 'md', validator: valor => ['sm', 'md', 'lg', 'xl'].includes(valor) },
  forma: { type: String, default: 'circulo', validator: valor => ['circulo', 'arredondado'].includes(valor) },
  // Uma letra para lojas e duas para pessoas (RN-018)
  quantidadeIniciais: { type: Number, default: 2 },
  // Vazio por padrão: o nome já aparece em texto ao lado do avatar
  alt: { type: String, default: '' },
})

// Imagem que não carrega (arquivo ausente, URL expirada ou valor legado) volta para as iniciais
const falhouCarregar = ref(false)

const exibirImagem = computed(() => !!props.src && !falhouCarregar.value)
const iniciais = computed(() => iniciaisDoNome(props.nome, props.quantidadeIniciais))
const classeForma = computed(() => {
  if (props.forma === 'circulo') return 'rounded-circle'
  return ['sm', 'md'].includes(props.tamanho) ? 'rounded-2' : 'rounded-4'
})

watch(() => props.src, () => { falhouCarregar.value = false })
</script>

<style scoped>
.avatar-imagem {
  background-color: var(--cor-neutra);
  border: 1px solid var(--cor-borda);
}

.avatar-imagem img {
  object-fit: cover;
}

.avatar-marcador {
  background-color: var(--cor-apoio);
  color: var(--cor-primaria);
  line-height: 1;
}

.avatar-sm { width: 1.75rem; height: 1.75rem; font-size: 0.75rem; }
.avatar-md { width: 3rem; height: 3rem; font-size: 1.125rem; }
.avatar-lg { width: 4.5rem; height: 4.5rem; font-size: 1.5rem; }
.avatar-xl { width: 6rem; height: 6rem; font-size: 2rem; }
</style>
