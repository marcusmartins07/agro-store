<template>
  <div class="d-flex justify-content-center py-3">
    <div class="login-card">
      <div class="login-header text-center">
        <h1 class="h5 fw-bold text-white mb-1">Agro Store</h1>
        <p class="text-white-50 small mb-0">Acesse ou crie sua conta para comprar na feira.</p>
      </div>

      <div class="p-4">
        <div class="toggle-wrap mb-4" role="tablist" aria-label="Acesso à conta">
          <button class="toggle-btn" :class="{ active: aba === 'entrar' }" @click="aba = 'entrar'">Entrar</button>
          <button class="toggle-btn" :class="{ active: aba === 'cadastrar' }" @click="aba = 'cadastrar'">Cadastrar</button>
        </div>

        <form v-if="aba === 'entrar'" @submit.prevent="fazerLogin" novalidate>
          <div class="mb-3">
            <label class="form-label fw-semibold small" for="login-cpf">CPF</label>
            <input id="login-cpf" v-model="cpf" class="form-control" inputmode="numeric" maxlength="14" placeholder="000.000.000-00" @input="cpf = mascaraCpf(cpf)" required>
          </div>
          <div class="mb-1">
            <label class="form-label fw-semibold small" for="login-senha">Senha</label>
            <div class="input-group">
              <input id="login-senha" v-model="senha" :type="mostrarSenhaLogin ? 'text' : 'password'" class="form-control" required>
              <button class="btn btn-outline-secondary" type="button" :aria-label="mostrarSenhaLogin ? 'Ocultar senha' : 'Mostrar senha'" @click="mostrarSenhaLogin = !mostrarSenhaLogin">
                {{ mostrarSenhaLogin ? 'Ocultar' : 'Mostrar' }}
              </button>
            </div>
          </div>
          <button type="submit" class="btn btn-primary w-100 fw-bold py-2 mt-3" :disabled="carregandoLogin">
            <span v-if="carregandoLogin" class="spinner-border spinner-border-sm me-2"></span>
            {{ carregandoLogin ? 'Entrando...' : 'Acessar marketplace' }}
          </button>
        </form>

        <form v-else @submit.prevent="fazerCadastro" novalidate>
          <div class="row g-3">
            <div class="col-12"><label class="form-label small fw-semibold" for="cadastro-nome">Nome completo</label><input id="cadastro-nome" v-model.trim="cadastro.nome" class="form-control" autocomplete="name" required></div>
            <div class="col-12 col-sm-6"><label class="form-label small fw-semibold" for="cadastro-cpf">CPF</label><input id="cadastro-cpf" v-model="cadastro.cpf" class="form-control" inputmode="numeric" maxlength="14" placeholder="000.000.000-00" @input="cadastro.cpf = mascaraCpf(cadastro.cpf)" required></div>
            <div class="col-12 col-sm-6"><label class="form-label small fw-semibold" for="cadastro-telefone">Celular</label><input id="cadastro-telefone" v-model="cadastro.telefone" class="form-control" inputmode="numeric" maxlength="15" placeholder="(00) 00000-0000" @input="cadastro.telefone = mascaraTelefone(cadastro.telefone)" required></div>
            <div class="col-12"><label class="form-label small fw-semibold" for="cadastro-email">E-mail</label><input id="cadastro-email" v-model.trim="cadastro.email" type="email" class="form-control" autocomplete="email" required></div>
            <div class="col-12 col-sm-6"><label class="form-label small fw-semibold" for="cadastro-data">Data de nascimento</label><input id="cadastro-data" v-model="cadastro.data_nascimento" type="date" class="form-control" required></div>
            <div class="col-12 col-sm-6"><label class="form-label small fw-semibold" for="cadastro-genero">Gênero</label><select id="cadastro-genero" v-model="cadastro.genero" class="form-select" required><option disabled value="">Selecione</option><option value="M">Masculino</option><option value="F">Feminino</option><option value="I">Prefiro não informar</option></select></div>
            <div class="col-12 col-sm-6">
              <label class="form-label small fw-semibold" for="cadastro-senha">Senha</label>
              <div class="input-group">
                <input id="cadastro-senha" v-model="cadastro.password" :type="mostrarSenhaCadastro ? 'text' : 'password'" class="form-control" minlength="8" autocomplete="new-password" required>
                <button class="btn btn-outline-secondary" type="button" :aria-label="mostrarSenhaCadastro ? 'Ocultar senha' : 'Mostrar senha'" @click="mostrarSenhaCadastro = !mostrarSenhaCadastro">
                  {{ mostrarSenhaCadastro ? 'Ocultar' : 'Mostrar' }}
                </button>
              </div>
              <div class="form-text">Use pelo menos 8 caracteres.</div>
            </div>
            <div class="col-12 col-sm-6">
              <label class="form-label small fw-semibold" for="cadastro-confirmacao">Confirmar senha</label>
              <div class="input-group">
                <input id="cadastro-confirmacao" v-model="cadastro.password_confirmacao" :type="mostrarConfirmacaoSenha ? 'text' : 'password'" class="form-control" minlength="8" autocomplete="new-password" required>
                <button class="btn btn-outline-secondary" type="button" :aria-label="mostrarConfirmacaoSenha ? 'Ocultar confirmação de senha' : 'Mostrar confirmação de senha'" @click="mostrarConfirmacaoSenha = !mostrarConfirmacaoSenha">
                  {{ mostrarConfirmacaoSenha ? 'Ocultar' : 'Mostrar' }}
                </button>
              </div>
            </div>
          </div>
          <button type="submit" class="btn btn-primary w-100 fw-bold py-2 mt-3" :disabled="carregandoCadastro">
            <span v-if="carregandoCadastro" class="spinner-border spinner-border-sm me-2"></span>
            {{ carregandoCadastro ? 'Criando conta...' : 'Criar conta' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import { useNotificacoesStore } from '@/stores/notificacoes.js'

const router = useRouter()
const authStore = useAuthStore()
const notificacoesStore = useNotificacoesStore()
const aba = ref('entrar')
const cpf = ref('')
const senha = ref('')
const mostrarSenhaLogin = ref(false)
const mostrarSenhaCadastro = ref(false)
const mostrarConfirmacaoSenha = ref(false)
const carregandoLogin = ref(false)
const carregandoCadastro = ref(false)
const cadastro = reactive({ nome: '', cpf: '', telefone: '', email: '', data_nascimento: '', genero: '', password: '', password_confirmacao: '' })

function somenteDigitos(valor) { return valor.replace(/\D/g, '') }
function mascaraCpf(valor) { return somenteDigitos(valor).replace(/(\d{3})(\d)/, '$1.$2').replace(/(\d{3})(\d)/, '$1.$2').replace(/(\d{3})(\d{1,2})$/, '$1-$2').slice(0, 14) }
function mascaraTelefone(valor) { return somenteDigitos(valor).replace(/^(\d{2})(\d)/, '($1) $2').replace(/(\d{5})(\d)/, '$1-$2').slice(0, 15) }

function mensagemErro(erro, fallback) {
  const dados = erro?.data
  if (!dados) return fallback
  const primeiraChave = Object.keys(dados)[0]
  const mensagem = dados[primeiraChave]
  return Array.isArray(mensagem) ? mensagem[0] : mensagem || fallback
}

function notificarErro(mensagem) {
  notificacoesStore.notificar({ tipo: 'danger', mensagem })
}

function validarLogin() {
  if (!somenteDigitos(cpf.value)) {
    notificarErro('Informe o CPF para entrar.')
    return false
  }
  if (!senha.value) {
    notificarErro('Informe a senha para entrar.')
    return false
  }
  return true
}

function validarCadastro() {
  const camposObrigatorios = [
    [cadastro.nome, 'Informe o nome completo.'],
    [cadastro.cpf, 'Informe o CPF.'],
    [cadastro.telefone, 'Informe o celular.'],
    [cadastro.email, 'Informe o e-mail.'],
    [cadastro.data_nascimento, 'Informe a data de nascimento.'],
    [cadastro.genero, 'Selecione o gênero.'],
    [cadastro.password, 'Informe a senha.'],
    [cadastro.password_confirmacao, 'Confirme a senha.'],
  ]
  const campoInvalido = camposObrigatorios.find(([valor]) => !valor)
  if (campoInvalido) {
    notificarErro(campoInvalido[1])
    return false
  }
  if (cadastro.password.length < 8) {
    notificarErro('A senha deve ter pelo menos 8 caracteres.')
    return false
  }
  if (cadastro.password !== cadastro.password_confirmacao) {
    notificarErro('As senhas não coincidem.')
    return false
  }
  return true
}

async function fazerLogin() {
  if (!validarLogin()) return
  carregandoLogin.value = true
  try {
    await authStore.login(somenteDigitos(cpf.value), senha.value)
    notificacoesStore.notificar({ tipo: 'success', mensagem: 'Login realizado com sucesso.', tempo: 10 })
    router.push({ name: 'produtos' })
  } catch (erro) {
    notificarErro(mensagemErro(erro, 'Não foi possível conectar ao servidor. Tente novamente.'))
  } finally { carregandoLogin.value = false }
}

async function fazerCadastro() {
  if (!validarCadastro()) return
  carregandoCadastro.value = true
  try {
    await authStore.cadastrar({ ...cadastro, cpf: somenteDigitos(cadastro.cpf), telefone: somenteDigitos(cadastro.telefone) })
    notificacoesStore.notificar({ tipo: 'success', mensagem: 'Conta criada com sucesso.', tempo: 10 })
    router.push({ name: 'produtos' })
  } catch (erro) {
    notificarErro(mensagemErro(erro, 'Não foi possível criar a conta. Tente novamente.'))
  } finally { carregandoCadastro.value = false }
}
</script>

<style scoped>
.login-card { background: var(--white); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; width: 100%; max-width: 520px; }
.login-header { background: var(--green-dark); padding: 1.75rem 1.5rem 1.5rem; }
.toggle-wrap { display: flex; background: var(--green-light); border-radius: 10px; padding: 3px; }
.toggle-btn { flex: 1; padding: 8px; border: 0; border-radius: 8px; background: transparent; color: var(--gray); }
.toggle-btn.active { background: var(--green-dark); color: var(--white); }
.btn-primary { background: var(--green-dark); border-color: var(--green-dark); }
</style>
