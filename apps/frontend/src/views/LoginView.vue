<template>
  <div class="d-flex justify-content-center py-3">
    <div class="login-card">

      <!-- Header verde -->
      <div class="login-header text-center">
        <div class="login-logo mx-auto mb-3">🌿</div>
        <h5 class="fw-bold text-white mb-1">Bem-vindo à Agro Store</h5>
        <p class="text-white-50 small mb-0">Escolha como deseja acessar sua conta</p>
      </div>

      <!-- Body -->
      <div class="p-4">
        <!-- Toggle Entrar / Cadastrar -->
        <div class="toggle-wrap mb-4">
          <button
            class="toggle-btn"
            :class="{ active: aba === 'entrar' }"
            @click="aba = 'entrar'"
          >Entrar</button>
          <button
            class="toggle-btn"
            :class="{ active: aba === 'cadastrar' }"
            @click="aba = 'cadastrar'"
          >Cadastrar</button>
        </div>

        <!-- FORM LOGIN -->
        <form v-if="aba === 'entrar'" @submit.prevent="fazerLogin">
          <div class="mb-3">
            <label class="form-label fw-semibold small" style="color:#1b5e35;">CPF</label>
            <div class="input-group">
              <span class="input-group-text bg-light">👤</span>
              <input
                v-model="cpf"
                type="text"
                class="form-control bg-light"
                placeholder="000.000.000-00"
                maxlength="14"
                @input="cpf = mascaraCpf(cpf)"
                required
              />
            </div>
          </div>

          <div class="mb-1">
            <div class="d-flex justify-content-between">
              <label class="form-label fw-semibold small" style="color:#1b5e35;">Senha</label>
              <a href="#" class="small" style="color:#f59e0b;">Esqueceu a senha?</a>
            </div>
            <div class="input-group">
              <span class="input-group-text bg-light">🔒</span>
              <input
                v-model="senha"
                :type="mostrarSenha ? 'text' : 'password'"
                class="form-control bg-light"
                placeholder="••••••••"
                required
              />
              <button
                type="button"
                class="input-group-text bg-light"
                @click="mostrarSenha = !mostrarSenha"
              >{{ mostrarSenha ? '🙈' : '👁️' }}</button>
            </div>
          </div>

          <!-- Erro -->
          <div v-if="erroLogin" class="alert alert-danger py-2 small mt-3 mb-0" role="alert">
            {{ erroLogin }}
          </div>

          <button
            type="submit"
            class="btn btn-success w-100 fw-bold py-2 mt-3"
            :disabled="carregando"
          >
            <span v-if="carregando" class="spinner-border spinner-border-sm me-2"></span>
            {{ carregando ? 'Entrando...' : 'Acessar Marketplace' }}
          </button>
        </form>

        <!-- CADASTRO (placeholder) -->
        <div v-else class="text-center py-3">
          <div class="fs-1 mb-2">🌱</div>
          <p class="text-muted small">Cadastro em breve disponível.</p>
        </div>

        <p class="text-muted text-center mt-3 mb-0" style="font-size:11px;">
          Ao continuar, você aceita nossos
          <a href="#" style="color:#2E8B57;">Termos de Serviço</a>
          e
          <a href="#" style="color:#2E8B57;">Políticas de Privacidade</a>.
        </p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const router    = useRouter()
const authStore = useAuthStore()

const aba         = ref('entrar')
const cpf         = ref('')
const senha       = ref('')
const mostrarSenha = ref(false)
const carregando  = ref(false)
const erroLogin   = ref('')

function mascaraCpf(valor) {
  return valor
    .replace(/\D/g, '')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d{1,2})$/, '$1-$2')
    .slice(0, 14)
}

async function fazerLogin() {
  erroLogin.value  = ''
  carregando.value = true
  try {
    // Remove máscara antes de enviar
    const cpfLimpo = cpf.value.replace(/\D/g, '')
    await authStore.login(cpfLimpo, senha.value)
    router.push({ name: 'produtos' })
  } catch (e) {
    if (e?.status === 401 || e?.status === 400) {
      erroLogin.value = 'CPF ou senha incorretos. Verifique e tente novamente.'
    } else {
      erroLogin.value = 'Não foi possível conectar ao servidor. Tente novamente.'
    }
  } finally {
    carregando.value = false
  }
}
</script>

<style scoped>
.login-card {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #d1e7d8;
  overflow: hidden;
  width: 100%;
  max-width: 400px;
}
.login-header {
  background: #2E8B57;
  padding: 1.75rem 1.5rem 1.5rem;
}
.login-logo {
  width: 48px; height: 48px;
  background: rgba(255,255,255,0.2);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
}
.toggle-wrap {
  display: flex;
  background: #E8F5E9;
  border-radius: 10px;
  padding: 3px;
}
.toggle-btn {
  flex: 1; padding: 8px;
  border: none; border-radius: 8px;
  font-size: 14px; font-weight: 500;
  background: none; color: #6b7280;
  cursor: pointer; transition: all 0.15s;
}
.toggle-btn.active {
  background: #2E8B57;
  color: #fff;
}
.btn-success { background-color: #2E8B57 !important; border-color: #2E8B57 !important; }
.btn-success:hover { background-color: #1e6b40 !important; }
.btn-success:disabled { opacity: 0.75; }
</style>