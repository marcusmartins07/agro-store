<template>
  <div>
    <h1 class="fw-semibold mb-4">Carrinho</h1>

    <div v-if="!authStore.estaLogado" class="card rounded-4 text-center py-5">
      <div class="card-body">
        <span class="icone-estado mb-3"><IconeSvg nome="cesta" :tamanho="32" /></span>
        <h2 class="h4 fw-semibold mb-2">Entre para usar o carrinho</h2>
        <p class="text-body-secondary mb-3">Seu carrinho fica salvo na sua conta.</p>
        <RouterLink :to="{ name: 'login', query: { retorno: route.fullPath } }" class="btn btn-primary rounded-pill px-4">Entrar</RouterLink>
      </div>
    </div>

    <div v-else-if="carrinhoStore.carregando && carrinhoStore.itens.length === 0" class="card rounded-4 text-center py-5">
      <div class="card-body text-body-secondary" role="status">Carregando carrinho...</div>
    </div>

    <div v-else-if="erroCarregamento && carrinhoStore.itens.length === 0" class="card rounded-4 text-center py-5">
      <div class="card-body" role="alert">
        <h2 class="h4 fw-semibold mb-2">Não foi possível carregar o carrinho</h2>
        <p class="text-body-secondary mb-3">{{ erroCarregamento }}</p>
        <button type="button" class="btn btn-primary rounded-pill px-4" @click="carregarCarrinho">Tentar novamente</button>
      </div>
    </div>

    <div v-else-if="carrinhoStore.itens.length === 0" class="card rounded-4 text-center py-5">
      <div class="card-body">
        <span class="icone-estado mb-3"><IconeSvg nome="cesta" :tamanho="32" /></span>
        <h2 class="h4 fw-semibold mb-2">Seu carrinho está vazio</h2>
        <p class="text-body-secondary mb-3">Você ainda não adicionou nenhum produto ao carrinho.</p>
        <RouterLink :to="{ name: 'produtos' }" class="btn btn-primary rounded-pill px-4">Explorar produtos</RouterLink>
      </div>
    </div>

    <div v-else class="row g-4">
      <div class="col-12 col-lg-8 d-flex flex-column gap-4">
        <div v-if="mensagemErro" class="alert alert-danger mb-0" role="alert">{{ mensagemErro }}</div>

        <section v-for="grupo in lojasDoCarrinho" :key="grupo.fornecedor" class="card rounded-4">
          <div class="card-body p-3 p-md-4">
            <h2 class="h6 fw-semibold text-body-secondary d-flex align-items-center gap-2 mb-1 titulo-loja">
              <IconeSvg nome="loja" :tamanho="16" />
              {{ grupo.fornecedor }}
            </h2>

            <ul class="list-unstyled mb-0">
              <li
                v-for="item in grupo.itens"
                :key="item.carrinho_produto_id"
                class="item-carrinho d-flex flex-wrap flex-sm-nowrap align-items-center gap-3 py-3"
              >
                <input
                  :id="`selecionar-${item.carrinho_produto_id}`"
                  class="form-check-input item-checkbox flex-shrink-0 m-0"
                  type="checkbox"
                  :checked="item.situacao.finalizavel && selecionados.has(item.carrinho_produto_id)"
                  :disabled="!item.situacao.finalizavel"
                  :aria-describedby="item.situacao.texto ? idSituacao(item) : undefined"
                  @change="alternarSelecao(item.carrinho_produto_id)"
                />
                <label :for="`selecionar-${item.carrinho_produto_id}`" class="visually-hidden">
                  Incluir {{ item.produto_nome }} na finalização
                </label>

                <span class="miniatura imagem-placeholder rounded-3 flex-shrink-0" aria-hidden="true">
                  <IconeSvg nome="imagem" :tamanho="22" />
                </span>

                <div class="flex-grow-1 info-item">
                  <RouterLink :to="{ name: 'produto', params: { id: item.produto } }" class="fw-semibold link-produto">
                    {{ item.produto_nome }}
                  </RouterLink>
                  <p class="small text-body-secondary mb-0">{{ formatarPreco(precoUnitario(item)) }} cada</p>
                  <div
                    v-if="item.situacao.texto"
                    :id="idSituacao(item)"
                    class="d-flex flex-wrap align-items-center gap-2 mt-1"
                  >
                    <SeloStatus
                      v-if="item.situacao.selo"
                      :status="item.situacao.selo"
                      :variante="item.situacao.variante"
                      class="text-wrap"
                    />
                    <span class="small text-body-secondary">{{ item.situacao.texto }}</span>
                  </div>
                </div>

                <div class="acoes-item d-flex align-items-center justify-content-end gap-3 ms-auto">
                  <SeletorQuantidade
                    :model-value="Number(item.quantidade)"
                    :max="limiteEstoque(item)"
                    :disabled="salvando || item.disponivel === false"
                    :rotulo="item.produto_nome"
                    compacto
                    @update:model-value="quantidade => alterarQuantidade(item, quantidade)"
                  />
                  <span
                    class="fw-bold text-end subtotal"
                    :class="{ 'text-body-secondary': !item.situacao.finalizavel }"
                  >{{ formatarPreco(item.subtotal) }}</span>
                  <button
                    type="button"
                    class="btn btn-link p-1 botao-remover"
                    :disabled="salvando"
                    :aria-label="`Remover ${item.produto_nome} do carrinho`"
                    @click="remover(item.carrinho_produto_id)"
                  >
                    <IconeSvg nome="lixeira" :tamanho="18" />
                  </button>
                </div>
              </li>
            </ul>
          </div>
        </section>
      </div>

      <div class="col-12 col-lg-4">
        <aside class="bg-apoio rounded-4 p-4 resumo" aria-labelledby="titulo-resumo">
          <h2 id="titulo-resumo" class="h4 fw-semibold mb-3">Resumo</h2>

          <ul v-if="resumoPorFornecedor.length > 1" class="list-unstyled small text-body-secondary border-bottom pb-3 mb-3">
            <li class="mb-1">Será gerado um pedido para cada loja:</li>
            <li v-for="grupo in resumoPorFornecedor" :key="grupo.fornecedor" class="d-flex justify-content-between gap-2">
              <span>{{ grupo.fornecedor }}</span>
              <span>{{ formatarPreco(grupo.total) }}</span>
            </li>
          </ul>

          <p v-if="textoNaoFinalizaveis" class="small text-body-secondary mb-3">{{ textoNaoFinalizaveis }}</p>

          <dl class="mb-0">
            <div class="d-flex justify-content-between small mb-2">
              <dt class="fw-normal">Itens selecionados</dt>
              <dd class="mb-0">{{ totalSelecionados }}</dd>
            </div>
            <div class="d-flex justify-content-between small mb-2">
              <dt class="fw-normal">Subtotal</dt>
              <dd class="mb-0">{{ formatarPreco(valorBrutoSelecionado) }}</dd>
            </div>
            <div class="d-flex justify-content-between small mb-3">
              <dt class="fw-normal">Descontos</dt>
              <dd class="mb-0">- {{ formatarPreco(descontoSelecionado) }}</dd>
            </div>
            <div class="d-flex justify-content-between fs-5 fw-bold border-top pt-3">
              <dt>Total</dt>
              <dd class="mb-0 text-primary">{{ formatarPreco(totalSelecionado) }}</dd>
            </div>
          </dl>

          <p class="d-flex align-items-start gap-2 small text-body-secondary my-3">
            <IconeSvg nome="local" :tamanho="16" />
            <span>{{ textoRetirada() }}</span>
          </p>

          <div v-if="erroFinalizacao" class="alert alert-danger small mb-3" role="alert">{{ erroFinalizacao }}</div>

          <button
            type="button"
            class="btn btn-primary btn-lg rounded-pill w-100 fw-semibold"
            :disabled="finalizando || totalSelecionados === 0"
            @click="finalizarPedido"
          >
            <span v-if="finalizando" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
            {{ finalizando ? 'Finalizando...' : 'Finalizar pedido' }}
          </button>
          <RouterLink :to="{ name: 'produtos' }" class="btn btn-outline-secondary rounded-pill w-100 mt-2">Continuar comprando</RouterLink>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import IconeSvg from '@/components/IconeSvg.vue'
import SeloStatus from '@/components/SeloStatus.vue'
import SeletorQuantidade from '@/components/SeletorQuantidade.vue'
import { useAuthStore } from '@/stores/auth.js'
import { useCarrinhoStore } from '@/stores/index.js'
import { textoRetirada } from '@/data/feira.js'
import { formatarPreco } from '@/utils/formatacao.js'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const carrinhoStore = useCarrinhoStore()
const selecionados = ref(new Set())
const salvando = ref(false)
const finalizando = ref(false)
const mensagemErro = ref('')
const erroCarregamento = ref('')
const erroFinalizacao = ref('')

const lojasDoCarrinho = computed(() =>
  Object.entries(carrinhoStore.porFornecedor).map(([fornecedor, itens]) => ({
    fornecedor,
    itens: itens.map(item => ({ ...item, situacao: descreverSituacao(item) })),
  }))
)

const itensSelecionados = computed(() =>
  carrinhoStore.itens.filter(item => selecionados.value.has(item.carrinho_produto_id) && podeFinalizar(item))
)

const totalSelecionados = computed(() => somar(itensSelecionados.value, item => Number(item.quantidade || 0)))
const totalSelecionado = computed(() => somar(itensSelecionados.value, item => Number(item.subtotal || 0)))
const valorBrutoSelecionado = computed(() =>
  somar(itensSelecionados.value, item => Number(item.valor_unitario || 0) * Number(item.quantidade || 0))
)
const descontoSelecionado = computed(() =>
  somar(itensSelecionados.value, item => Number(item.valor_desconto || 0) * Number(item.quantidade || 0))
)

const resumoPorFornecedor = computed(() => {
  const grupos = {}
  for (const item of itensSelecionados.value) {
    const fornecedor = item.loja_nome || 'Fornecedor'
    grupos[fornecedor] = (grupos[fornecedor] || 0) + Number(item.subtotal || 0)
  }
  return Object.entries(grupos).map(([fornecedor, total]) => ({ fornecedor, total }))
})

const textoNaoFinalizaveis = computed(() => {
  const quantidade = carrinhoStore.itens.filter(item => !podeFinalizar(item)).length
  if (quantidade === 0) return ''
  if (quantidade === 1) return '1 item do carrinho não entra no pedido. Veja a situação indicada na lista.'
  return `${quantidade} itens do carrinho não entram no pedido. Veja a situação indicada na lista.`
})

onMounted(async () => {
  if (authStore.estaLogado) await carregarCarrinho()
})

// Mantém selecionados só os itens que ainda existem e podem ser finalizados (ex.: estoque zerado após recarregar)
watch(() => carrinhoStore.itens, () => {
  const idsFinalizaveis = new Set(carrinhoStore.itens.filter(podeFinalizar).map(item => item.carrinho_produto_id))
  selecionados.value = new Set([...selecionados.value].filter(id => idsFinalizaveis.has(id)))
})

function somar(itens, valorDoItem) {
  return itens.reduce((total, item) => total + valorDoItem(item), 0)
}

function precoUnitario(item) {
  if (item.valor_unitario === null || item.valor_unitario === undefined) return null
  return Number(item.valor_unitario) - Number(item.valor_desconto || 0)
}

function limiteEstoque(item) {
  return item.estoque === null || item.estoque === undefined ? Infinity : Number(item.estoque)
}

function descreverSituacao(item) {
  const estoque = limiteEstoque(item)

  if (item.disponivel === false && estoque > 0) {
    return {
      finalizavel: false,
      selo: 'Indisponível',
      variante: 'cancelado',
      texto: 'Produto ou loja indisponível no momento. Remova o item do carrinho.',
    }
  }
  if (item.disponivel === false) {
    return {
      finalizavel: false,
      selo: 'Sem estoque',
      variante: 'cancelado',
      texto: 'Não entra no pedido. Remova o item ou aguarde a reposição.',
    }
  }
  if (Number(item.quantidade) === 0) {
    const limite = Number.isFinite(estoque) ? ` (até ${estoque})` : ''
    return {
      finalizavel: false,
      selo: 'Disponível novamente',
      variante: 'pronto',
      texto: `Aumente a quantidade para incluir no pedido${limite}.`,
    }
  }

  const noLimite = Number(item.quantidade) >= estoque
  return { finalizavel: true, selo: '', variante: '', texto: noLimite ? `Máximo disponível: ${estoque}` : '' }
}

function podeFinalizar(item) {
  return descreverSituacao(item).finalizavel
}

function idSituacao(item) {
  return `situacao-${item.carrinho_produto_id}`
}

function idsFinalizaveis() {
  return carrinhoStore.itens.filter(podeFinalizar).map(item => item.carrinho_produto_id)
}

async function carregarCarrinho() {
  mensagemErro.value = ''
  erroCarregamento.value = ''
  try {
    await carrinhoStore.carregar()
    selecionados.value = new Set(idsFinalizaveis())
  } catch (e) {
    // Sem itens já carregados, a falha vira o estado de erro da tela; com itens, um alerta sobre a lista
    if (carrinhoStore.itens.length === 0) {
      erroCarregamento.value = carrinhoStore.erro || 'Não foi possível concluir a operação.'
    } else {
      mensagemErro.value = carrinhoStore.erro
    }
  }
}

function alternarSelecao(itemId) {
  erroFinalizacao.value = ''
  const proximos = new Set(selecionados.value)
  if (proximos.has(itemId)) {
    proximos.delete(itemId)
  } else {
    proximos.add(itemId)
  }
  selecionados.value = proximos
}

async function alterarQuantidade(item, quantidade) {
  if (quantidade < 1) return

  const estavaSemQuantidade = Number(item.quantidade) === 0
  mensagemErro.value = ''
  erroFinalizacao.value = ''
  salvando.value = true
  try {
    await carrinhoStore.alterarQuantidade(item.carrinho_produto_id, quantidade)
    // Após a reposição, o item que volta de 0 para 1 ou mais retorna marcado para finalizar
    const atualizado = carrinhoStore.itens.find(atual => atual.carrinho_produto_id === item.carrinho_produto_id)
    if (estavaSemQuantidade && atualizado && podeFinalizar(atualizado)) {
      selecionados.value = new Set([...selecionados.value, item.carrinho_produto_id])
    }
  } catch (e) {
    mensagemErro.value = carrinhoStore.erro
  } finally {
    salvando.value = false
  }
}

async function remover(itemId) {
  mensagemErro.value = ''
  erroFinalizacao.value = ''
  salvando.value = true
  try {
    await carrinhoStore.remover(itemId)
    const proximos = new Set(selecionados.value)
    proximos.delete(itemId)
    selecionados.value = proximos
  } catch (e) {
    mensagemErro.value = carrinhoStore.erro
  } finally {
    salvando.value = false
  }
}

async function finalizarPedido() {
  const ids = itensSelecionados.value.map(item => item.carrinho_produto_id)
  if (ids.length === 0) return

  mensagemErro.value = ''
  erroFinalizacao.value = ''
  finalizando.value = true
  try {
    await carrinhoStore.finalizar(ids)
    selecionados.value = new Set()
    router.push({ name: 'pedidos' })
  } catch (e) {
    erroFinalizacao.value = carrinhoStore.erro
  } finally {
    finalizando.value = false
  }
}
</script>

<style scoped>
.titulo-loja {
  font-family: var(--fonte-texto);
}
.item-carrinho + .item-carrinho {
  border-top: 1px solid var(--cor-borda);
}
.item-checkbox {
  width: 1.125rem;
  height: 1.125rem;
}
.miniatura {
  width: 4rem;
  height: 4rem;
}
/* Base 0: nomes e textos de situação longos quebram dentro da coluna, sem empurrar as informações para baixo da miniatura */
.info-item {
  flex-basis: 0;
  min-width: 0;
  overflow-wrap: anywhere;
}
/* No celular, seletor, subtotal e remover sempre ocupam a segunda linha do item */
@media (max-width: 575.98px) {
  .acoes-item {
    flex-basis: 100%;
  }
}
.link-produto:hover {
  color: var(--cor-primaria);
}
.subtotal {
  min-width: 5.5rem;
}
.botao-remover {
  color: var(--cor-texto-secundario);
}
.botao-remover:hover:not(:disabled) {
  color: var(--danger);
}
@media (min-width: 992px) {
  .resumo {
    position: sticky;
    top: 6.5rem;
  }
}
</style>
