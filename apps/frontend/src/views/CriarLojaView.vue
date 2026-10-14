<template>
  <section class="mx-auto conteudo-estreito">
    <div class="mb-4">
      <h1 class="fw-semibold mb-1">Criar minha loja</h1>
      <p class="text-body-secondary mb-0">Preencha as informações da sua loja para começar a vender na feira.</p>
    </div>

    <div class="card rounded-4">
      <div class="card-body p-3 p-md-4">
        <div class="text-center mb-4">
          <span class="icone-estado" aria-hidden="true"><IconeSvg nome="loja" :tamanho="32" /></span>
        </div>

        <form novalidate @submit.prevent="criarLoja">
          <p class="small text-body-secondary">Campos com <span class="text-danger">*</span> são obrigatórios.</p>

          <div class="mb-3">
            <label for="nova-loja-nome" class="form-label">Nome da loja <span class="text-danger">*</span></label>
            <input
              id="nova-loja-nome"
              v-model.trim="form.nome"
              type="text"
              class="form-control"
              maxlength="150"
              placeholder="Ex.: Sítio Boa Terra"
              required
            >
          </div>

          <div class="mb-3">
            <label for="nova-loja-descricao" class="form-label">Descrição</label>
            <textarea
              id="nova-loja-descricao"
              v-model.trim="form.descricao"
              class="form-control"
              rows="3"
              placeholder="Conte um pouco sobre sua loja e seus produtos."
            ></textarea>
          </div>

          <div class="mb-4">
            <label for="nova-loja-cnpj" class="form-label">CNPJ <span class="text-danger">*</span></label>
            <input
              id="nova-loja-cnpj"
              v-model="form.cnpj"
              type="text"
              class="form-control"
              inputmode="numeric"
              placeholder="00.000.000/0000-00"
              maxlength="18"
              required
              @input="form.cnpj = mascaraCnpj(form.cnpj)"
            >
          </div>

          <div v-if="erro" class="alert alert-danger small mb-3" role="alert">{{ erro }}</div>

          <div class="d-flex gap-2">
            <button type="button" class="btn btn-outline-secondary rounded-pill flex-grow-1" @click="router.back()">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary rounded-pill flex-grow-1 fw-semibold" :disabled="salvando">
              <span v-if="salvando" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
              {{ salvando ? 'Criando...' : 'Criar loja' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import IconeSvg from '@/components/IconeSvg.vue'
import { api } from '@/services/api.js'
import { useNotificacoesStore } from '@/stores/notificacoes.js'
import { mascaraCnpj, somenteDigitos } from '@/utils/formatacao.js'

const router = useRouter()
const notificacoes = useNotificacoesStore()

const form = ref({ nome: '', descricao: '', cnpj: '' })
const salvando = ref(false)
const erro = ref('')

// A foto da loja não é enviada: o campo imagem_perfil do backend guarda texto e não aceita upload de arquivo.
async function criarLoja() {
  erro.value = ''
  if (!form.value.nome || somenteDigitos(form.value.cnpj).length !== 14) {
    erro.value = 'Informe o nome da loja e um CNPJ com 14 dígitos.'
    return
  }

  salvando.value = true
  try {
    await api.lojas.criar({
      nome: form.value.nome,
      descricao: form.value.descricao,
      cnpj: somenteDigitos(form.value.cnpj),
    })
    notificacoes.notificar({ tipo: 'success', mensagem: 'Loja criada! Agora cadastre seus produtos.', tempo: 6 })
    router.push({ name: 'minha-loja' })
  } catch (falha) {
    const dados = falha?.data || {}
    if (dados.cnpj) erro.value = 'CNPJ inválido ou já cadastrado.'
    else if (dados.non_field_errors) erro.value = dados.non_field_errors[0]
    else erro.value = dados.detail || 'Não foi possível criar a loja. Verifique os dados e tente novamente.'
  } finally {
    salvando.value = false
  }
}
</script>

<style scoped>
.conteudo-estreito {
  max-width: 37.5rem;
}
</style>
