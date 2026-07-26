<template>
  <div>
    <h2 class="fw-bold mb-4" style="color:#1b5e35;">Minha Loja</h2>

    <!-- Loading -->
    <div v-if="carregando" class="card border p-4" style="border-color:#d1e7d8 !important; border-radius:14px;">
      <div class="placeholder-glow d-flex gap-3 align-items-center mb-4">
        <span class="placeholder rounded-circle" style="width:80px;height:80px;flex-shrink:0;"></span>
        <div class="flex-grow-1">
          <span class="placeholder col-5 d-block mb-2" style="height:20px;"></span>
          <span class="placeholder col-3 d-block"></span>
        </div>
      </div>
      <span class="placeholder col-12 d-block mb-2" style="height:40px;"></span>
      <span class="placeholder col-12 d-block mb-2" style="height:40px;"></span>
      <span class="placeholder col-12 d-block" style="height:40px;"></span>
    </div>

    <!-- Sem loja -->
    <div v-else-if="semLoja" class="card border text-center py-5" style="border-color:#d1e7d8 !important; border-radius:14px;">
      <div class="card-body">
        <div class="fs-1 mb-3">🏪</div>
        <h5 class="fw-bold mb-2" style="color:#1b5e35;">Você ainda não tem uma loja</h5>
        <p class="text-muted mb-4">Crie sua loja para começar a vender na Agro Store.</p>
        <RouterLink to="/criar-loja" class="btn btn-success rounded-pill px-4 fw-bold">
          🌾 Criar minha Loja
        </RouterLink>
      </div>
    </div>

    <!-- Erro -->
    <div v-else-if="erro" class="alert alert-danger">
      ⚠️ Não foi possível carregar os dados da loja.
      <button class="btn btn-sm btn-outline-danger ms-2" @click="carregarLoja">Tentar novamente</button>
    </div>

    <!-- Dados da loja -->
    <div v-else-if="loja" class="row g-4">

      <!-- Card principal -->
      <div class="col-12 col-lg-4">
        <div class="card border text-center p-4" style="border-color:#d1e7d8 !important; border-radius:14px;">

          <!-- Imagem ou emoji -->
          <div class="loja-avatar mx-auto mb-3">
            <img
              v-if="loja.imagem_perfil"
              :src="imagemUrl"
              class="w-100 h-100 rounded-circle object-fit-cover"
              @error="imagemComErro = true"
            />
            <span v-else class="fs-1">🏪</span>
          </div>

          <h5 class="fw-bold mb-1" style="color:#1b5e35;">{{ loja.nome }}</h5>
          <p class="text-muted small mb-1">{{ loja.proprietario_nome }}</p>

          <span class="badge rounded-pill px-3 py-2 mb-4" :class="loja.ativa ? 'badge-ativa' : 'badge-inativa'">
            {{ loja.ativa ? '✅ Loja Ativa' : '⏸️ Loja Inativa' }}
          </span>

          <hr style="border-color:#d1e7d8;" />

          <RouterLink to="/criar-loja" class="btn btn-outline-success w-100 btn-sm">
            ✏️ Editar informações
          </RouterLink>
        </div>
      </div>

      <!-- Informações -->
      <div class="col-12 col-lg-8">
        <div class="card border" style="border-color:#d1e7d8 !important; border-radius:14px;">
          <div class="card-body p-4">
            <h6 class="fw-bold mb-4" style="color:#1b5e35;">Informações da Loja</h6>

            <div class="row g-3">

              <div class="col-12">
                <label class="form-label small fw-semibold text-muted">Nome da loja</label>
                <div class="info-field">{{ loja.nome }}</div>
              </div>

              <div class="col-12">
                <label class="form-label small fw-semibold text-muted">Descrição</label>
                <div class="info-field">{{ loja.descricao || '—' }}</div>
              </div>

              <div class="col-12 col-sm-6">
                <label class="form-label small fw-semibold text-muted">CNPJ</label>
                <div class="info-field">{{ formatarCnpj(loja.cnpj) }}</div>
              </div>

              <div class="col-12 col-sm-6">
                <label class="form-label small fw-semibold text-muted">Proprietário</label>
                <div class="info-field">{{ loja.proprietario_nome }}</div>
              </div>

              <div class="col-12 col-sm-6">
                <label class="form-label small fw-semibold text-muted">ID da loja</label>
                <div class="info-field">#{{ loja.loja_id }}</div>
              </div>

              <div class="col-12 col-sm-6">
                <label class="form-label small fw-semibold text-muted">Status</label>
                <div class="info-field">{{ loja.ativa ? 'Ativa' : 'Inativa' }}</div>
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
import { api, BACKEND_URL } from '@/services/api.js'

const loja          = ref(null)
const carregando    = ref(true)
const erro          = ref(false)
const semLoja       = ref(false)
const imagemComErro = ref(false)

const imagemUrl = computed(() => {
  if (!loja.value?.imagem_perfil || imagemComErro.value) return null
  // Se já for URL completa, usa direto; senão monta com BASE_URL
  if (loja.value.imagem_perfil.startsWith('http')) return loja.value.imagem_perfil
  const caminho = loja.value.imagem_perfil.replace(/^\/?(media\/)?/, '')
  return `${BACKEND_URL}/media/${caminho}`
})

async function carregarLoja() {
  carregando.value = true
  erro.value       = false
  semLoja.value    = false
  try {
    loja.value = await api.lojas.me()
  } catch (e) {
    // 404 = usuário não tem loja ainda
    if (e?.status === 404 || e?.message?.includes('404')) {
      semLoja.value = true
    } else {
      erro.value = true
    }
  } finally {
    carregando.value = false
  }
}

function formatarCnpj(cnpj) {
  if (!cnpj) return '—'
  return cnpj.replace(/\D/g, '')
    .replace(/(\d{2})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1/$2')
    .replace(/(\d{4})(\d{1,2})$/, '$1-$2')
}

onMounted(carregarLoja)
</script>

<style scoped>
.loja-avatar {
  width: 90px; height: 90px;
  background: #E8F5E9;
  border-radius: 50%;
  border: 2px solid #a5d6a7;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
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
.badge-ativa   { background: #c8e6c9; color: #1b5e35; }
.badge-inativa { background: #fee2e2; color: #dc2626; }
.btn-success { background-color: #2E8B57 !important; border-color: #2E8B57 !important; }
.btn-success:hover { background-color: #1e6b40 !important; }
.btn-outline-success { color: #2E8B57 !important; border-color: #2E8B57 !important; }
.btn-outline-success:hover { background-color: #2E8B57 !important; color: #fff !important; }
</style>
