<template>
  <PainelAcesso>
    <h1 class="h3 fw-semibold mb-2">Esqueceu a senha?</h1>
    <p class="text-body-secondary mb-4">
      Informe o e-mail da sua conta. Se ele estiver cadastrado, enviaremos um link para você criar uma nova senha.
      O link vale por 30 minutos.
    </p>

    <template v-if="mensagemSucesso">
      <div ref="alertaSucesso" class="alert alert-success" role="status" tabindex="-1">
        <p class="mb-2">{{ mensagemSucesso }}</p>
        <p class="mb-0 small">Verifique também a caixa de spam. O link vale por 30 minutos e só pode ser usado uma vez.</p>
      </div>
      <button type="button" class="btn btn-outline-primary rounded-pill w-100" @click="usarOutroEmail">
        Usar outro e-mail
      </button>
    </template>

    <form v-else novalidate @submit.prevent="enviar">
      <div v-if="erroGeral" class="alert" :class="`alert-${erroGeral.tipo}`" role="alert">{{ erroGeral.mensagem }}</div>

      <div class="mb-4">
        <label class="form-label fw-semibold small" for="esqueci-email">E-mail</label>
        <input
          id="esqueci-email"
          ref="campoEmail"
          v-model="email"
          type="email"
          class="form-control"
          :class="{ 'is-invalid': erroEmail }"
          autocomplete="email"
          inputmode="email"
          required
          :aria-invalid="erroEmail ? 'true' : 'false'"
          :aria-describedby="erroEmail ? 'ajuda-esqueci-email erro-esqueci-email' : 'ajuda-esqueci-email'"
          :disabled="enviando"
        >
        <div id="ajuda-esqueci-email" class="form-text">Campo obrigatório. Use o e-mail cadastrado na sua conta.</div>
        <div v-if="erroEmail" id="erro-esqueci-email" class="invalid-feedback">{{ erroEmail }}</div>
      </div>

      <button type="submit" class="btn btn-primary btn-lg rounded-pill w-100 fw-semibold" :disabled="enviando">
        <span v-if="enviando" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
        {{ enviando ? 'Enviando...' : 'Enviar link' }}
      </button>
    </form>

    <div class="text-center mt-4">
      <router-link :to="{ name: 'login' }" class="btn btn-link btn-sm">Voltar para o login</router-link>
    </div>
  </PainelAcesso>
</template>

<script setup>
import { nextTick, ref } from 'vue'
import PainelAcesso from '@/components/PainelAcesso.vue'
import { api } from '@/services/api.js'
import { erroGeralRedefinicao } from '@/utils/redefinicaoSenha.js'

const MENSAGEM_EMAIL_VAZIO = 'Informe o e-mail da sua conta.'
const MENSAGEM_EMAIL_INVALIDO = 'Informe um e-mail válido, como nome@exemplo.com.'
// Conferência simples de formato só para orientar o usuário; o backend valida o e-mail
const FORMATO_EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const email = ref('')
const erroEmail = ref('')
const erroGeral = ref(null)
const enviando = ref(false)
const mensagemSucesso = ref('')
const alertaSucesso = ref(null)
const campoEmail = ref(null)

function validar() {
  const valor = email.value.trim()
  if (!valor) erroEmail.value = MENSAGEM_EMAIL_VAZIO
  else if (!FORMATO_EMAIL.test(valor)) erroEmail.value = MENSAGEM_EMAIL_INVALIDO
  else erroEmail.value = ''
  return !erroEmail.value
}

async function enviar() {
  erroGeral.value = null
  if (!validar()) {
    campoEmail.value?.focus()
    return
  }

  enviando.value = true
  try {
    const resposta = await api.auth.solicitarRedefinicaoSenha(email.value.trim())
    mensagemSucesso.value = resposta?.detail || 'Se houver uma conta com este e-mail, enviaremos um link para redefinir a senha.'
    await nextTick()
    alertaSucesso.value?.focus()
  } catch (erro) {
    // Reabilita o campo antes de devolver o foco a ele
    enviando.value = false
    if (erro?.status === 400) {
      erroEmail.value = MENSAGEM_EMAIL_INVALIDO
      await nextTick()
      campoEmail.value?.focus()
    } else {
      erroGeral.value = erroGeralRedefinicao(erro)
    }
  } finally {
    enviando.value = false
  }
}

async function usarOutroEmail() {
  mensagemSucesso.value = ''
  email.value = ''
  erroEmail.value = ''
  await nextTick()
  campoEmail.value?.focus()
}
</script>
