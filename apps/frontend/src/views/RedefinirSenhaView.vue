<template>
  <PainelAcesso>
    <h1 class="h3 fw-semibold mb-2">Crie uma nova senha</h1>

    <template v-if="linkInvalido">
      <div ref="alertaLinkInvalido" class="alert alert-danger mt-3" role="alert" tabindex="-1">{{ MENSAGEM_LINK_INVALIDO }}</div>
      <router-link :to="{ name: 'esqueci-senha' }" class="btn btn-primary rounded-pill w-100 fw-semibold">Solicitar novo link</router-link>
    </template>

    <template v-else>
      <p class="text-body-secondary mb-4">Escolha uma senha nova para entrar na sua conta.</p>

      <form novalidate @submit.prevent="enviar">
        <div v-if="erroGeral" class="alert" :class="`alert-${erroGeral.tipo}`" role="alert">{{ erroGeral.mensagem }}</div>

        <div class="mb-3">
          <label class="form-label fw-semibold small" for="nova-senha">Nova senha</label>
          <div class="input-group">
            <input
              id="nova-senha"
              ref="campoSenha"
              v-model="senha"
              :type="mostrarSenha ? 'text' : 'password'"
              class="form-control"
              :class="{ 'is-invalid': errosSenha.length }"
              autocomplete="new-password"
              required
              :aria-invalid="errosSenha.length ? 'true' : 'false'"
              :aria-describedby="errosSenha.length ? 'ajuda-nova-senha erro-nova-senha' : 'ajuda-nova-senha'"
              :disabled="enviando"
            >
            <button
              class="btn btn-outline-secondary"
              type="button"
              :aria-label="mostrarSenha ? 'Ocultar nova senha' : 'Mostrar nova senha'"
              @click="mostrarSenha = !mostrarSenha"
            >
              {{ mostrarSenha ? 'Ocultar' : 'Mostrar' }}
            </button>
          </div>
          <div id="ajuda-nova-senha" class="form-text">
            Campo obrigatório. Use pelo menos 8 caracteres. Evite senhas comuns, só com números ou parecidas com seus dados.
          </div>
          <div v-if="errosSenha.length" id="erro-nova-senha" class="invalid-feedback d-block">
            <p v-for="mensagem in errosSenha" :key="mensagem" class="mb-0">{{ mensagem }}</p>
          </div>
        </div>

        <div class="mb-4">
          <label class="form-label fw-semibold small" for="confirmar-nova-senha">Confirmar nova senha</label>
          <div class="input-group">
            <input
              id="confirmar-nova-senha"
              ref="campoConfirmacao"
              v-model="confirmacao"
              :type="mostrarConfirmacao ? 'text' : 'password'"
              class="form-control"
              :class="{ 'is-invalid': errosConfirmacao.length }"
              autocomplete="new-password"
              required
              :aria-invalid="errosConfirmacao.length ? 'true' : 'false'"
              :aria-describedby="errosConfirmacao.length ? 'ajuda-confirmar-nova-senha erro-confirmar-nova-senha' : 'ajuda-confirmar-nova-senha'"
              :disabled="enviando"
            >
            <button
              class="btn btn-outline-secondary"
              type="button"
              :aria-label="mostrarConfirmacao ? 'Ocultar confirmação da nova senha' : 'Mostrar confirmação da nova senha'"
              @click="mostrarConfirmacao = !mostrarConfirmacao"
            >
              {{ mostrarConfirmacao ? 'Ocultar' : 'Mostrar' }}
            </button>
          </div>
          <div id="ajuda-confirmar-nova-senha" class="form-text">Campo obrigatório. Repita a nova senha.</div>
          <div v-if="errosConfirmacao.length" id="erro-confirmar-nova-senha" class="invalid-feedback d-block">
            <p v-for="mensagem in errosConfirmacao" :key="mensagem" class="mb-0">{{ mensagem }}</p>
          </div>
        </div>

        <button type="submit" class="btn btn-primary btn-lg rounded-pill w-100 fw-semibold" :disabled="enviando">
          <span v-if="enviando" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
          {{ enviando ? 'Salvando...' : 'Redefinir senha' }}
        </button>
      </form>
    </template>

    <div class="text-center mt-4">
      <router-link :to="{ name: 'login' }" class="btn btn-link btn-sm">Voltar para o login</router-link>
    </div>
  </PainelAcesso>
</template>

<script setup>
import { nextTick, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import PainelAcesso from '@/components/PainelAcesso.vue'
import { api } from '@/services/api.js'
import { useAuthStore } from '@/stores/auth.js'
import { useNotificacoesStore } from '@/stores/notificacoes.js'
import { useProdutorStore } from '@/stores/produtor.js'
import { erroGeralRedefinicao } from '@/utils/redefinicaoSenha.js'

const MENSAGEM_LINK_INVALIDO = 'Este link de redefinição é inválido ou expirou. Solicite um novo.'
const MENSAGEM_SUCESSO = 'Senha redefinida. Entre com a nova senha.'
const TAMANHO_MINIMO_SENHA = 8

const router = useRouter()
const authStore = useAuthStore()
const notificacoesStore = useNotificacoesStore()
const produtorStore = useProdutorStore()

const token = new URLSearchParams(window.location.hash.slice(1)).get('token') || ''

const senha = ref('')
const confirmacao = ref('')
const mostrarSenha = ref(false)
const mostrarConfirmacao = ref(false)
const errosSenha = ref([])
const errosConfirmacao = ref([])
const erroGeral = ref(null)
const enviando = ref(false)
const linkInvalido = ref(!token)
const campoSenha = ref(null)
const campoConfirmacao = ref(null)
const alertaLinkInvalido = ref(null)

onMounted(() => {
  if (window.location.hash) router.replace({ name: 'redefinir-senha' })
})

function comoLista(mensagens) {
  if (!mensagens) return []
  return Array.isArray(mensagens) ? mensagens : [mensagens]
}

function validar() {
  errosSenha.value = []
  errosConfirmacao.value = []

  if (!senha.value) errosSenha.value = ['Informe a nova senha.']
  else if (senha.value.length < TAMANHO_MINIMO_SENHA) errosSenha.value = ['A senha deve ter pelo menos 8 caracteres.']

  if (!confirmacao.value) errosConfirmacao.value = ['Confirme a nova senha.']
  else if (senha.value && senha.value !== confirmacao.value) errosConfirmacao.value = ['As senhas não coincidem.']

  return !errosSenha.value.length && !errosConfirmacao.value.length
}

function focarPrimeiroCampoInvalido() {
  if (errosSenha.value.length) campoSenha.value?.focus()
  else if (errosConfirmacao.value.length) campoConfirmacao.value?.focus()
}

async function mostrarLinkInvalido() {
  linkInvalido.value = true
  await nextTick()
  alertaLinkInvalido.value?.focus()
}

function concluir(mensagem) {
  authStore.logout()
  produtorStore.limpar()
  notificacoesStore.notificar({ tipo: 'success', mensagem: mensagem || MENSAGEM_SUCESSO, tempo: 10 })
  router.replace({ name: 'login' })
}

async function enviar() {
  erroGeral.value = null
  if (!validar()) {
    focarPrimeiroCampoInvalido()
    return
  }

  enviando.value = true
  try {
    const resposta = await api.auth.confirmarRedefinicaoSenha({
      token,
      password: senha.value,
      password_confirmacao: confirmacao.value,
    })
    concluir(resposta?.detail)
  } catch (erro) {
    // Reabilita os campos antes de devolver o foco a eles
    enviando.value = false
    const dados = erro?.data || {}
    if (erro?.status === 400 && (dados.detail || dados.token)) {
      await mostrarLinkInvalido()
    } else if (erro?.status === 400 && (dados.password || dados.password_confirmacao)) {
      errosSenha.value = comoLista(dados.password)
      errosConfirmacao.value = comoLista(dados.password_confirmacao)
      await nextTick()
      focarPrimeiroCampoInvalido()
    } else {
      erroGeral.value = erroGeralRedefinicao(erro)
    }
  } finally {
    enviando.value = false
  }
}
</script>
