<template>
  <section>
    <div class="d-flex justify-content-between align-items-start flex-wrap gap-3 mb-4">
      <div><h1 class="h2 fw-bold mb-1">Meus produtos</h1><p class="text-body-secondary mb-0">Cadastre, ajuste o estoque e controle a disponibilidade.</p></div>
      <button class="btn btn-success" @click="abrirNovo">Cadastrar produto</button>
    </div>

    <div v-if="carregando" class="card p-4 text-body-secondary">Carregando produtos...</div>
    <div v-else-if="erro" class="alert alert-danger">{{ erro }} <button class="btn btn-sm btn-outline-danger ms-2" @click="carregar">Tentar novamente</button></div>
    <div v-else-if="produtos.length === 0" class="card text-center p-5"><h2 class="h5 fw-bold">Nenhum produto cadastrado</h2><p class="text-body-secondary">Cadastre o primeiro produto da sua loja.</p><button class="btn btn-success align-self-center" @click="abrirNovo">Cadastrar produto</button></div>
    <div v-else class="card"><div class="table-responsive"><table class="table align-middle mb-0"><thead><tr><th>Produto</th><th>Categoria</th><th>Estoque</th><th>Preço atual</th><th>Status</th><th><span class="visually-hidden">Ações</span></th></tr></thead><tbody>
      <tr v-for="produto in produtos" :key="produto.produto_id"><td><div class="d-flex align-items-center gap-2"><img v-if="produto.imagem" :src="produto.imagem" alt="" class="imagem-miniatura rounded border"><div><strong>{{ produto.nome }}</strong><div class="small text-body-secondary">SKU: {{ produto.sku || 'Não informado' }}</div></div></div></td><td>{{ produto.categoria_nome }}</td><td>{{ produto.estoque }}</td><td>{{ formatarPreco(produto.preco) }}</td><td><span class="badge" :class="produto.ativo ? 'text-bg-success' : 'text-bg-secondary'">{{ produto.ativo ? 'Ativo' : 'Inativo' }}</span></td><td class="text-end"><button class="btn btn-sm btn-outline-success" @click="abrirEdicao(produto)">Editar</button></td></tr>
    </tbody></table></div></div>

    <div v-if="formAberto" class="modal-backdrop-custom" @click.self="fecharFormulario"><div class="card modal-card"><div class="card-body p-4">
      <div class="d-flex justify-content-between gap-3 mb-3"><h2 class="h4 mb-0">{{ produtoEditado ? 'Editar produto' : 'Cadastrar produto' }}</h2><button class="btn-close" aria-label="Fechar" @click="fecharFormulario"></button></div>
      <form @submit.prevent="salvar"><div class="row g-3">
        <div class="col-12 col-md-8"><label for="nome" class="form-label">Nome <span class="text-danger">*</span></label><input id="nome" v-model.trim="form.nome" class="form-control" required maxlength="155"></div>
        <div class="col-12 col-md-4"><label for="estoque" class="form-label">Estoque <span class="text-danger">*</span></label><input id="estoque" v-model.number="form.estoque" type="number" min="0" class="form-control" required></div>
        <div class="col-12"><label for="descricao" class="form-label">Descrição</label><textarea id="descricao" v-model.trim="form.descricao" rows="3" class="form-control"></textarea></div>
        <div class="col-12"><label for="imagem" class="form-label">Imagem do produto</label><div class="d-flex align-items-center gap-3"><img v-if="previewImagem" :src="previewImagem" alt="Pré-visualização da imagem do produto" class="imagem-preview rounded border"><input id="imagem" type="file" class="form-control" accept="image/jpeg,image/png,image/webp" @change="selecionarImagem"></div><div class="form-text">Opcional. JPG, PNG ou WEBP com até 5 MB.</div></div>
        <div class="col-12 col-md-6"><label for="categoria" class="form-label">Categoria <span class="text-danger">*</span></label><select id="categoria" v-model="form.categoria" class="form-select" required><option value="">Selecione</option><option v-for="categoria in categorias" :key="categoria.categoria_id" :value="categoria.categoria_id">{{ categoria.nome }}</option></select></div>
        <div class="col-12 col-md-6"><label for="preco" class="form-label">{{ produtoEditado ? 'Novo preço de venda' : 'Preço de venda' }} <span v-if="!produtoEditado" class="text-danger">*</span></label><input id="preco" v-model="form.precoVenda" inputmode="decimal" class="form-control" placeholder="0,00" :required="!produtoEditado"><div v-if="produtoEditado" class="form-text">Preencha somente para registrar um novo preço.</div></div><div class="col-12 col-md-6"><label for="desconto" class="form-label">Desconto percentual</label><input id="desconto" v-model.number="form.desconto" type="number" min="0" max="100" class="form-control" placeholder="Opcional"></div>
        <div v-if="produtoEditado" class="col-12"><div class="form-check"><input id="ativo" v-model="form.ativo" class="form-check-input" type="checkbox"><label for="ativo" class="form-check-label">Produto disponível para compra</label></div></div>
      </div><p v-if="erroFormulario" class="text-danger small mt-3 mb-0">{{ erroFormulario }}</p><div class="d-flex justify-content-end gap-2 mt-4"><button type="button" class="btn btn-outline-secondary" :disabled="salvando" @click="fecharFormulario">Cancelar</button><button class="btn btn-success" :disabled="salvando">{{ salvando ? 'Salvando...' : 'Salvar produto' }}</button></div></form>
    </div></div></div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/services/api.js'
import { useNotificacoesStore } from '@/stores/notificacoes.js'

const produtos = ref([]); const categorias = ref([]); const carregando = ref(true); const erro = ref(''); const formAberto = ref(false)
const produtoEditado = ref(null); const salvando = ref(false); const erroFormulario = ref('')
const arquivoImagem = ref(null); const previewImagem = ref('')
const notificacoes = useNotificacoesStore()
const formVazio = () => ({ nome: '', descricao: '', estoque: 0, categoria: '', precoVenda: '', desconto: null, ativo: true })
const form = ref(formVazio())
const formatarPreco = valor => Number(valor || 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
const mensagemErro = falha => {
  const dados = falha?.data; const campo = dados && Object.keys(dados)[0]
  return campo ? (Array.isArray(dados[campo]) ? dados[campo][0] : String(dados[campo])) : 'Não foi possível salvar o produto.'
}
async function carregar() { carregando.value = true; erro.value = ''; try { [produtos.value, categorias.value] = await Promise.all([api.produtos.listarMeus(), api.categorias.listar()]) } catch (falha) { erro.value = falha?.data?.detail || 'Não foi possível carregar os produtos.' } finally { carregando.value = false } }
function definirImagem(arquivo, preview) { if (previewImagem.value.startsWith('blob:')) URL.revokeObjectURL(previewImagem.value); arquivoImagem.value = arquivo; previewImagem.value = preview }
function abrirNovo() { produtoEditado.value = null; form.value = formVazio(); definirImagem(null, ''); erroFormulario.value = ''; formAberto.value = true }
function abrirEdicao(produto) { produtoEditado.value = produto; form.value = { ...formVazio(), ...produto, categoria: produto.categoria }; definirImagem(null, produto.imagem || ''); erroFormulario.value = ''; formAberto.value = true }
function fecharFormulario() { if (!salvando.value) formAberto.value = false }
function selecionarImagem(event) { const arquivo = event.target.files?.[0]; if (!arquivo) { definirImagem(null, produtoEditado.value?.imagem || ''); return } definirImagem(arquivo, URL.createObjectURL(arquivo)) }
function decimal(valor) { return String(valor).replace(',', '.').trim() }
async function enviarImagem(produtoId) { if (!arquivoImagem.value) return ''; try { await api.produtos.enviarImagem(produtoId, arquivoImagem.value); return '' } catch (falha) { return mensagemErro(falha) } }
async function salvar() { salvando.value = true; erroFormulario.value = ''; try { const produto = { nome: form.value.nome, descricao: form.value.descricao, estoque: form.value.estoque, categoria: form.value.categoria, ativo: form.value.ativo }; let produtoId; if (produtoEditado.value) { produtoId = produtoEditado.value.produto_id; await api.produtos.atualizar(produtoId, produto); if (form.value.precoVenda) await api.produtos.criarPreco({ produto: produtoId, preco_venda: decimal(form.value.precoVenda), porcentagem_desconto: form.value.desconto }) } else { const criado = await api.produtos.criar(produto); produtoId = criado.produto_id; await api.produtos.criarPreco({ produto: produtoId, preco_venda: decimal(form.value.precoVenda), porcentagem_desconto: form.value.desconto }) } const erroImagem = await enviarImagem(produtoId); const mensagem = produtoEditado.value ? 'Produto atualizado.' : 'Produto cadastrado.'; notificacoes.notificar(erroImagem ? { tipo: 'warning', mensagem: `${mensagem} A imagem não foi enviada: ${erroImagem}`, tempo: 8 } : { tipo: 'success', mensagem, tempo: 4 }); formAberto.value = false; definirImagem(null, ''); await carregar() } catch (falha) { erroFormulario.value = mensagemErro(falha) } finally { salvando.value = false } }
onMounted(carregar)
</script>

<style scoped>
.modal-backdrop-custom { position: fixed; inset: 0; z-index: 1050; display: grid; place-items: center; padding: 1rem; background: rgb(0 0 0 / 45%); }
.modal-card { width: min(720px, 100%); max-height: calc(100vh - 2rem); overflow: auto; }
.imagem-miniatura { width: 44px; height: 44px; object-fit: cover; flex-shrink: 0; }
.imagem-preview { width: 72px; height: 72px; object-fit: cover; flex-shrink: 0; }
</style>
