<template>
  <div class="toast-container position-fixed top-0 end-0 p-3" aria-live="polite" aria-atomic="true">
    <div
      v-for="notificacao in notificacoesStore.notificacoes"
      :key="notificacao.id"
      class="alert alert-dismissible fade show notification shadow-sm mb-2"
      :class="`alert-${notificacao.tipo}`"
      :role="notificacao.tipo === 'danger' || notificacao.tipo === 'warning' ? 'alert' : 'status'"
    >
      {{ notificacao.mensagem }}
      <button
        type="button"
        class="btn-close"
        aria-label="Fechar notificação"
        @click.stop="notificacoesStore.remover(notificacao.id)"
      ></button>
    </div>
  </div>
</template>

<script setup>
import { useNotificacoesStore } from '@/stores/notificacoes.js'

const notificacoesStore = useNotificacoesStore()
</script>

<style scoped>
.toast-container { z-index: 1080; }
.notification { max-width: 360px; min-width: 280px; pointer-events: auto; }
</style>
