<template>
  <section>
    <div class="mb-4">
      <h1 class="fw-semibold mb-1">Meu perfil</h1>
      <p class="text-body-secondary mb-0">Consulte e mantenha seus dados de contato atualizados.</p>
    </div>

    <div v-if="!authStore.estaLogado" class="card rounded-4 text-center py-5">
      <div class="card-body">
        <span class="icone-estado mb-3"><IconeSvg nome="usuario" :tamanho="32" /></span>
        <h2 class="h4 fw-semibold mb-2">Entre para ver seu perfil</h2>
        <p class="text-body-secondary mb-3">Seus dados ficam vinculados à sua conta.</p>
        <RouterLink :to="{ name: 'login', query: { retorno: route.fullPath } }" class="btn btn-primary rounded-pill px-4">Entrar</RouterLink>
      </div>
    </div>

    <div v-else-if="carregando" class="row g-4" aria-hidden="true">
      <div class="col-12 col-lg-4"><div class="card rounded-4 p-4 placeholder-glow"><span class="placeholder col-8 mx-auto"></span></div></div>
      <div class="col-12 col-lg-8"><div class="card rounded-4 p-4 placeholder-glow"><span class="placeholder col-5"></span></div></div>
      <span class="visually-hidden" role="status">Carregando perfil...</span>
    </div>

    <div v-else-if="erro" class="alert alert-danger d-flex flex-wrap align-items-center gap-2" role="alert">
      <span><strong>Não foi possível carregar seus dados.</strong> Verifique sua conexão e tente novamente.</span>
      <button type="button" class="btn btn-sm btn-outline-danger" @click="carregar">Tentar novamente</button>
    </div>

    <div v-else-if="usuario" class="row g-4">
      <div class="col-12 col-lg-4 d-flex flex-column gap-4">
        <div class="card rounded-4 text-center">
          <div class="card-body p-4">
            <SeletorImagemUnica
              id="perfil-foto"
              ref="seletorFoto"
              v-model="arquivoFoto"
              rotulo="Foto de perfil"
              rotulo-oculto
              empilhado
              ajuda="Opcional. JPG, PNG ou WEBP com até 5 MB. Só você vê esta foto."
              tamanho="xl"
              :imagem-atual="usuario.foto_perfil"
              :nome="usuario.nome"
              :enviando="enviandoFoto"
              :desabilitado="removendoFoto"
              :erro="erroFoto"
              @selecionar="erroFoto = ''"
              @erro="erroFoto = ''"
              @remover="modalRemoverFoto?.abrir()"
            >
              <template #apos-imagem>
                <div>
                  <h2 class="h5 fw-semibold mb-1">{{ usuario.nome }}</h2>
                  <p class="small text-body-secondary text-break mb-3">{{ usuario.email }}</p>
                  <span class="badge rounded-pill selo-status d-inline-flex align-items-center gap-1">
                    <IconeSvg :nome="usuario.is_produtor ? 'broto' : 'usuario'" :tamanho="14" />
                    {{ usuario.is_produtor ? 'Produtor rural' : 'Cliente' }}
                  </span>
                </div>
              </template>
              <template #acoes>
                <div v-if="arquivoFoto" class="d-flex flex-wrap justify-content-center gap-2">
                  <button type="button" class="btn btn-primary btn-sm rounded-pill px-3" :disabled="enviandoFoto" @click="salvarFoto">
                    <span v-if="enviandoFoto" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
                    {{ enviandoFoto ? 'Salvando...' : 'Salvar imagem' }}
                  </button>
                  <button type="button" class="btn btn-outline-secondary btn-sm rounded-pill px-3" :disabled="enviandoFoto" @click="cancelarFoto">
                    Cancelar
                  </button>
                </div>
              </template>
            </SeletorImagemUnica>
          </div>
        </div>

        <section v-if="usuario.tem_loja" class="card rounded-4" aria-labelledby="titulo-minha-loja">
          <div class="card-body p-4">
            <h2 id="titulo-minha-loja" class="h6 fw-semibold text-body-secondary d-flex align-items-center gap-2 mb-3 titulo-secao">
              <IconeSvg nome="loja" :tamanho="16" /> Minha loja
            </h2>
            <template v-if="loja">
              <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
                <p class="fs-5 fw-semibold mb-0">{{ loja.nome }}</p>
                <span class="badge rounded-pill selo-status" :class="loja.ativa ? 'selo-entregue' : 'selo-cancelado'">
                  {{ loja.ativa ? 'Ativa' : 'Inativa' }}
                </span>
              </div>
              <p v-if="loja.descricao" class="small text-body-secondary descricao-loja">{{ loja.descricao }}</p>
            </template>
            <RouterLink :to="{ name: 'minha-loja' }" class="btn btn-primary rounded-pill w-100 mt-2">Gerenciar minha loja</RouterLink>
          </div>
        </section>

        <section v-else class="card rounded-4 bg-apoio border-0" aria-labelledby="titulo-abrir-loja">
          <div class="card-body p-4">
            <span class="icone-loja rounded-circle d-inline-flex align-items-center justify-content-center mb-3" aria-hidden="true">
              <IconeSvg nome="loja" :tamanho="22" />
            </span>
            <h2 id="titulo-abrir-loja" class="h5 fw-semibold mb-2">Gostaria de abrir uma loja?</h2>
            <template v-if="usuario.is_produtor">
              <p class="small text-body-secondary mb-3">
                Crie sua loja para cadastrar produtos e receber pedidos para retirada na feira.
              </p>
              <RouterLink :to="{ name: 'criar-loja' }" class="btn btn-primary rounded-pill w-100">Criar minha loja</RouterLink>
            </template>
            <p v-else class="small text-body-secondary mb-0">
              Para vender na Agro Store é preciso ter o perfil de produtor rural habilitado.
              Procure a organização da Feira do Produtor Rural para solicitar a habilitação.
            </p>
          </div>
        </section>
      </div>

      <div class="col-12 col-lg-8">
        <section class="card rounded-4 h-100" aria-labelledby="titulo-informacoes">
          <div class="card-body p-4">
            <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-4">
              <h2 id="titulo-informacoes" class="h5 fw-semibold mb-0">Informações pessoais</h2>
              <button
                v-if="!editando"
                type="button"
                class="btn btn-outline-primary rounded-pill px-3 d-inline-flex align-items-center gap-2"
                @click="iniciarEdicao"
              >
                <IconeSvg nome="lapis" :tamanho="16" /> Editar
              </button>
            </div>

            <dl v-if="!editando" class="row g-3 mb-0">
              <div v-for="campo in camposLeitura" :key="campo.rotulo" class="col-12 col-sm-6">
                <dt class="small fw-semibold text-body-secondary mb-1">{{ campo.rotulo }}</dt>
                <dd class="campo-leitura rounded-3 mb-0">{{ campo.valor }}</dd>
              </div>
            </dl>

            <form v-else novalidate @submit.prevent="salvar">
              <p class="small text-body-secondary">Campos com <span class="text-danger">*</span> são obrigatórios.</p>
              <div class="row g-3">
                <div class="col-12">
                  <label for="perfil-nome" class="form-label">Nome completo <span class="text-danger">*</span></label>
                  <input
                    id="perfil-nome"
                    v-model.trim="form.nome"
                    class="form-control"
                    :class="{ 'is-invalid': erros.nome }"
                    maxlength="150"
                    autocomplete="name"
                    required
                    aria-describedby="erro-perfil-nome"
                  >
                  <div id="erro-perfil-nome" class="invalid-feedback">{{ erros.nome }}</div>
                </div>

                <div class="col-12 col-sm-6">
                  <label for="perfil-email" class="form-label">E-mail <span class="text-danger">*</span></label>
                  <input
                    id="perfil-email"
                    v-model.trim="form.email"
                    type="email"
                    class="form-control"
                    :class="{ 'is-invalid': erros.email }"
                    autocomplete="email"
                    required
                    aria-describedby="erro-perfil-email"
                  >
                  <div id="erro-perfil-email" class="invalid-feedback">{{ erros.email }}</div>
                </div>

                <div class="col-12 col-sm-6">
                  <label for="perfil-cpf" class="form-label">CPF</label>
                  <input id="perfil-cpf" :value="formatarCpf(usuario.cpf)" class="form-control" disabled aria-describedby="ajuda-perfil-cpf">
                  <div id="ajuda-perfil-cpf" class="form-text">O CPF identifica sua conta e não pode ser alterado.</div>
                </div>

                <div class="col-12 col-sm-6">
                  <label for="perfil-telefone" class="form-label">Celular <span class="text-danger">*</span></label>
                  <input
                    id="perfil-telefone"
                    v-model="form.telefone"
                    class="form-control"
                    :class="{ 'is-invalid': erros.telefone }"
                    inputmode="numeric"
                    maxlength="15"
                    placeholder="(00) 00000-0000"
                    autocomplete="tel-national"
                    required
                    aria-describedby="erro-perfil-telefone"
                    @input="form.telefone = mascaraTelefone(form.telefone)"
                  >
                  <div id="erro-perfil-telefone" class="invalid-feedback">{{ erros.telefone }}</div>
                </div>

                <div class="col-12 col-sm-6">
                  <label for="perfil-nascimento" class="form-label">Data de nascimento <span class="text-danger">*</span></label>
                  <input
                    id="perfil-nascimento"
                    v-model="form.data_nascimento"
                    type="date"
                    class="form-control"
                    :class="{ 'is-invalid': erros.data_nascimento }"
                    :max="hoje"
                    autocomplete="bday"
                    required
                    aria-describedby="ajuda-perfil-idade erro-perfil-nascimento"
                  >
                  <div id="erro-perfil-nascimento" class="invalid-feedback">{{ erros.data_nascimento }}</div>
                  <div id="ajuda-perfil-idade" class="form-text" aria-live="polite">
                    {{ idadeFormulario === null ? 'A idade é calculada pela data de nascimento.' : `Idade: ${idadeFormulario} anos` }}
                  </div>
                </div>

                <div class="col-12 col-sm-6">
                  <label for="perfil-genero" class="form-label">Gênero <span class="text-danger">*</span></label>
                  <select
                    id="perfil-genero"
                    v-model="form.genero"
                    class="form-select"
                    :class="{ 'is-invalid': erros.genero }"
                    required
                    aria-describedby="erro-perfil-genero"
                  >
                    <option v-for="(rotulo, codigo) in GENEROS" :key="codigo" :value="codigo">{{ rotulo }}</option>
                  </select>
                  <div id="erro-perfil-genero" class="invalid-feedback">{{ erros.genero }}</div>
                </div>
              </div>

              <div v-if="erroGeral" class="alert alert-danger small mt-3 mb-0" role="alert">{{ erroGeral }}</div>

              <div class="d-flex justify-content-end gap-2 mt-4">
                <button type="button" class="btn btn-outline-secondary rounded-pill px-4" :disabled="salvando" @click="cancelarEdicao">Cancelar</button>
                <button type="submit" class="btn btn-primary rounded-pill px-4" :disabled="salvando">
                  <span v-if="salvando" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
                  {{ salvando ? 'Salvando...' : 'Salvar' }}
                </button>
              </div>
            </form>
          </div>
        </section>
      </div>
    </div>

    <ModalConfirmacao
      ref="modalRemoverFoto"
      titulo="Remover foto de perfil?"
      texto-confirmar="Remover"
      texto-carregando="Removendo..."
      :carregando="removendoFoto"
      @confirmar="removerFoto"
      @fechado="aoFecharModalFoto"
    >
      <p class="mb-0">Sua foto deixa de aparecer no perfil e no menu da conta, e as iniciais do seu nome são exibidas no lugar.</p>
    </ModalConfirmacao>
  </section>
</template>

<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import IconeSvg from '@/components/IconeSvg.vue'
import ModalConfirmacao from '@/components/ModalConfirmacao.vue'
import SeletorImagemUnica from '@/components/SeletorImagemUnica.vue'
import { api } from '@/services/api.js'
import { useAuthStore } from '@/stores/auth.js'
import { useNotificacoesStore } from '@/stores/notificacoes.js'
import {
  calcularIdade, formatarCpf, formatarData, formatarTelefone, mascaraTelefone, somenteDigitos,
} from '@/utils/formatacao.js'
import { MENSAGEM_FALHA_REMOCAO_IMAGEM, mensagemErroEnvioImagem } from '@/utils/imagem.js'

const GENEROS = { M: 'Masculino', F: 'Feminino', I: 'Prefiro não informar' }

const route = useRoute()
const authStore = useAuthStore()
const notificacoes = useNotificacoesStore()
const usuario = ref(null)
const loja = ref(null)
const carregando = ref(false)
const erro = ref(false)
const editando = ref(false)
const salvando = ref(false)
const form = ref({})
const erros = ref({})
const erroGeral = ref('')
// Data local no formato aaaa-mm-dd (limite do campo de nascimento)
const hoje = new Date().toLocaleDateString('sv-SE')

// Foto de perfil (RN-018): fluxo próprio, independente da edição das informações pessoais
const arquivoFoto = ref(null)
const enviandoFoto = ref(false)
const removendoFoto = ref(false)
const erroFoto = ref('')
const seletorFoto = ref(null)
const modalRemoverFoto = ref(null)

const camposLeitura = computed(() => {
  const dados = usuario.value
  const idade = calcularIdade(dados.data_nascimento)
  return [
    { rotulo: 'Nome completo', valor: dados.nome },
    { rotulo: 'E-mail', valor: dados.email },
    { rotulo: 'CPF', valor: formatarCpf(dados.cpf) },
    { rotulo: 'Celular', valor: formatarTelefone(dados.telefone) },
    { rotulo: 'Data de nascimento', valor: formatarData(dados.data_nascimento) },
    { rotulo: 'Idade', valor: idade === null ? 'Não informada' : `${idade} anos` },
    { rotulo: 'Gênero', valor: GENEROS[dados.genero] || 'Não informado' },
  ]
})

const idadeFormulario = computed(() => calcularIdade(form.value.data_nascimento))

onMounted(() => {
  if (authStore.estaLogado) carregar()
})

async function carregar() {
  carregando.value = true
  erro.value = false
  try {
    usuario.value = await api.usuarios.me()
    authStore.atualizarUsuario(usuario.value)
    loja.value = usuario.value.tem_loja ? await carregarLoja() : null
  } catch (falha) {
    console.error(falha)
    erro.value = true
  } finally {
    carregando.value = false
  }
}

// A falha ao buscar a loja não impede exibir o perfil; o bloco mostra apenas o botão de gerenciar
async function carregarLoja() {
  try {
    return await api.lojas.me()
  } catch (falha) {
    console.error(falha)
    return null
  }
}

async function iniciarEdicao() {
  const dados = usuario.value
  form.value = {
    nome: dados.nome,
    email: dados.email,
    telefone: mascaraTelefone(dados.telefone || ''),
    data_nascimento: dados.data_nascimento,
    genero: dados.genero,
  }
  erros.value = {}
  erroGeral.value = ''
  editando.value = true
  await nextTick()
  document.getElementById('perfil-nome')?.focus()
}

function aplicarUsuario(dados) {
  usuario.value = dados
  authStore.atualizarUsuario(dados)
}

async function salvarFoto() {
  erroFoto.value = ''
  enviandoFoto.value = true
  try {
    aplicarUsuario(await api.usuarios.atualizarFoto(arquivoFoto.value))
    arquivoFoto.value = null
    notificacoes.notificar({ tipo: 'success', mensagem: 'Foto de perfil atualizada.', tempo: 4 })
  } catch (falha) {
    erroFoto.value = mensagemErroEnvioImagem(falha, 'foto_perfil')
    // Arquivo recusado pelo backend sai da prévia e a foto atual volta a aparecer; em falha de rede, pode tentar de novo
    if (falha?.status === 400) arquivoFoto.value = null
  } finally {
    enviandoFoto.value = false
  }
  // Espera o botão ser reabilitado para devolver o foco
  await nextTick()
  seletorFoto.value?.focar()
}

// Removida a foto, o botão "Remover imagem" some: o foco vai para "Escolher imagem"
function aoFecharModalFoto() {
  if (!usuario.value?.foto_perfil) seletorFoto.value?.focar()
}

function cancelarFoto() {
  arquivoFoto.value = null
  erroFoto.value = ''
  seletorFoto.value?.limparErro()
  seletorFoto.value?.focar()
}

async function removerFoto() {
  removendoFoto.value = true
  try {
    await api.usuarios.removerFoto()
  } catch (falha) {
    // 404: não havia foto válida para remover; o estado final é o mesmo
    if (falha?.status !== 404) {
      notificacoes.notificar({ tipo: 'danger', mensagem: MENSAGEM_FALHA_REMOCAO_IMAGEM })
      removendoFoto.value = false
      modalRemoverFoto.value?.fechar()
      return
    }
  }
  aplicarUsuario({ ...usuario.value, foto_perfil: null })
  erroFoto.value = ''
  removendoFoto.value = false
  modalRemoverFoto.value?.fechar()
  notificacoes.notificar({ tipo: 'success', mensagem: 'Foto de perfil removida.', tempo: 4 })
}

function cancelarEdicao() {
  editando.value = false
}

function validar() {
  const novosErros = {}
  if (!form.value.nome) novosErros.nome = 'Informe seu nome completo.'
  if (!/^\S+@\S+\.\S+$/.test(form.value.email || '')) novosErros.email = 'Informe um e-mail válido.'
  if (somenteDigitos(form.value.telefone).length !== 11) novosErros.telefone = 'Informe um celular com DDD (11 dígitos).'
  if (!form.value.data_nascimento) novosErros.data_nascimento = 'Informe sua data de nascimento.'
  if (!GENEROS[form.value.genero]) novosErros.genero = 'Selecione uma opção.'
  erros.value = novosErros
  return Object.keys(novosErros).length === 0
}

async function salvar() {
  erroGeral.value = ''
  if (!validar()) return

  salvando.value = true
  try {
    usuario.value = await api.usuarios.atualizar({ ...form.value, telefone: somenteDigitos(form.value.telefone) })
    authStore.atualizarUsuario(usuario.value)
    editando.value = false
    notificacoes.notificar({ tipo: 'success', mensagem: 'Dados atualizados com sucesso.', tempo: 4 })
  } catch (falha) {
    const dados = falha?.data || {}
    const errosDosCampos = {}
    for (const campo of Object.keys(form.value)) {
      if (dados[campo]) errosDosCampos[campo] = Array.isArray(dados[campo]) ? dados[campo][0] : String(dados[campo])
    }
    erros.value = errosDosCampos
    if (!Object.keys(errosDosCampos).length) erroGeral.value = dados.detail || 'Não foi possível salvar seus dados.'
  } finally {
    salvando.value = false
  }
}
</script>

<style scoped>
.icone-loja {
  width: 3rem;
  height: 3rem;
  background-color: var(--cor-superficie);
  color: var(--cor-primaria);
}
.titulo-secao {
  font-family: var(--fonte-texto);
}
.campo-leitura {
  min-height: 2.75rem;
  padding: 0.625rem 0.875rem;
  background-color: var(--cor-fundo);
  border: 1px solid var(--cor-borda);
  overflow-wrap: anywhere;
}
.descricao-loja {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
