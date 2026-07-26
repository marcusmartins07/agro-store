<template>
  <div class="d-flex justify-content-center">
    <div class="w-100" style="max-width: 600px;">

      <div class="mb-4">
        <h2 class="fw-bold mb-1" style="color:#1b5e35;">Criar minha Loja</h2>
        <p class="text-muted small">Preencha as informações da sua loja para começar a vender.</p>
      </div>

      <div class="card border" style="border-color:#d1e7d8 !important; border-radius:14px;">
        <div class="card-body p-4">
          <form @submit.prevent="criarLoja">

            <!-- Preview da imagem -->
            <div class="text-center mb-4">
              <div class="loja-avatar mx-auto mb-2" @click="$refs.inputImagem.click()">
                <img v-if="previewImagem" :src="previewImagem" class="w-100 h-100 rounded-circle object-fit-cover" />
                <span v-else class="fs-1">🏪</span>
                <div class="avatar-overlay">📷</div>
              </div>
              <p class="text-muted small">Clique para adicionar a foto da loja</p>
              <input
                ref="inputImagem"
                type="file"
                accept="image/*"
                class="d-none"
                @change="selecionarImagem"
              />
            </div>

            <!-- Nome -->
            <div class="mb-3">
              <label class="form-label fw-semibold small" style="color:#1b5e35;">Nome da loja <span class="text-danger">*</span></label>
              <input
                v-model="form.nome"
                type="text"
                class="form-control"
                placeholder="Ex: Feira do João"
                required
              />
            </div>

            <!-- Descrição -->
            <div class="mb-3">
              <label class="form-label fw-semibold small" style="color:#1b5e35;">Descrição</label>
              <textarea
                v-model="form.descricao"
                class="form-control"
                rows="3"
                placeholder="Conte um pouco sobre sua loja e seus produtos..."
              ></textarea>
            </div>

            <!-- CNPJ -->
            <div class="mb-4">
              <label class="form-label fw-semibold small" style="color:#1b5e35;">CNPJ <span class="text-danger">*</span></label>
              <input
                v-model="form.cnpj"
                type="text"
                class="form-control"
                placeholder="00.000.000/0000-00"
                maxlength="18"
                @input="form.cnpj = mascaraCnpj(form.cnpj)"
                required
              />
            </div>

            <!-- Erro -->
            <div v-if="erro" class="alert alert-danger py-2 small mb-3">
              {{ erro }}
            </div>

            <!-- Botões -->
            <div class="d-flex gap-2">
              <button
                type="button"
                class="btn btn-outline-secondary flex-grow-1"
                @click="$router.back()"
              >
                Cancelar
              </button>
              <button
                type="submit"
                class="btn btn-success flex-grow-1 fw-bold"
                :disabled="salvando"
              >
                <span v-if="salvando" class="spinner-border spinner-border-sm me-2"></span>
                {{ salvando ? 'Criando...' : '🌾 Criar Loja' }}
              </button>
            </div>

          </form>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/services/api.js'
import { useAuthStore } from '@/stores/auth.js'

const router    = useRouter()
const authStore = useAuthStore()

const form = ref({ nome: '', descricao: '', cnpj: '' })
const imagemArquivo  = ref(null)
const previewImagem  = ref(null)
const salvando       = ref(false)
const erro           = ref('')

function selecionarImagem(event) {
  const arquivo = event.target.files[0]
  if (!arquivo) return
  imagemArquivo.value = arquivo
  previewImagem.value = URL.createObjectURL(arquivo)
}

function mascaraCnpj(valor) {
  return valor
    .replace(/\D/g, '')
    .replace(/(\d{2})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1/$2')
    .replace(/(\d{4})(\d{1,2})$/, '$1-$2')
    .slice(0, 18)
}

async function criarLoja() {
  erro.value = ''
  salvando.value = true

  try {
    const usuario = await api.usuarios.me()
    const formData = new FormData()
    formData.append('proprietario', usuario.id)
    formData.append('nome',         form.value.nome)
    formData.append('descricao',    form.value.descricao)
    formData.append('cnpj',         form.value.cnpj.replace(/\D/g, ''))
    if (imagemArquivo.value) {
      formData.append('imagem_perfil', imagemArquivo.value)
    }

    await api.lojas.criar(formData)
    router.push({ name: 'cliente' })
  } catch (e) {
    console.error(e)
    if (e?.data?.cnpj) {
      erro.value = 'CNPJ inválido ou já cadastrado.'
    } else if (e?.data?.nome) {
      erro.value = 'Este nome de loja já está em uso.'
    } else {
      erro.value = 'Não foi possível criar a loja. Verifique os dados e tente novamente.'
    }
  } finally {
    salvando.value = false
  }
}
</script>

<style scoped>
.loja-avatar {
  width: 100px; height: 100px;
  background: #E8F5E9;
  border-radius: 50%;
  border: 2px dashed #a5d6a7;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; position: relative; overflow: hidden;
  transition: border-color 0.2s;
}
.loja-avatar:hover { border-color: #2E8B57; }
.avatar-overlay {
  position: absolute; inset: 0;
  background: rgba(46,139,87,0.6);
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; opacity: 0;
  transition: opacity 0.2s;
}
.loja-avatar:hover .avatar-overlay { opacity: 1; }
.btn-success { background-color: #2E8B57 !important; border-color: #2E8B57 !important; }
.btn-success:hover { background-color: #1e6b40 !important; }
</style>