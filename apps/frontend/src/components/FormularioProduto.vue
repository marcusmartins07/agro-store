<template>
  <div
    ref="painel"
    class="offcanvas offcanvas-end painel-formulario"
    tabindex="-1"
    aria-labelledby="titulo-formulario-produto"
  >
    <div class="offcanvas-header border-bottom">
      <h2 id="titulo-formulario-produto" class="offcanvas-title h4 fw-semibold">
        {{ produtoEditado ? 'Editar produto' : 'Novo produto' }}
      </h2>
      <button type="button" class="btn-close" aria-label="Fechar" :disabled="salvando" @click="fechar"></button>
    </div>

    <div class="offcanvas-body">
      <form id="formulario-produto" novalidate @submit.prevent="salvar">
        <p class="small text-body-secondary">Campos com <span class="text-danger">*</span> são obrigatórios.</p>

        <div class="mb-3">
          <label for="produto-nome" class="form-label">Nome <span class="text-danger">*</span></label>
          <input
            id="produto-nome"
            v-model.trim="form.nome"
            class="form-control"
            :class="{ 'is-invalid': erros.nome }"
            maxlength="155"
            required
            aria-describedby="erro-produto-nome"
          >
          <div id="erro-produto-nome" class="invalid-feedback">{{ erros.nome }}</div>
        </div>

        <div class="row g-3 mb-3">
          <div class="col-12 col-sm-7">
            <label for="produto-categoria" class="form-label">Categoria <span class="text-danger">*</span></label>
            <select
              id="produto-categoria"
              v-model="form.categoria"
              class="form-select"
              :class="{ 'is-invalid': erros.categoria }"
              required
              aria-describedby="erro-produto-categoria"
            >
              <option value="">Selecione</option>
              <option v-if="categoriaInativa" :value="categoriaInativa.id" disabled>{{ categoriaInativa.nome }} (inativa)</option>
              <option v-for="categoria in produtorStore.categorias" :key="categoria.categoria_id" :value="categoria.categoria_id">
                {{ categoria.nome }}
              </option>
            </select>
            <div id="erro-produto-categoria" class="invalid-feedback">{{ erros.categoria }}</div>
          </div>
          <div class="col-12 col-sm-5">
            <label for="produto-estoque" class="form-label">Estoque <span class="text-danger">*</span></label>
            <input
              id="produto-estoque"
              v-model.number="form.estoque"
              type="number"
              min="0"
              class="form-control"
              :class="{ 'is-invalid': erros.estoque }"
              required
              aria-describedby="erro-produto-estoque"
            >
            <div id="erro-produto-estoque" class="invalid-feedback">{{ erros.estoque }}</div>
          </div>
        </div>

        <div class="mb-3">
          <label for="produto-descricao" class="form-label">Descrição</label>
          <textarea id="produto-descricao" v-model.trim="form.descricao" rows="3" class="form-control"></textarea>
        </div>

        <div class="mb-3">
          <label for="produto-imagem" class="form-label">Imagem do produto</label>
          <div class="d-flex align-items-center gap-3">
            <img v-if="previewImagem" :src="previewImagem" alt="Pré-visualização da imagem do produto" class="imagem-preview rounded-3 border">
            <span v-else class="imagem-preview imagem-placeholder rounded-3" aria-hidden="true"><IconeSvg nome="imagem" :tamanho="22" /></span>
            <input
              id="produto-imagem"
              ref="campoImagem"
              type="file"
              class="form-control"
              accept="image/jpeg,image/png,image/webp"
              aria-describedby="ajuda-produto-imagem"
              @change="selecionarImagem"
            >
          </div>
          <div id="ajuda-produto-imagem" class="form-text">Opcional. JPG, PNG ou WEBP com até 5 MB.</div>
        </div>

        <fieldset class="bg-apoio rounded-4 p-3 mb-3">
          <legend class="h6 fw-semibold float-none w-auto mb-2">Preço</legend>
          <div class="row g-3">
            <div class="col-12 col-sm-7">
              <label for="produto-preco" class="form-label">
                {{ produtoEditado ? 'Novo preço de venda' : 'Preço de venda' }}
                <span v-if="!produtoEditado" class="text-danger">*</span>
              </label>
              <div class="input-group has-validation">
                <span class="input-group-text">R$</span>
                <input
                  id="produto-preco"
                  v-model="form.precoVenda"
                  inputmode="decimal"
                  class="form-control"
                  :class="{ 'is-invalid': erros.precoVenda }"
                  placeholder="0,00"
                  :required="!produtoEditado"
                  aria-describedby="ajuda-produto-preco erro-produto-preco"
                >
                <div id="erro-produto-preco" class="invalid-feedback">{{ erros.precoVenda }}</div>
              </div>
              <div v-if="produtoEditado" id="ajuda-produto-preco" class="form-text">
                Deixe em branco para manter {{ formatarPreco(produtoEditado.preco_original) }}.
              </div>
            </div>
            <div class="col-12 col-sm-5">
              <label for="produto-desconto" class="form-label">Desconto (%)</label>
              <input
                id="produto-desconto"
                v-model="form.desconto"
                type="number"
                min="0"
                max="100"
                step="1"
                class="form-control"
                :class="{ 'is-invalid': erros.desconto }"
                placeholder="Opcional"
                aria-describedby="erro-produto-desconto"
              >
              <div id="erro-produto-desconto" class="invalid-feedback">{{ erros.desconto }}</div>
            </div>
          </div>
          <p class="small mb-0 mt-3" aria-live="polite">
            Preço final ao cliente: <strong>{{ precoFinal === null ? 'informe o preço de venda' : formatarPreco(precoFinal) }}</strong>
          </p>
        </fieldset>

        <div v-if="produtoEditado" class="form-check mb-3">
          <input id="produto-ativo" v-model="form.ativo" class="form-check-input" type="checkbox">
          <label for="produto-ativo" class="form-check-label">Produto disponível para compra</label>
        </div>

        <div v-if="erroGeral" class="alert alert-danger small mb-0" role="alert">{{ erroGeral }}</div>
      </form>
    </div>

    <div class="d-flex justify-content-end gap-2 p-3 border-top">
      <button type="button" class="btn btn-outline-secondary rounded-pill px-4" :disabled="salvando" @click="fechar">Cancelar</button>
      <button type="submit" form="formulario-produto" class="btn btn-primary rounded-pill px-4" :disabled="salvando">
        <span v-if="salvando" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
        {{ salvando ? 'Salvando...' : 'Salvar produto' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
// Mesmo módulo importado em main.js: reaproveita a instância do Bootstrap sem duplicar seus eventos
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.min.js'
import IconeSvg from '@/components/IconeSvg.vue'
import { useProdutorStore } from '@/stores/produtor.js'
import { formatarPreco } from '@/utils/formatacao.js'

const emit = defineEmits(['salvo'])

const produtorStore = useProdutorStore()
const painel = ref(null)
const campoImagem = ref(null)
const produtoEditado = ref(null)
const form = ref(formVazio())
const erros = ref({})
const erroGeral = ref('')
const salvando = ref(false)
const arquivoImagem = ref(null)
const previewImagem = ref('')
let offcanvas = null
let gatilho = null

const categoriaInativa = computed(() => {
  const produto = produtoEditado.value
  if (!produto || produtorStore.categorias.some(categoria => categoria.categoria_id === produto.categoria)) return null
  return { id: produto.categoria, nome: produto.categoria_nome }
})

// Prévia visual; o backend calcula e grava o preço com desconto
const precoFinal = computed(() => {
  const informado = String(form.value.precoVenda ?? '').replace(',', '.').trim()
  const base = informado !== '' ? Number(informado) : Number(produtoEditado.value?.preco_original ?? NaN)
  if (!Number.isFinite(base) || base <= 0) return null
  const desconto = Number(form.value.desconto) || 0
  return base - base * (desconto / 100)
})

onMounted(() => {
  offcanvas = bootstrap.Offcanvas.getOrCreateInstance(painel.value)
  painel.value.addEventListener('hidden.bs.offcanvas', aoFechar)
})

// Ao sair da rota com o painel aberto (ex.: botão voltar), fecha antes de descartar;
// dispose() sozinho deixaria a rolagem da página bloqueada pelo Bootstrap.
onBeforeUnmount(() => {
  const elemento = painel.value
  const instancia = offcanvas
  elemento.removeEventListener('hidden.bs.offcanvas', aoFechar)
  if (elemento.classList.contains('show')) {
    elemento.addEventListener('hidden.bs.offcanvas', () => instancia.dispose(), { once: true })
    instancia.hide()
  } else {
    instancia.dispose()
  }
  limparImagem()
})

function formVazio() {
  return { nome: '', descricao: '', estoque: 0, categoria: '', precoVenda: '', desconto: '', ativo: true }
}

function abrir(produto = null) {
  gatilho = document.activeElement
  produtoEditado.value = produto
  form.value = produto
    ? {
        nome: produto.nome,
        descricao: produto.descricao || '',
        estoque: produto.estoque,
        categoria: produto.categoria,
        precoVenda: '',
        desconto: produto.desconto ?? '',
        ativo: produto.ativo,
      }
    : formVazio()
  erros.value = {}
  erroGeral.value = ''
  limparImagem()
  previewImagem.value = produto?.imagem || ''
  if (campoImagem.value) campoImagem.value.value = ''
  offcanvas.show()
}

function fechar() {
  if (!salvando.value) offcanvas.hide()
}

// Aberto por código, o offcanvas não devolve o foco sozinho; volta para o botão que o abriu
function aoFechar() {
  limparImagem()
  if (gatilho?.isConnected) gatilho.focus()
  gatilho = null
}

function selecionarImagem(evento) {
  const arquivo = evento.target.files?.[0]
  limparImagem()
  arquivoImagem.value = arquivo || null
  previewImagem.value = arquivo ? URL.createObjectURL(arquivo) : produtoEditado.value?.imagem || ''
}

function limparImagem() {
  if (previewImagem.value.startsWith('blob:')) URL.revokeObjectURL(previewImagem.value)
  arquivoImagem.value = null
}

function validar() {
  const novosErros = {}
  if (!form.value.nome) novosErros.nome = 'Informe o nome do produto.'
  if (!form.value.categoria) novosErros.categoria = 'Selecione uma categoria.'
  if (!Number.isInteger(form.value.estoque) || form.value.estoque < 0) novosErros.estoque = 'Informe um estoque igual ou maior que zero.'

  const preco = String(form.value.precoVenda ?? '').replace(',', '.').trim()
  if (!produtoEditado.value && preco === '') novosErros.precoVenda = 'Informe o preço de venda.'
  else if (preco !== '' && !(Number(preco) > 0)) novosErros.precoVenda = 'Informe um preço maior que zero.'

  const desconto = form.value.desconto
  if (desconto !== '' && desconto !== null && !(Number(desconto) >= 0 && Number(desconto) <= 100)) {
    novosErros.desconto = 'Informe um desconto entre 0 e 100%.'
  }

  erros.value = novosErros
  return Object.keys(novosErros).length === 0
}

async function salvar() {
  erroGeral.value = ''
  if (!validar()) return

  salvando.value = true
  try {
    const { erroImagem } = await produtorStore.salvarProduto({
      dados: {
        nome: form.value.nome,
        descricao: form.value.descricao,
        estoque: form.value.estoque,
        categoria: form.value.categoria,
        ativo: form.value.ativo,
      },
      precoVenda: form.value.precoVenda,
      desconto: form.value.desconto,
      arquivoImagem: arquivoImagem.value,
      produtoExistente: produtoEditado.value,
    })
    emit('salvo', { editado: !!produtoEditado.value, erroImagem })
    salvando.value = false
    offcanvas.hide()
  } catch (falha) {
    erroGeral.value = falha.message
  } finally {
    salvando.value = false
  }
}

defineExpose({ abrir })
</script>

<style scoped>
.painel-formulario {
  --bs-offcanvas-width: min(34rem, 100vw);
}
.imagem-preview {
  width: 4.5rem;
  height: 4.5rem;
  object-fit: cover;
  flex-shrink: 0;
}
</style>
