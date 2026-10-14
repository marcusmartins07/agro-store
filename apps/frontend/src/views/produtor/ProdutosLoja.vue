<template>
  <div>
    <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
      <div>
        <h2 class="h4 fw-semibold mb-1">Produtos da loja</h2>
        <p class="small text-body-secondary mb-0">
          Produtos desativados saem do catálogo, mas continuam no histórico dos pedidos.
        </p>
      </div>
      <div class="d-flex gap-2" role="group" aria-label="Filtrar produtos">
        <button
          v-for="opcao in opcoesFiltro"
          :key="opcao.valor"
          type="button"
          class="btn btn-sm rounded-pill px-3"
          :class="opcao.valor === filtro ? 'btn-primary' : 'btn-outline-secondary'"
          :aria-pressed="opcao.valor === filtro"
          @click="filtro = opcao.valor"
        >
          {{ opcao.rotulo }} <span class="opacity-75">({{ opcao.quantidade }})</span>
        </button>
      </div>
    </div>

    <div v-if="produtorStore.produtos.length === 0" class="card rounded-4 text-center py-5">
      <div class="card-body">
        <span class="icone-estado mb-3"><IconeSvg nome="pacote" :tamanho="32" /></span>
        <h3 class="h4 fw-semibold mb-2">Nenhum produto cadastrado</h3>
        <p class="text-body-secondary mb-3">Cadastre o primeiro produto da sua loja para aparecer no catálogo.</p>
        <button type="button" class="btn btn-primary rounded-pill px-4" @click="abrirFormulario()">Cadastrar produto</button>
      </div>
    </div>

    <div v-else-if="produtosFiltrados.length === 0" class="card rounded-4 text-center py-5">
      <div class="card-body">
        <p class="text-body-secondary mb-3">Nenhum produto {{ filtro === 'ativos' ? 'ativo' : 'inativo' }} no momento.</p>
        <button type="button" class="btn btn-outline-primary rounded-pill px-4" @click="filtro = 'todos'">Ver todos</button>
      </div>
    </div>

    <div v-else class="card rounded-4 overflow-hidden">
      <div class="table-responsive">
        <table class="table align-middle mb-0 tabela-produtos">
          <caption class="visually-hidden">Produtos da loja com preços, estoque e status</caption>
          <thead>
            <tr>
              <th scope="col">Produto</th>
              <th scope="col" class="d-none d-lg-table-cell">Categoria</th>
              <th scope="col" class="text-center">Estoque</th>
              <th scope="col" class="text-end d-none d-md-table-cell">Preço bruto</th>
              <th scope="col" class="text-center d-none d-md-table-cell">Desconto</th>
              <th scope="col" class="text-end">Preço líquido</th>
              <th scope="col">Status</th>
              <th scope="col"><span class="visually-hidden">Ações</span></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="produto in produtosFiltrados" :key="produto.produto_id">
              <td>
                <div class="d-flex align-items-center gap-3">
                  <img v-if="produto.imagem" :src="produto.imagem" alt="" class="miniatura rounded-3 border">
                  <span v-else class="miniatura imagem-placeholder rounded-3" aria-hidden="true"><IconeSvg nome="imagem" :tamanho="18" /></span>
                  <div class="info-produto">
                    <span class="fw-semibold d-block">{{ produto.nome }}</span>
                    <span class="small text-body-secondary">SKU {{ produto.sku || 'não gerado' }}</span>
                  </div>
                </div>
              </td>
              <td class="d-none d-lg-table-cell">{{ produto.categoria_nome }}</td>
              <td class="text-center">
                {{ produto.estoque }}
                <span v-if="produto.estoque === 0" class="d-block small text-danger">Sem estoque</span>
              </td>
              <td class="text-end d-none d-md-table-cell text-nowrap">{{ precoOuAviso(produto.preco_original) }}</td>
              <td class="text-center d-none d-md-table-cell">
                <span v-if="temDesconto(produto)" class="badge rounded-pill badge-destaque">-{{ produto.desconto }}%</span>
                <span v-else class="text-body-secondary">—</span>
              </td>
              <td class="text-end fw-semibold text-nowrap">{{ precoOuAviso(produto.preco) }}</td>
              <td><SeloStatus :status="produto.ativo ? 'Ativo' : 'Inativo'" :variante="produto.ativo ? 'entregue' : 'cancelado'" /></td>
              <td class="text-end">
                <div class="d-inline-flex gap-2">
                  <button
                    type="button"
                    class="btn btn-sm btn-outline-primary rounded-pill d-inline-flex align-items-center gap-1"
                    :aria-label="`Editar ${produto.nome}`"
                    @click="abrirFormulario(produto)"
                  >
                    <IconeSvg nome="lapis" :tamanho="14" /> <span class="d-none d-xl-inline">Editar</span>
                  </button>
                  <button
                    type="button"
                    class="btn btn-sm rounded-pill text-nowrap"
                    :class="produto.ativo ? 'btn-outline-danger' : 'btn-outline-secondary'"
                    :disabled="alternando === produto.produto_id"
                    @click="produto.ativo ? pedirDesativacao(produto) : alternarAtivo(produto)"
                  >
                    {{ produto.ativo ? 'Desativar' : 'Reativar' }}<span class="visually-hidden"> {{ produto.nome }}</span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <FormularioProduto ref="formulario" @salvo="aoSalvar" />

    <ModalConfirmacao
      ref="modalDesativar"
      titulo="Desativar produto"
      texto-confirmar="Desativar produto"
      texto-carregando="Desativando..."
      :carregando="alternando !== null"
      @confirmar="confirmarDesativacao"
    >
      <p class="mb-2"><strong>{{ produtoParaDesativar?.nome }}</strong> deixará de aparecer no catálogo e não poderá ser comprado.</p>
      <p class="small text-body-secondary mb-0">Os pedidos já realizados são preservados. Você pode reativá-lo a qualquer momento.</p>
    </ModalConfirmacao>
  </div>
</template>

<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import FormularioProduto from '@/components/FormularioProduto.vue'
import IconeSvg from '@/components/IconeSvg.vue'
import ModalConfirmacao from '@/components/ModalConfirmacao.vue'
import SeloStatus from '@/components/SeloStatus.vue'
import { useNotificacoesStore } from '@/stores/notificacoes.js'
import { useProdutorStore } from '@/stores/produtor.js'
import { formatarPreco, temDesconto } from '@/utils/formatacao.js'

const route = useRoute()
const router = useRouter()
const produtorStore = useProdutorStore()
const notificacoes = useNotificacoesStore()
const formulario = ref(null)
const modalDesativar = ref(null)
const filtro = ref('todos')
const alternando = ref(null)
const produtoParaDesativar = ref(null)

const opcoesFiltro = computed(() => [
  { valor: 'todos', rotulo: 'Todos', quantidade: produtorStore.produtos.length },
  { valor: 'ativos', rotulo: 'Ativos', quantidade: produtorStore.produtosAtivos },
  { valor: 'inativos', rotulo: 'Inativos', quantidade: produtorStore.produtosInativos },
])

const produtosFiltrados = computed(() => {
  const ordenados = [...produtorStore.produtos].sort((a, b) => a.nome.localeCompare(b.nome, 'pt-BR'))
  if (filtro.value === 'ativos') return ordenados.filter(produto => produto.ativo)
  if (filtro.value === 'inativos') return ordenados.filter(produto => !produto.ativo)
  return ordenados
})

// O botão "Novo produto" do topo chega aqui com ?novo=1
watch(() => route.query.novo, async (novo) => {
  if (novo !== '1') return
  await nextTick()
  abrirFormulario()
  router.replace({ name: 'produtos-produtor' })
}, { immediate: true })

function precoOuAviso(valor) {
  return valor === null || valor === undefined ? 'Sem preço' : formatarPreco(valor)
}

function abrirFormulario(produto = null) {
  formulario.value?.abrir(produto)
}

function aoSalvar({ editado, erroImagem }) {
  const mensagem = editado ? 'Produto atualizado.' : 'Produto cadastrado.'
  notificacoes.notificar(erroImagem
    ? { tipo: 'warning', mensagem: `${mensagem} Nem todas as imagens foram salvas: ${erroImagem}`, tempo: 8 }
    : { tipo: 'success', mensagem, tempo: 4 })
}

function pedirDesativacao(produto) {
  produtoParaDesativar.value = produto
  modalDesativar.value?.abrir()
}

async function confirmarDesativacao() {
  await alternarAtivo(produtoParaDesativar.value)
  modalDesativar.value?.fechar()
}

async function alternarAtivo(produto) {
  alternando.value = produto.produto_id
  try {
    const atualizado = await produtorStore.alternarAtivo(produto)
    notificacoes.notificar({
      tipo: 'success',
      mensagem: atualizado.ativo ? `${produto.nome} voltou ao catálogo.` : `${produto.nome} foi desativado.`,
      tempo: 4,
    })
  } catch (falha) {
    notificacoes.notificar({ tipo: 'danger', mensagem: falha.message })
  } finally {
    alternando.value = null
  }
}
</script>

<style scoped>
.miniatura {
  width: 3rem;
  height: 3rem;
  object-fit: cover;
  flex-shrink: 0;
}
.info-produto {
  min-width: 8rem;
}
.tabela-produtos {
  --bs-table-bg: var(--cor-superficie);
}
.tabela-produtos thead th {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--cor-texto-secundario);
  background-color: var(--cor-apoio);
  white-space: nowrap;
}
</style>
