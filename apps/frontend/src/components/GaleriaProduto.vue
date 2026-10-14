<template>
  <div>
    <div
      class="galeria position-relative rounded-5 overflow-hidden"
      role="region"
      aria-roledescription="carrossel"
      :aria-label="`Imagens de ${nomeProduto}`"
    >
      <div class="ratio ratio-1x1">
        <img v-if="slideAtual.tipo === 'imagem'" :src="slideAtual.src" :alt="slideAtual.alt" class="object-fit-cover">
        <div v-else class="imagem-placeholder text-center p-4">
          <IconeSvg nome="imagem" :tamanho="56" />
          <span class="fw-semibold">{{ slideAtual.tipo === 'ilustrativa' ? 'Imagem ilustrativa' : 'Sem foto cadastrada' }}</span>
        </div>
      </div>

      <template v-if="slides.length > 1">
        <button type="button" class="botao-navegacao start-0 ms-3" @click="irPara(indiceAtual - 1)">
          <IconeSvg nome="seta-esquerda" />
          <span class="visually-hidden">Imagem anterior</span>
        </button>
        <button type="button" class="botao-navegacao end-0 me-3" @click="irPara(indiceAtual + 1)">
          <IconeSvg nome="seta-direita" />
          <span class="visually-hidden">Próxima imagem</span>
        </button>
        <p class="visually-hidden" aria-live="polite">Imagem {{ indiceAtual + 1 }} de {{ slides.length }}</p>
      </template>
    </div>

    <div v-if="slides.length > 1" class="d-flex flex-wrap gap-2 mt-3">
      <button
        v-for="(slide, indice) in slides"
        :key="indice"
        type="button"
        class="miniatura rounded-3 overflow-hidden p-0"
        :class="{ ativa: indice === indiceAtual }"
        :aria-label="`Ver imagem ${indice + 1} de ${slides.length}`"
        :aria-current="indice === indiceAtual ? 'true' : undefined"
        @click="irPara(indice)"
      >
        <img v-if="slide.tipo === 'imagem'" :src="slide.src" alt="" class="w-100 h-100 object-fit-cover" loading="lazy">
        <span v-else class="imagem-placeholder w-100 h-100">
          <IconeSvg nome="imagem" :tamanho="20" />
        </span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import IconeSvg from '@/components/IconeSvg.vue'

const props = defineProps({
  // Cada slide: { tipo: 'imagem' | 'sem-foto' | 'ilustrativa', src?, alt }
  slides: { type: Array, required: true },
  nomeProduto: { type: String, required: true },
})

const indiceAtual = ref(0)

const slideAtual = computed(() => props.slides[indiceAtual.value] ?? { tipo: 'sem-foto', alt: '' })

watch(() => props.slides, () => {
  indiceAtual.value = 0
})

function irPara(indice) {
  const total = props.slides.length
  indiceAtual.value = (indice + total) % total
}
</script>

<style scoped>
.galeria {
  background-color: var(--cor-neutra);
}
.botao-navegacao {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--cor-borda);
  border-radius: 50%;
  background-color: var(--cor-superficie);
  color: var(--cor-texto);
  box-shadow: var(--sombra-suave);
}
.botao-navegacao:hover {
  background-color: var(--cor-apoio);
}
.botao-navegacao:focus-visible,
.miniatura:focus-visible {
  outline: 2px solid var(--cor-foco);
  outline-offset: 2px;
}
.miniatura {
  width: 5rem;
  height: 5rem;
  border: 2px solid transparent;
  background-color: var(--cor-neutra);
}
.miniatura:hover,
.miniatura.ativa {
  border-color: var(--cor-primaria);
}
</style>
