<template>
  <div>
    <h1 class="h2 fw-bold mb-4">Meu perfil</h1>

    <div v-if="carregando" class="card border p-4"><div class="placeholder-glow"><span class="placeholder col-5"></span></div></div>
    <div v-else-if="erro" class="alert alert-danger" role="alert">
      Não foi possível carregar os dados.
      <button class="btn btn-sm btn-outline-danger ms-2" @click="carregarUsuario">Tentar novamente</button>
    </div>
    <div v-else-if="usuario" class="row g-4">
      <div class="col-12 col-lg-4">
        <div class="card border text-center p-4 h-100">
          <div class="avatar mx-auto mb-3">{{ iniciais }}</div>
          <h2 class="h5 fw-bold mb-1">{{ usuario.nome }}</h2>
          <p class="text-body-secondary small mb-3">{{ usuario.email }}</p>
          <span class="badge rounded-pill px-3 py-2 mb-4" :class="usuario.is_produtor ? 'text-bg-success' : 'text-bg-secondary'">
            {{ usuario.is_produtor ? 'Produtor rural' : 'Cliente' }}
          </span>
          <div v-if="usuario.is_produtor"><hr><RouterLink :to="{ name: 'minha-loja' }" class="btn btn-outline-primary w-100">Gerenciar minha loja</RouterLink></div>
        </div>
      </div>
      <div class="col-12 col-lg-8"><div class="card border h-100"><div class="card-body p-4">
        <h2 class="h5 fw-bold mb-4">Informações pessoais</h2>
        <div class="row g-3">
          <CampoPerfil rotulo="Nome completo" :valor="usuario.nome" />
          <CampoPerfil rotulo="CPF" :valor="formatarCpf(usuario.cpf)" />
          <CampoPerfil rotulo="E-mail" :valor="usuario.email" />
          <CampoPerfil rotulo="Celular" :valor="formatarTelefone(usuario.telefone)" />
          <CampoPerfil rotulo="Data de nascimento" :valor="formatarData(usuario.data_nascimento)" />
          <CampoPerfil rotulo="Gênero" :valor="formatarGenero(usuario.genero)" />
          <CampoPerfil rotulo="Idade" :valor="`${usuario.idade} anos`" />
        </div>
      </div></div></div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineComponent, h, onMounted, ref } from 'vue'
import { api } from '@/services/api.js'

const CampoPerfil = defineComponent({
  props: { rotulo: { type: String, required: true }, valor: { type: String, required: true } },
  setup(props) { return () => h('div', { class: 'col-12 col-sm-6' }, [h('div', { class: 'form-label small fw-semibold text-body-secondary' }, props.rotulo), h('div', { class: 'info-field' }, props.valor)]) },
})
const usuario = ref(null)
const carregando = ref(true)
const erro = ref(false)
const iniciais = computed(() => usuario.value?.nome?.split(' ').slice(0, 2).map(nome => nome[0]).join('').toUpperCase() || '?')
async function carregarUsuario() { carregando.value = true; erro.value = false; try { usuario.value = await api.usuarios.me() } catch { erro.value = true } finally { carregando.value = false } }
function formatarCpf(cpf) { return cpf?.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4') || '-' }
function formatarTelefone(telefone) { return telefone?.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3') || '-' }
function formatarData(data) { return data ? data.split('-').reverse().join('/') : '-' }
function formatarGenero(genero) { return { M: 'Masculino', F: 'Feminino', I: 'Prefiro não informar' }[genero] || '-' }
onMounted(carregarUsuario)
</script>

<style scoped>
.avatar { align-items: center; background: var(--green-mid); border-radius: 50%; color: var(--green-text); display: flex; font-size: 1.4rem; font-weight: 700; height: 64px; justify-content: center; width: 64px; }
.info-field { background: var(--gray-light); border: 1px solid var(--border); border-radius: 8px; color: var(--green-text); padding: 10px 14px; }
.btn-outline-primary { border-color: var(--green-dark); color: var(--green-dark); }
</style>
