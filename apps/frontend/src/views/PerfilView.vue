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

      <div class="col-12 col-lg-8 d-flex flex-column gap-4">
        <section class="card rounded-4" aria-labelledby="titulo-informacoes">
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

        <!-- Telefones do usuário (RN-021) -->
        <section class="card rounded-4" aria-labelledby="titulo-telefones">
          <div class="card-body p-4">
            <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-2">
              <h2 id="titulo-telefones" class="h5 fw-semibold mb-0">Telefones</h2>
              <button
                id="perfil-telefone-adicionar"
                type="button"
                class="btn btn-outline-primary rounded-pill px-3 d-inline-flex align-items-center gap-2"
                :disabled="!podeAbrirFormulario"
                @click="abrirFormularioTelefone('novo', 'perfil-telefone-adicionar')"
              >
                <IconeSvg nome="mais" :tamanho="16" /> Adicionar telefone
              </button>
            </div>
            <p class="small text-body-secondary mb-3">O telefone principal é o contato que o produtor vê nos seus pedidos em aberto.</p>

            <div v-if="tiposTelefoneStore.erro" class="alert alert-warning small py-2 d-flex flex-wrap align-items-center gap-2" role="alert">
              <span>Não foi possível carregar os tipos de telefone.</span>
              <button type="button" class="btn btn-sm btn-outline-secondary" @click="tiposTelefoneStore.carregar()">Tentar novamente</button>
            </div>

            <div v-if="carregandoTelefones && !telefones" class="placeholder-glow d-flex flex-column gap-3" role="status">
              <span class="placeholder col-12 rounded-4 placeholder-telefone" aria-hidden="true"></span>
              <span class="placeholder col-12 rounded-4 placeholder-telefone" aria-hidden="true"></span>
              <span class="visually-hidden">Carregando telefones...</span>
            </div>

            <div v-else-if="erroTelefones" class="alert alert-danger d-flex flex-wrap align-items-center gap-2 mb-0" role="alert">
              <span>Não foi possível carregar seus telefones.</span>
              <button type="button" class="btn btn-sm btn-outline-danger" :disabled="carregandoTelefones" @click="recarregarTelefones">Tentar novamente</button>
            </div>

            <template v-else-if="telefones">
              <div v-if="!telefones.length" class="alert alert-warning" :class="{ 'mb-0': edicaoTelefone?.id !== 'novo' }" role="status">
                <p class="fw-semibold mb-1">Você ainda não tem um telefone cadastrado.</p>
                <p class="small mb-0">
                  Cadastre um telefone para que o produtor possa entrar em contato sobre a retirada dos seus pedidos.
                  O primeiro telefone cadastrado será o principal.
                </p>
              </div>

              <ul class="list-unstyled d-flex flex-column gap-3 mb-0">
                <li v-if="edicaoTelefone?.id === 'novo'" class="border rounded-4 p-3">
                  <FormularioTelefone
                    :ref="registrarFormularioTelefone"
                    id-sufixo="novo"
                    :tipos="tiposTelefoneStore.tipos"
                    :tipo-padrao="tiposTelefoneStore.idPorDescricao('Celular') ?? ''"
                    :erros="errosTelefone"
                    :enviando="enviandoTelefone"
                    :primeiro="!telefones.length"
                    @salvar="salvarTelefone"
                    @cancelar="fecharFormularioTelefone"
                  />
                </li>

                <li
                  v-for="telefone in telefones"
                  :key="telefone.id"
                  class="border rounded-4 p-3"
                  :class="{ 'bg-apoio border-primary': telefone.e_principal }"
                >
                  <FormularioTelefone
                    v-if="edicaoTelefone?.id === telefone.id"
                    :ref="registrarFormularioTelefone"
                    :id-sufixo="telefone.id"
                    :tipos="tiposTelefoneStore.tipos"
                    :telefone="telefone"
                    :erros="errosTelefone"
                    :enviando="enviandoTelefone"
                    @salvar="salvarTelefone"
                    @cancelar="fecharFormularioTelefone"
                  />

                  <template v-else>
                    <div class="d-flex align-items-start gap-3">
                      <span class="text-primary mt-1"><IconeSvg nome="telefone" :tamanho="20" /></span>
                      <div class="flex-grow-1">
                        <div class="d-flex flex-wrap align-items-center gap-2">
                          <span class="fw-semibold">{{ formatarTelefone(telefone.numero) }}</span>
                          <span v-if="telefone.e_principal" class="badge rounded-pill text-bg-primary">Principal</span>
                        </div>
                        <p class="small text-body-secondary mb-0">{{ telefone.tipo_descricao }}</p>
                      </div>
                    </div>

                    <div class="d-flex flex-wrap gap-2 mt-3">
                      <button
                        :id="`perfil-telefone-editar-${telefone.id}`"
                        type="button"
                        class="btn btn-sm btn-outline-secondary rounded-pill d-inline-flex align-items-center gap-1"
                        :disabled="!podeAbrirFormulario"
                        :aria-label="`Editar telefone ${formatarTelefone(telefone.numero)}`"
                        @click="abrirFormularioTelefone(telefone.id, `perfil-telefone-editar-${telefone.id}`)"
                      >
                        <IconeSvg nome="lapis" :tamanho="14" /> Editar
                      </button>
                      <button
                        v-if="!telefone.e_principal"
                        type="button"
                        class="btn btn-sm btn-outline-primary rounded-pill"
                        :disabled="acoesBloqueadas"
                        :aria-label="`Definir como principal o telefone ${formatarTelefone(telefone.numero)}`"
                        @click="definirPrincipal(telefone)"
                      >
                        Definir como principal
                      </button>
                      <button
                        type="button"
                        class="btn btn-sm btn-outline-danger rounded-pill"
                        :class="{ disabled: !!motivoBloqueioExclusao(telefone) }"
                        :disabled="acoesBloqueadas"
                        :aria-disabled="motivoBloqueioExclusao(telefone) ? 'true' : null"
                        :aria-describedby="motivoBloqueioExclusao(telefone) ? `perfil-telefone-bloqueio-${telefone.id}` : null"
                        :aria-label="`Excluir telefone ${formatarTelefone(telefone.numero)}`"
                        @click="solicitarExclusao(telefone)"
                      >
                        Excluir
                      </button>
                    </div>
                    <p
                      v-if="motivoBloqueioExclusao(telefone)"
                      :id="`perfil-telefone-bloqueio-${telefone.id}`"
                      class="small text-body-secondary mt-2 mb-0"
                    >
                      {{ motivoBloqueioExclusao(telefone) }}
                    </p>
                  </template>
                </li>
              </ul>
            </template>
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

    <ModalConfirmacao
      ref="modalExcluirTelefone"
      titulo="Excluir telefone?"
      texto-confirmar="Excluir"
      texto-carregando="Excluindo..."
      :carregando="enviandoTelefone"
      @confirmar="excluirTelefone"
      @fechado="aoFecharModalTelefone"
    >
      <p v-if="telefoneParaExcluir" class="mb-0">
        O telefone {{ formatarTelefone(telefoneParaExcluir.numero) }} ({{ telefoneParaExcluir.tipo_descricao }}) será removido da sua conta.
      </p>
    </ModalConfirmacao>
  </section>
</template>

<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import FormularioTelefone from '@/components/FormularioTelefone.vue'
import IconeSvg from '@/components/IconeSvg.vue'
import ModalConfirmacao from '@/components/ModalConfirmacao.vue'
import SeletorImagemUnica from '@/components/SeletorImagemUnica.vue'
import { api } from '@/services/api.js'
import { useAuthStore } from '@/stores/auth.js'
import { useNotificacoesStore } from '@/stores/notificacoes.js'
import { useTiposTelefoneStore } from '@/stores/tiposTelefone.js'
import {
  calcularIdade, formatarCpf, formatarData, formatarTelefone,
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

// Telefones (RN-021): fluxo próprio; a lista vem do GET /me/ e é recarregada após cada alteração
const MENSAGEM_FALHA_ACAO_TELEFONE = 'Não foi possível concluir a ação. Tente novamente.'
const tiposTelefoneStore = useTiposTelefoneStore()
const telefones = ref(null)
const carregandoTelefones = ref(false)
const erroTelefones = ref(false)
const enviandoTelefone = ref(false)
// { id: telefoneId | 'novo', origem: id do botão que abriu o formulário }
const edicaoTelefone = ref(null)
const errosTelefone = ref({})
const formularioTelefone = ref(null)
const telefoneParaExcluir = ref(null)
const modalExcluirTelefone = ref(null)
let exclusaoConcluida = false

const camposLeitura = computed(() => {
  const dados = usuario.value
  const idade = calcularIdade(dados.data_nascimento)
  return [
    { rotulo: 'Nome completo', valor: dados.nome },
    { rotulo: 'E-mail', valor: dados.email },
    { rotulo: 'CPF', valor: formatarCpf(dados.cpf) },
    { rotulo: 'Data de nascimento', valor: formatarData(dados.data_nascimento) },
    { rotulo: 'Idade', valor: idade === null ? 'Não informada' : `${idade} anos` },
    { rotulo: 'Gênero', valor: GENEROS[dados.genero] || 'Não informado' },
  ]
})

const idadeFormulario = computed(() => calcularIdade(form.value.data_nascimento))

const tiposTelefoneDisponiveis = computed(() => !tiposTelefoneStore.carregando && !tiposTelefoneStore.erro && tiposTelefoneStore.tipos.length > 0)
const acoesBloqueadas = computed(() => enviandoTelefone.value || carregandoTelefones.value)
const podeAbrirFormulario = computed(() => !acoesBloqueadas.value && !edicaoTelefone.value && tiposTelefoneDisponiveis.value && !!telefones.value)

onMounted(() => {
  if (authStore.estaLogado) {
    carregar()
    tiposTelefoneStore.carregar()
  }
})

async function carregar() {
  carregando.value = true
  erro.value = false
  try {
    usuario.value = await api.usuarios.me()
    authStore.atualizarUsuario(usuario.value)
    if (Array.isArray(usuario.value.telefones)) aplicarTelefones(usuario.value.telefones, false)
    else recarregarTelefones()
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
    aplicarUsuario(await api.usuarios.atualizar({ ...form.value }))
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

// ----- Telefones (RN-021) -----

function primeiraMensagem(valor) {
  if (Array.isArray(valor)) return valor.length ? String(valor[0]) : ''
  return valor ? String(valor) : ''
}

// Mensagem de regra do backend ({ detail } ou { e_principal }), usada nas notificações de erro
function mensagemErroTelefone(falha, fallback = MENSAGEM_FALHA_ACAO_TELEFONE) {
  const dados = falha?.data || {}
  return primeiraMensagem(dados.detail) || primeiraMensagem(dados.e_principal)
    || primeiraMensagem(dados.numero) || primeiraMensagem(dados.tipo) || fallback
}

// Principal primeiro; a store da sessão acompanha a lista para não guardar o formato antigo (usuario.telefone)
function aplicarTelefones(lista, sincronizarSessao = true) {
  telefones.value = [...lista].sort((a, b) => Number(b.e_principal) - Number(a.e_principal))
  erroTelefones.value = false
  if (sincronizarSessao && usuario.value) aplicarUsuario({ ...usuario.value, telefones: telefones.value })
}

async function recarregarTelefones() {
  carregandoTelefones.value = true
  try {
    aplicarTelefones(await api.telefones.listar())
    return true
  } catch (falha) {
    console.error(falha)
    erroTelefones.value = true
    return false
  } finally {
    carregandoTelefones.value = false
  }
}

function registrarFormularioTelefone(componente) {
  if (componente) formularioTelefone.value = componente
}

async function abrirFormularioTelefone(id, origem) {
  if (!podeAbrirFormulario.value) return
  errosTelefone.value = {}
  edicaoTelefone.value = { id, origem }
  await nextTick()
  formularioTelefone.value?.focar()
}

async function fecharFormularioTelefone(destinoFoco) {
  const origem = destinoFoco || edicaoTelefone.value?.origem
  edicaoTelefone.value = null
  errosTelefone.value = {}
  formularioTelefone.value = null
  await nextTick()
  document.getElementById(origem)?.focus()
}

async function salvarTelefone(dados) {
  const edicao = edicaoTelefone.value
  if (!edicao) return
  const novo = edicao.id === 'novo'
  errosTelefone.value = {}
  enviandoTelefone.value = true
  try {
    if (novo) await api.telefones.criar(dados)
    else await api.telefones.atualizar(edicao.id, dados)
  } catch (falha) {
    const resposta = falha?.data || {}
    const errosCampos = {}
    if (resposta.numero) errosCampos.numero = primeiraMensagem(resposta.numero)
    if (resposta.tipo) errosCampos.tipo = primeiraMensagem(resposta.tipo)
    if (!Object.keys(errosCampos).length) errosCampos.geral = mensagemErroTelefone(falha)
    errosTelefone.value = errosCampos
    enviandoTelefone.value = false
    return
  }
  enviandoTelefone.value = false
  notificacoes.notificar({ tipo: 'success', mensagem: novo ? 'Telefone adicionado.' : 'Telefone atualizado.', tempo: 4 })
  await recarregarTelefones()
  // Depois de recarregar, o botão de origem (ou "Adicionar telefone") volta a existir e recebe o foco
  await fecharFormularioTelefone(novo ? 'perfil-telefone-adicionar' : `perfil-telefone-editar-${edicao.id}`)
}

async function definirPrincipal(telefone) {
  if (acoesBloqueadas.value) return
  enviandoTelefone.value = true
  try {
    await api.telefones.atualizar(telefone.id, { e_principal: true })
  } catch (falha) {
    notificacoes.notificar({ tipo: 'danger', mensagem: mensagemErroTelefone(falha) })
    enviandoTelefone.value = false
    return
  }
  enviandoTelefone.value = false
  notificacoes.notificar({ tipo: 'success', mensagem: 'Telefone principal alterado.', tempo: 4 })
  // O backend desmarca o principal anterior: a lista é recarregada para refletir o banco
  await recarregarTelefones()
  await nextTick()
  document.getElementById(`perfil-telefone-editar-${telefone.id}`)?.focus()
}

// Espelho de exibição da regra: o backend continua recusando a exclusão indevida
function motivoBloqueioExclusao(telefone) {
  if (!telefones.value || telefones.value.length <= 1) return 'Mantenha ao menos um telefone cadastrado.'
  if (telefone.e_principal) return 'Para excluir o principal, defina outro telefone como principal antes.'
  return ''
}

function solicitarExclusao(telefone) {
  if (acoesBloqueadas.value || motivoBloqueioExclusao(telefone)) return
  telefoneParaExcluir.value = telefone
  exclusaoConcluida = false
  modalExcluirTelefone.value?.abrir()
}

async function excluirTelefone() {
  const telefone = telefoneParaExcluir.value
  if (!telefone) return
  enviandoTelefone.value = true
  try {
    await api.telefones.excluir(telefone.id)
  } catch (falha) {
    notificacoes.notificar({ tipo: 'danger', mensagem: mensagemErroTelefone(falha, 'Não foi possível excluir o telefone. Tente novamente.') })
    enviandoTelefone.value = false
    modalExcluirTelefone.value?.fechar()
    return
  }
  enviandoTelefone.value = false
  exclusaoConcluida = true
  modalExcluirTelefone.value?.fechar()
  notificacoes.notificar({ tipo: 'success', mensagem: 'Telefone excluído.', tempo: 4 })
  await recarregarTelefones()
}

// O botão "Excluir" do telefone removido some: o foco vai para "Adicionar telefone"
function aoFecharModalTelefone() {
  if (exclusaoConcluida) document.getElementById('perfil-telefone-adicionar')?.focus()
  exclusaoConcluida = false
  telefoneParaExcluir.value = null
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
.placeholder-telefone {
  min-height: 4.5rem;
}
.descricao-loja {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
