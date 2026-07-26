<template>
  <div>
    <h2 class="fw-bold mb-4" style="color: #1b5e35;">Meu Carrinho</h2>

    <div v-if="carrinhoStore.totalItens === 0" class="card border text-center py-5" style="border-color: #d1e7d8 !important; border-radius: 14px;">
      <div class="card-body">
        <div style="width:80px;height:80px;background:#c8e6c9;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:34px;margin:0 auto 1rem;">🛒</div>
        <h5 class="fw-bold mb-2" style="color:#1b5e35;">Seu carrinho está vazio</h5>
        <p class="text-muted mb-3">Você ainda não adicionou nenhum produto ao carrinho.</p>
        <RouterLink to="/" class="btn btn-success rounded-pill px-4">Voltar ao Mercado</RouterLink>
      </div>
    </div>

    <div v-else class="row g-4">
      <div class="col-12 col-lg-8">
        <div v-for="(itens, fornecedor) in carrinhoStore.porFornecedor" :key="fornecedor" class="mb-3">
          <p class="text-muted small fw-bold text-uppercase mb-2">🏪 {{ fornecedor }}</p>
          <div class="card border mb-2" style="border-color:#d1e7d8 !important;border-radius:12px;" v-for="item in itens" :key="item.id">
            <div class="card-body p-3 d-flex align-items-center gap-3">
              <div class="produto-img-mini">{{ item.emoji }}</div>
              <div class="flex-grow-1">
                <p class="fw-bold mb-0 small" style="color:#1b5e35;">{{ item.nome }}</p>
                <p class="fw-bold mb-0" style="color:#2E8B57;">{{ formatarPreco(item.preco) }}</p>
              </div>
              <div class="d-flex align-items-center gap-2">
                <button class="btn btn-outline-secondary btn-sm" @click="carrinhoStore.alterarQuantidade(item.id, -1)">−</button>
                <span class="fw-bold" style="min-width:20px;text-align:center;">{{ item.quantidade }}</span>
                <button class="btn btn-outline-secondary btn-sm" @click="carrinhoStore.alterarQuantidade(item.id, 1)">+</button>
              </div>
              <span class="fw-bold ms-2" style="min-width:80px;text-align:right;color:#1b5e35;">{{ formatarPreco(item.preco * item.quantidade) }}</span>
              <button class="btn btn-link text-danger p-0 ms-1" @click="carrinhoStore.remover(item.id)">✕</button>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-lg-4">
        <div class="card border" style="border-color:#d1e7d8 !important;border-radius:14px;">
          <div class="card-body p-4">
            <h6 class="fw-bold mb-3" style="color:#1b5e35;">Resumo do pedido</h6>
            <div v-for="(itens, fornecedor) in carrinhoStore.porFornecedor" :key="fornecedor" class="d-flex justify-content-between small text-muted mb-1">
              <span>{{ fornecedor }}</span>
              <span>{{ formatarPreco(itens.reduce((s, i) => s + i.preco * i.quantidade, 0)) }}</span>
            </div>
            <hr style="border-color:#d1e7d8;" />
            <div class="d-flex justify-content-between fw-bold mb-4" style="color:#1b5e35;">
              <span>Total</span><span>{{ formatarPreco(carrinhoStore.total) }}</span>
            </div>
            <button class="btn btn-success w-100 fw-bold py-2">Finalizar Pedido</button>
            <RouterLink to="/" class="btn btn-outline-secondary w-100 mt-2">Continuar comprando</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCarrinhoStore } from '@/stores/index.js'
const carrinhoStore = useCarrinhoStore()
function formatarPreco(valor) {
  return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}
</script>

<style scoped>
.produto-img-mini { width:52px;height:52px;background:#E8F5E9;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0; }
.btn-success { background-color:#2E8B57 !important;border-color:#2E8B57 !important; }
.btn-success:hover { background-color:#1e6b40 !important;border-color:#1e6b40 !important; }
</style>
