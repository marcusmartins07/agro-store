<template>
  <div class="row g-4">
    <div class="col-12 col-lg-8">
      <section class="card rounded-4" aria-labelledby="titulo-dados-loja">
        <div class="card-body p-3 p-md-4">
          <h2 id="titulo-dados-loja" class="h4 fw-semibold mb-1">Dados da loja</h2>
          <p class="small text-body-secondary mb-4">Essas informações aparecem na vitrine pública da sua loja.</p>

          <form novalidate @submit.prevent="salvar">
            <div class="mb-3">
              <label for="loja-nome" class="form-label">Nome da loja <span class="text-danger">*</span></label>
              <input
                id="loja-nome"
                v-model.trim="form.nome"
                class="form-control"
                :class="{ 'is-invalid': erros.nome }"
                maxlength="150"
                required
                aria-describedby="erro-loja-nome"
              >
              <div id="erro-loja-nome" class="invalid-feedback">{{ erros.nome }}</div>
            </div>

            <div class="mb-3">
              <label for="loja-descricao" class="form-label">Descrição</label>
              <textarea
                id="loja-descricao"
                v-model.trim="form.descricao"
                class="form-control"
                :class="{ 'is-invalid': erros.descricao }"
                rows="4"
                placeholder="Conte o que você produz e como cultiva seus produtos."
                aria-describedby="erro-loja-descricao"
              ></textarea>
              <div id="erro-loja-descricao" class="invalid-feedback">{{ erros.descricao }}</div>
            </div>

            <div class="mb-4">
              <label for="loja-cnpj" class="form-label">CNPJ</label>
              <input id="loja-cnpj" :value="cnpjFormatado" class="form-control" disabled aria-describedby="ajuda-loja-cnpj">
              <div id="ajuda-loja-cnpj" class="form-text">O CNPJ não pode ser alterado por aqui.</div>
            </div>

            <div v-if="erroGeral" class="alert alert-danger small" role="alert">{{ erroGeral }}</div>

            <div class="d-flex justify-content-end gap-2">
              <button type="button" class="btn btn-outline-secondary rounded-pill px-4" :disabled="salvando || !alterado" @click="restaurar">
                Descartar alterações
              </button>
              <button type="submit" class="btn btn-primary rounded-pill px-4" :disabled="salvando || !alterado">
                <span v-if="salvando" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
                {{ salvando ? 'Salvando...' : 'Salvar alterações' }}
              </button>
            </div>
          </form>
        </div>
      </section>
    </div>

    <div class="col-12 col-lg-4 d-flex flex-column gap-4">
      <section class="card rounded-4" aria-labelledby="titulo-vitrine">
        <div class="card-body p-3 p-md-4">
          <h2 id="titulo-vitrine" class="h6 fw-semibold mb-2 titulo-secao">Vitrine pública</h2>
          <p class="small text-body-secondary mb-3">Veja a loja como os clientes a encontram no catálogo.</p>
          <RouterLink :to="{ name: 'loja', params: { id: loja.loja_id } }" class="btn btn-outline-primary rounded-pill w-100">
            Ver minha vitrine
          </RouterLink>
        </div>
      </section>

      <section class="card rounded-4" aria-labelledby="titulo-status-loja">
        <div class="card-body p-3 p-md-4">
          <h2 id="titulo-status-loja" class="h6 fw-semibold d-flex justify-content-between align-items-center gap-2 mb-2 titulo-secao">
            Status da loja
            <span class="badge rounded-pill selo-status" :class="loja.ativa ? 'selo-entregue' : 'selo-cancelado'">
              {{ loja.ativa ? 'Ativa' : 'Inativa' }}
            </span>
          </h2>
          <template v-if="loja.ativa">
            <p class="small text-body-secondary mb-3">
              Ao desativar, a loja deixa de aceitar novas compras. Produtos e pedidos são preservados.
            </p>
            <button type="button" class="btn btn-outline-danger rounded-pill w-100" :disabled="salvando" @click="desativar">
              Desativar loja
            </button>
          </template>
          <p v-else class="small text-body-secondary mb-0">A loja está inativa e não aceita novas compras.</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useNotificacoesStore } from '@/stores/notificacoes.js'
import { useProdutorStore } from '@/stores/produtor.js'
import { mascaraCnpj } from '@/utils/formatacao.js'

const produtorStore = useProdutorStore()
const notificacoes = useNotificacoesStore()
const form = ref({ nome: '', descricao: '' })
const erros = ref({})
const erroGeral = ref('')
const salvando = ref(false)

const loja = computed(() => produtorStore.loja)
const cnpjFormatado = computed(() => mascaraCnpj(loja.value?.cnpj || ''))
const alterado = computed(() =>
  form.value.nome !== (loja.value?.nome || '') || form.value.descricao !== (loja.value?.descricao || '')
)

watch(loja, restaurar, { immediate: true })

function restaurar() {
  form.value = { nome: loja.value?.nome || '', descricao: loja.value?.descricao || '' }
  erros.value = {}
  erroGeral.value = ''
}

async function salvar() {
  erroGeral.value = ''
  erros.value = form.value.nome ? {} : { nome: 'Informe o nome da loja.' }
  if (erros.value.nome) return

  salvando.value = true
  try {
    await produtorStore.salvarLoja({ nome: form.value.nome, descricao: form.value.descricao })
    notificacoes.notificar({ tipo: 'success', mensagem: 'Dados da loja atualizados.', tempo: 4 })
  } catch (falha) {
    const campos = falha.campos || {}
    erros.value = Object.fromEntries(
      ['nome', 'descricao'].filter(campo => campos[campo]).map(campo => [campo, [].concat(campos[campo])[0]])
    )
    if (!Object.keys(erros.value).length) erroGeral.value = falha.message
  } finally {
    salvando.value = false
  }
}

async function desativar() {
  if (!window.confirm('Desativar a loja impedirá novas compras. Deseja continuar?')) return

  salvando.value = true
  try {
    await produtorStore.salvarLoja({ ativa: false })
    notificacoes.notificar({ tipo: 'warning', mensagem: 'Loja desativada. Produtos e pedidos foram preservados.' })
  } catch (falha) {
    notificacoes.notificar({ tipo: 'danger', mensagem: falha.message })
  } finally {
    salvando.value = false
  }
}
</script>

<style scoped>
.titulo-secao {
  font-family: var(--fonte-texto);
}
</style>
