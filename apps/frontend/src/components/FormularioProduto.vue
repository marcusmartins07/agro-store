<template>
  <div
    ref="painel"
    class="offcanvas offcanvas-end painel-formulario"
    tabindex="-1"
    aria-labelledby="titulo-formulario-produto"
  >
    <div class="offcanvas-header border-bottom">
      <h2 id="titulo-formulario-produto" class="offcanvas-title h4 fw-semibold">
        {{ ajuste ? 'Ajustar imagem' : produtoEditado ? 'Editar produto' : 'Novo produto' }}
      </h2>
      <button type="button" class="btn-close" aria-label="Fechar" :disabled="salvando" @click="fechar"></button>
    </div>

    <div class="offcanvas-body">
      <EditorEnquadramento
        v-if="ajuste"
        :src="ajuste.src"
        :enquadramento-inicial="ajuste.enquadramento"
        :nome-arquivo="ajuste.nomeArquivo"
        :erro-externo="ajuste.erro"
        @aplicar="aplicarAjuste"
        @cancelar="fecharAjuste"
      />

      <form v-show="!ajuste" id="formulario-produto" novalidate @submit.prevent="salvar">
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
          <label for="produto-imagem" class="form-label">
            Imagens do produto <span class="text-body-secondary fw-normal">({{ imagens.length }} de {{ LIMITE_IMAGENS }})</span>
          </label>

          <ul v-if="imagens.length" class="list-unstyled d-flex flex-wrap gap-2 mb-2">
            <li v-for="(imagem, indice) in imagens" :key="imagem.chave" class="cartao-imagem rounded-3 border p-1">
              <div class="position-relative">
                <img :src="imagem.src" :alt="`Imagem ${indice + 1} do produto`" class="imagem-preview rounded-2">
                <span v-if="imagem.chave === chavePrincipal" class="badge text-bg-primary selo-principal">Principal</span>
                <button
                  type="button"
                  class="btn btn-sm btn-remover-imagem"
                  :aria-label="`Remover imagem ${indice + 1}`"
                  title="Remover imagem"
                  @click="removerImagem(indice)"
                >
                  <IconeSvg nome="lixeira" :tamanho="14" />
                </button>
              </div>
              <div class="d-flex justify-content-between mt-1">
                <button
                  type="button"
                  class="btn btn-sm btn-acao"
                  :disabled="indice === 0"
                  :aria-label="`Mover imagem ${indice + 1} para a esquerda`"
                  @click="moverImagem(indice, -1)"
                >
                  <IconeSvg nome="seta-esquerda" :tamanho="14" />
                </button>
                <button
                  type="button"
                  class="btn btn-sm btn-acao"
                  :class="{ 'text-primary': imagem.chave === chavePrincipal }"
                  :aria-label="`Definir imagem ${indice + 1} como principal`"
                  :aria-pressed="imagem.chave === chavePrincipal"
                  @click="chavePrincipal = imagem.chave"
                >
                  <IconeSvg nome="estrela" :tamanho="14" :preenchido="imagem.chave === chavePrincipal" />
                </button>
                <button
                  type="button"
                  class="btn btn-sm btn-acao"
                  :aria-label="`Ajustar enquadramento da imagem ${indice + 1}`"
                  title="Ajustar enquadramento"
                  @click="abrirAjuste(indice)"
                >
                  <IconeSvg nome="recortar" :tamanho="14" />
                </button>
                <button
                  type="button"
                  class="btn btn-sm btn-acao"
                  :disabled="indice === imagens.length - 1"
                  :aria-label="`Mover imagem ${indice + 1} para a direita`"
                  @click="moverImagem(indice, 1)"
                >
                  <IconeSvg nome="seta-direita" :tamanho="14" />
                </button>
              </div>
            </li>
          </ul>

          <input
            id="produto-imagem"
            ref="campoImagem"
            type="file"
            multiple
            class="form-control"
            :class="{ 'is-invalid': erros.imagens }"
            accept="image/jpeg,image/png,image/webp"
            :disabled="imagens.length >= LIMITE_IMAGENS"
            aria-describedby="ajuda-produto-imagem erro-produto-imagem"
            @change="selecionarImagens"
          >
          <div id="erro-produto-imagem" class="invalid-feedback">{{ erros.imagens }}</div>
          <div id="ajuda-produto-imagem" class="form-text">
            Opcional. Até {{ LIMITE_IMAGENS }} imagens JPG, PNG ou WEBP com até 5 MB cada.
            A imagem principal (<IconeSvg nome="estrela" :tamanho="12" preenchido />) aparece no catálogo.
          </div>
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

    <div v-if="!ajuste" class="d-flex justify-content-end gap-2 p-3 border-top">
      <button type="button" class="btn btn-outline-secondary rounded-pill px-4" :disabled="salvando" @click="fechar">Cancelar</button>
      <button type="submit" form="formulario-produto" class="btn btn-primary rounded-pill px-4" :disabled="salvando">
        <span v-if="salvando" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
        {{ salvando ? 'Salvando...' : 'Salvar produto' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.min.js'
import EditorEnquadramento from '@/components/EditorEnquadramento.vue'
import IconeSvg from '@/components/IconeSvg.vue'
import { useProdutorStore } from '@/stores/produtor.js'
import { formatarPreco } from '@/utils/formatacao.js'
import { carregarImagemParaEdicao } from '@/utils/imagem.js'

const LIMITE_IMAGENS = 5

const emit = defineEmits(['salvo'])

const produtorStore = useProdutorStore()
const painel = ref(null)
const campoImagem = ref(null)
const produtoEditado = ref(null)
const form = ref(formVazio())
const erros = ref({})
const erroGeral = ref('')
const salvando = ref(false)
// Cada item: { chave, src, id } para imagens já salvas ou { chave, src, arquivo } para novas.
// Novas que passaram pelo editor guardam também srcOriginal (sem recorte), nomeOriginal e o enquadramento escolhido.
const imagens = ref([])
const chavePrincipal = ref(null)
const imagensRemovidas = ref([])
// Imagem aberta no editor: { chave, src, enquadramento, nomeArquivo, erro, srcBaixada }
const ajuste = ref(null)
let contadorImagensNovas = 0
let offcanvas = null
let gatilho = null

const categoriaInativa = computed(() => {
  const produto = produtoEditado.value
  if (!produto || produtorStore.categorias.some(categoria => categoria.categoria_id === produto.categoria)) return null
  return { id: produto.categoria, nome: produto.categoria_nome }
})

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
  descartarAjuste()
  liberarPreviews()
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
  carregarImagens(produto?.imagens || [])
  if (campoImagem.value) campoImagem.value.value = ''
  offcanvas.show()
}

function fechar() {
  if (!salvando.value) offcanvas.hide()
}

function aoFechar() {
  descartarAjuste()
  liberarPreviews()
  if (gatilho?.isConnected) gatilho.focus()
  gatilho = null
}

function carregarImagens(imagensSalvas) {
  descartarAjuste()
  liberarPreviews()
  imagens.value = imagensSalvas.map(imagem => ({ chave: `salva-${imagem.id}`, id: imagem.id, src: imagem.imagem }))
  chavePrincipal.value = imagens.value.find((_, indice) => imagensSalvas[indice].e_principal)?.chave ?? null
  imagensRemovidas.value = []
}

function selecionarImagens(evento) {
  const arquivos = Array.from(evento.target.files || [])
  const vagas = LIMITE_IMAGENS - imagens.value.length
  evento.target.value = ''

  erros.value = { ...erros.value, imagens: '' }
  const excedentes = arquivos.length - vagas
  if (excedentes > 0) {
    const resto = excedentes === 1 ? '1 não foi adicionada' : `${excedentes} não foram adicionadas`
    erros.value.imagens = `Cada produto pode ter até ${LIMITE_IMAGENS} imagens; ${resto}.`
  }

  for (const arquivo of arquivos.slice(0, vagas)) {
    contadorImagensNovas += 1
    imagens.value.push({ chave: `nova-${contadorImagensNovas}`, arquivo, src: URL.createObjectURL(arquivo) })
  }
  if (!chavePrincipal.value) chavePrincipal.value = imagens.value[0]?.chave ?? null
}

function moverImagem(indice, direcao) {
  const lista = [...imagens.value]
  const destino = indice + direcao
  ;[lista[indice], lista[destino]] = [lista[destino], lista[indice]]
  imagens.value = lista
}

function removerImagem(indice) {
  const [removida] = imagens.value.splice(indice, 1)
  if (removida.id) imagensRemovidas.value.push(removida.id)
  else liberarUrls(removida)

  if (removida.chave === chavePrincipal.value) chavePrincipal.value = imagens.value[0]?.chave ?? null
  if (erros.value.imagens) erros.value = { ...erros.value, imagens: '' }
}

// Novas imagens reabrem a partir do arquivo original; as já salvas são baixadas para o editor
async function abrirAjuste(indice) {
  const item = imagens.value[indice]
  ajuste.value = {
    chave: item.chave,
    src: item.id ? null : item.srcOriginal ?? item.src,
    enquadramento: item.enquadramento ?? null,
    nomeArquivo: item.nomeOriginal ?? item.arquivo?.name ?? nomeDaUrl(item.src),
    erro: '',
    srcBaixada: null,
  }
  await nextTick()
  painel.value.querySelector('.offcanvas-body').scrollTop = 0
  painel.value.querySelector('.editor-enquadramento [tabindex], .editor-enquadramento button')?.focus({ preventScroll: true })
  if (!item.id) return

  const chave = item.chave
  try {
    const srcBaixada = await carregarImagemParaEdicao(item.src)
    if (ajuste.value?.chave !== chave) return URL.revokeObjectURL(srcBaixada)
    ajuste.value = { ...ajuste.value, src: srcBaixada, srcBaixada }
  } catch (falha) {
    if (ajuste.value?.chave === chave) ajuste.value = { ...ajuste.value, erro: falha.message }
  }
}

function aplicarAjuste({ arquivo, enquadramento }) {
  const indice = imagens.value.findIndex(imagem => imagem.chave === ajuste.value.chave)
  const item = imagens.value[indice]
  const src = URL.createObjectURL(arquivo)

  if (item.id) {
    contadorImagensNovas += 1
    const novaChave = `nova-${contadorImagensNovas}`
    imagens.value.splice(indice, 1, {
      chave: novaChave, arquivo, src, srcOriginal: ajuste.value.srcBaixada, enquadramento, nomeOriginal: ajuste.value.nomeArquivo,
    })
    imagensRemovidas.value.push(item.id)
    if (chavePrincipal.value === item.chave) chavePrincipal.value = novaChave
  } else {
    if (item.srcOriginal) URL.revokeObjectURL(item.src)
    imagens.value.splice(indice, 1, {
      ...item, arquivo, src, srcOriginal: item.srcOriginal ?? item.src, enquadramento, nomeOriginal: item.nomeOriginal ?? item.arquivo.name,
    })
  }

  ajuste.value = null
  devolverFocoAoAjuste(indice)
}

function fecharAjuste() {
  const indice = imagens.value.findIndex(imagem => imagem.chave === ajuste.value.chave)
  descartarAjuste()
  devolverFocoAoAjuste(indice)
}

function descartarAjuste() {
  if (ajuste.value?.srcBaixada) URL.revokeObjectURL(ajuste.value.srcBaixada)
  ajuste.value = null
}

async function devolverFocoAoAjuste(indice) {
  await nextTick()
  painel.value.querySelector(`[aria-label="Ajustar enquadramento da imagem ${indice + 1}"]`)?.focus()
}

function nomeDaUrl(url) {
  return decodeURIComponent(url.split('?')[0].split('/').pop() || 'imagem')
}

function liberarUrls(imagem) {
  for (const url of [imagem.src, imagem.srcOriginal]) {
    if (url?.startsWith('blob:')) URL.revokeObjectURL(url)
  }
}

function liberarPreviews() {
  for (const imagem of imagens.value) liberarUrls(imagem)
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
      imagens: { itens: imagens.value, chavePrincipal: chavePrincipal.value, removidas: imagensRemovidas.value },
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
  display: block;
  width: 5.5rem;
  height: 5.5rem;
  object-fit: cover;
}
.cartao-imagem {
  width: 6.25rem;
  background-color: var(--cor-superficie);
}
.selo-principal {
  position: absolute;
  top: 0.25rem;
  left: 0.25rem;
  font-size: 0.65rem;
}
.btn-acao {
  padding: 0.15rem 0.2rem;
  line-height: 1;
  border: 0;
  color: var(--cor-texto);
}
.btn-acao:hover:not(:disabled) {
  background-color: var(--cor-apoio);
}
.btn-remover-imagem {
  position: absolute;
  top: 0.25rem;
  right: 0.25rem;
  padding: 0.15rem 0.25rem;
  line-height: 1;
  border: 0;
  color: var(--bs-danger);
  background-color: var(--cor-superficie);
}
.btn-remover-imagem:hover {
  color: var(--bs-danger);
  background-color: var(--cor-apoio);
}
.btn-acao:focus-visible,
.btn-remover-imagem:focus-visible {
  outline: 2px solid var(--cor-foco);
  outline-offset: 1px;
}
</style>
