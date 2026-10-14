<template>
  <section>
    <div class="d-flex justify-content-between align-items-start flex-wrap gap-3 mb-4"><div><h1 class="h2 fw-bold mb-1">Pedidos da loja</h1><p class="text-body-secondary mb-0">Prepare os pedidos para retirada presencial.</p></div><RouterLink :to="{ name: 'minha-loja' }" class="btn btn-outline-success">Voltar ao painel</RouterLink></div>
    <div v-if="carregando" class="card p-4 text-body-secondary">Carregando pedidos...</div>
    <div v-else-if="erro" class="alert alert-danger">{{ erro }} <button class="btn btn-sm btn-outline-danger ms-2" @click="carregar">Tentar novamente</button></div>
    <div v-else-if="pedidos.length === 0" class="card text-center p-5"><h2 class="h5 fw-bold">Nenhum pedido para esta loja</h2><p class="text-body-secondary mb-0">Os pedidos recebidos aparecerão aqui.</p></div>
    <div v-else class="d-grid gap-3"><article v-for="pedido in pedidos" :key="pedido.pedido_id" class="card"><div class="card-body p-4"><div class="d-flex justify-content-between align-items-start flex-wrap gap-3 mb-3"><div><h2 class="h5 fw-bold mb-1">Pedido #{{ pedido.pedido_id }}</h2><p class="text-body-secondary mb-0">Cliente: {{ pedido.cliente?.nome }}<span v-if="pedido.cliente?.telefone"> · {{ formatarTelefone(pedido.cliente.telefone) }}</span></p></div><span class="badge text-bg-secondary">{{ pedido.status_nome }}</span></div><div class="table-responsive"><table class="table table-sm align-middle"><thead><tr><th>Produto</th><th class="text-center">Quantidade</th><th class="text-end">Subtotal</th></tr></thead><tbody><tr v-for="item in pedido.itens" :key="item.pedido_produto_id"><td>{{ item.nome_produto }}</td><td class="text-center">{{ item.quantidade }}</td><td class="text-end">{{ formatarPreco(item.subtotal) }}</td></tr></tbody></table></div><div class="d-flex justify-content-between align-items-center flex-wrap gap-3"><strong>Total: {{ formatarPreco(pedido.valor_liquido) }}</strong><div class="d-flex gap-2"><button v-for="proximo in proximosStatus(pedido.status_nome)" :key="proximo.nome" class="btn btn-sm" :class="proximo.cancelar ? 'btn-outline-danger' : 'btn-success'" :disabled="atualizando === pedido.pedido_id" @click="atualizarStatus(pedido, proximo)">{{ atualizando === pedido.pedido_id ? 'Atualizando...' : proximo.nome }}</button></div></div></div></article></div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/services/api.js'
import { useNotificacoesStore } from '@/stores/notificacoes.js'

const pedidos = ref([]); const carregando = ref(true); const erro = ref(''); const atualizando = ref(null)
const notificacoes = useNotificacoesStore()
const fluxo = { Pendente: [{ nome: 'Iniciar preparo', status: 'Em preparo' }, { nome: 'Cancelar', status: 'Cancelado', cancelar: true }], 'Em preparo': [{ nome: 'Pronto para retirada', status: 'Pronto para retirada' }, { nome: 'Cancelar', status: 'Cancelado', cancelar: true }], 'Pronto para retirada': [{ nome: 'Marcar como entregue', status: 'Entregue' }] }
const statusIds = ref({})
const formatarPreco = valor => Number(valor || 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
const formatarTelefone = telefone => telefone ? telefone.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3') : ''
function proximosStatus(status) { return fluxo[status] || [] }
async function carregar() { carregando.value = true; erro.value = ''; try { const [pedidosRecebidos, statusRecebidos] = await Promise.all([api.pedidos.listarMinhaLoja(), api.pedidos.listarStatusDisponiveis()]); pedidos.value = pedidosRecebidos; statusIds.value = Object.fromEntries(statusRecebidos.map(item => [item.status, item.status_pedido_id])) } catch (falha) { erro.value = falha?.data?.detail || 'Não foi possível carregar os pedidos.' } finally { carregando.value = false } }
async function atualizarStatus(pedido, proximo) { const statusId = statusIds.value[proximo.status]; if (!statusId) { notificacoes.notificar({ tipo: 'danger', mensagem: 'O status necessário ainda não está disponível.' }); return } if (proximo.cancelar && !window.confirm('Cancelar este pedido?')) return; atualizando.value = pedido.pedido_id; try { await api.pedidos.atualizarStatus(pedido.pedido_id, statusId); notificacoes.notificar({ tipo: 'success', mensagem: 'Status do pedido atualizado.', tempo: 4 }); await carregar() } catch (falha) { notificacoes.notificar({ tipo: 'danger', mensagem: falha?.data?.detail || 'Não foi possível atualizar o status.' }) } finally { atualizando.value = null } }
onMounted(carregar)
</script>
