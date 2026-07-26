<template>
  <div>
    <h2 class="fw-bold mb-4" style="color:#1b5e35;">Meu Perfil</h2>

    <!-- Loading -->
    <div v-if="carregando" class="card border p-4" style="border-color:#d1e7d8 !important; border-radius:14px;">
      <div class="placeholder-glow d-flex gap-3 align-items-center mb-4">
        <span class="placeholder rounded-circle" style="width:64px;height:64px;flex-shrink:0;"></span>
        <div class="flex-grow-1">
          <span class="placeholder col-4 d-block mb-2"></span>
          <span class="placeholder col-3 d-block"></span>
        </div>
      </div>
      <span class="placeholder col-12 d-block mb-2" style="height:40px;"></span>
      <span class="placeholder col-12 d-block mb-2" style="height:40px;"></span>
      <span class="placeholder col-12 d-block" style="height:40px;"></span>
    </div>

    <!-- Erro -->
    <div v-else-if="erro" class="alert alert-danger">
      ⚠️ Não foi possível carregar os dados. 
      <button class="btn btn-sm btn-outline-danger ms-2" @click="carregarUsuario">Tentar novamente</button>
    </div>

    <!-- Dados -->
    <div v-else-if="usuario" class="row g-4">

      <!-- Card perfil -->
      <div class="col-12 col-lg-4">
        <div class="card border text-center p-4" style="border-color:#d1e7d8 !important; border-radius:14px;">
          <div class="avatar mx-auto mb-3">{{ iniciais }}</div>
          <h5 class="fw-bold mb-1" style="color:#1b5e35;">{{ usuario.nome }}</h5>
          <p class="text-muted small mb-3">{{ usuario.email }}</p>

          <span
            class="badge rounded-pill px-3 py-2 mb-4"
            :class="usuario.is_produtor ? 'badge-produtor' : 'badge-cliente'"
          >
            {{ usuario.is_produtor ? '🌾 Produtor Rural' : '🛒 Cliente' }}
          </span>

          <!-- Botão criar loja -->
          <div v-if="!usuario.is_produtor">
            <hr style="border-color:#d1e7d8;" />
            <p class="text-muted small mb-3">Quer vender seus produtos na Agro Store?</p>
            <button
              class="btn btn-success w-100 fw-bold"
              :disabled="tornandoProdutor"
              @click="virarProdutor"
            >
              <span v-if="tornandoProdutor" class="spinner-border spinner-border-sm me-2"></span>
              🌾 Criar minha Loja
            </button>
          </div>

          <!-- Já é produtor -->
          <div v-else>
            <hr style="border-color:#d1e7d8;" />
            <RouterLink to="/vendedor" class="btn btn-outline-success w-100">
              🏪 Gerenciar minha Loja
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Informações -->
      <div class="col-12 col-lg-8">
        <div class="card border" style="border-color:#d1e7d8 !important; border-radius:14px;">
          <div class="card-body p-4">
            <h6 class="fw-bold mb-4" style="color:#1b5e35;">Informações Pessoais</h6>

            <div class="row g-3">
              <div class="col-12 col-sm-6">
                <label class="form-label small fw-semibold text-muted">Nome completo</label>
                <div class="info-field">{{ usuario.nome }}</div>
              </div>

              <div class="col-12 col-sm-6">
                <label class="form-label small fw-semibold text-muted">CPF</label>
                <div class="info-field">{{ formatarCpf(usuario.cpf) }}</div>
              </div>

              <div class="col-12 col-sm-6">
                <label class="form-label small fw-semibold text-muted">E-mail</label>
                <div class="info-field">{{ usuario.email }}</div>
              </div>

              <div class="col-12 col-sm-6">
                <label class="form-label small fw-semibold text-muted">Data de nascimento</label>
                <div class="info-field">{{ formatarData(usuario.data_nascimento) }}</div>
              </div>

              <div class="col-12 col-sm-6">
                <label class="form-label small fw-semibold text-muted">Gênero</label>
                <div class="info-field">{{ formatarGenero(usuario.genero) }}</div>
              </div>

              <div class="col-12 col-sm-6">
                <label class="form-label small fw-semibold text-muted">Idade</label>
                <div class="info-field">{{ usuario.idade }} anos</div>
              </div>
            </div>

          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/services/api.js'

const router          = useRouter()
const usuario         = ref(null)
const carregando      = ref(true)
const erro            = ref(false)
const tornandoProdutor = ref(false)

const iniciais = computed(() => {
  if (!usuario.value?.nome) return '?'
  return usuario.value.nome
    .split(' ')
    .slice(0, 2)
    .map(n => n[0])
    .join('')
    .toUpperCase()
})

async function carregarUsuario() {
  carregando.value = true
  erro.value = false
  try {
    usuario.value = await api.usuarios.me()
  } catch (e) {
    console.error(e)
    erro.value = true
  } finally {
    carregando.value = false
  }
}

async function virarProdutor() {
  tornandoProdutor.value = true
  try {
    await api.usuarios.tornarProdutor(usuario.value.id)
    usuario.value.is_produtor = true
    // Redireciona para criar loja
    router.push({ name: 'criar-loja' })
  } catch (e) {
    console.error(e)
    alert('Não foi possível atualizar o perfil. Tente novamente.')
  } finally {
    tornandoProdutor.value = false
  }
}

function formatarCpf(cpf) {
  return cpf?.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4') ?? '-'
}

function formatarData(data) {
  if (!data) return '-'
  const [ano, mes, dia] = data.split('-')
  return `${dia}/${mes}/${ano}`
}

function formatarGenero(g) {
  const map = { M: 'Masculino', F: 'Feminino', O: 'Outro' }
  return map[g] ?? '-'
}

onMounted(carregarUsuario)
</script>

<style scoped>
.avatar {
  width: 64px; height: 64px;
  background: #c8e6c9;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; font-weight: 700;
  color: #1b5e35;
}
.info-field {
  background: #f8fdf9;
  border: 1px solid #d1e7d8;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 14px;
  color: #1b5e35;
  font-weight: 500;
}
.badge-produtor { background: #c8e6c9; color: #1b5e35; }
.badge-cliente  { background: #E8F5E9; color: #2E8B57; }
.btn-success { background-color: #2E8B57 !important; border-color: #2E8B57 !important; }
.btn-success:hover { background-color: #1e6b40 !important; }
.btn-outline-success { color: #2E8B57 !important; border-color: #2E8B57 !important; }
.btn-outline-success:hover { background-color: #2E8B57 !important; color: #fff !important; }
</style>