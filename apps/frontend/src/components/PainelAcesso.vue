<template>
  <div class="row g-4 align-items-stretch py-md-3">
    <div class="col-md-6 d-none d-md-flex">
      <div class="fundo-destaque rounded-5 p-5 d-flex flex-column justify-content-end w-100">
        <slot name="painel">
          <IconeSvg nome="broto" :tamanho="40" class="mb-3" />
          <!-- O h1 só fica no painel quando a tela não tem outro título principal (ex.: login) -->
          <component :is="tituloNoPainel ? 'h1' : 'p'" class="fonte-titulo fw-semibold mb-3 titulo-painel">
            Bem-vindo à Agro Store
          </component>
          <p class="mb-0 opacity-75">
            Conectando as famílias agricultoras da Feira do Produtor Rural Willi Dummer a quem valoriza comida de verdade.
          </p>
        </slot>
      </div>
    </div>

    <div class="col-12 col-md-6">
      <div class="card rounded-5 sombra-suave h-100">
        <div class="card-body p-4 p-lg-5">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import IconeSvg from '@/components/IconeSvg.vue'

defineProps({
  tituloNoPainel: { type: Boolean, default: false },
})
</script>

<style scoped>
.titulo-painel {
  font-size: 2.5rem;
  line-height: 1.2;
}
</style>
