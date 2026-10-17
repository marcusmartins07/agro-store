---
name: agro-frontend
description: "Padrões do frontend do Agro Store (Vue 3, Vite, Vue Router, Pinia, Bootstrap 5): guia visual, paleta e tokens, tipografia, componentes compartilhados, estados, mocks, área do produtor, acessibilidade e checklist de alterações. Use ao criar, alterar, especificar ou revisar telas e componentes em apps/frontend/."
---

> Origem: `skills/frontend.md`. Referências a `.ai/skills/*.md` correspondem às skills `agro-*` desta pasta.

# Skill: Frontend

## Objetivo

Orientar alterações no frontend do Agro Store, desenvolvido em Vue 3 com Vite,
mantendo uma interface clara, acessível e coerente com o contexto da Feira do
Produtor Rural Willi Dummer.

## Localização

```text
apps/frontend/
```

## Tecnologias

- Vue 3.
- Vite.
- Vue Router.
- Pinia.
- Bootstrap 5.

Não instalar bibliotecas visuais, de ícones, de animação ou de estilos sem
autorização. O Bootstrap é a base do design system leve do projeto.

Exceções aprovadas, sem pacote npm:

- Fontes Fraunces (títulos) e DM Sans (texto) carregadas por `<link>` do Google
  Fonts em `index.html`. Sem conexão, os tokens caem para Georgia e a fonte do
  sistema, sem quebrar o layout.
- Ícones SVG inline no componente `src/components/IconeSvg.vue`, com traçados
  baseados no Lucide (licença ISC).

## Regras obrigatórias

- Usar Bootstrap como base visual e priorizar suas classes utilitárias e
  componentes antes de criar CSS local.
- Manter a identidade visual definida no protótipo (creme, verde-floresta e
  laranja) e os tokens globais em `src/assets/main.css`.
- Manter componentes simples e reutilizáveis.
- Não colocar regra de negócio crítica somente no frontend.
- Usar services para comunicação com a API.
- Usar stores Pinia para estados globais.
- Não duplicar chamadas de API sem necessidade.
- Tratar loading, vazio e erros de forma clara para o usuário.
- Não alterar regras de negócio, contratos da API ou autenticação por causa de
  uma melhoria visual.

## Organização esperada

```text
src/
├── api/
├── assets/
├── components/
├── layouts/
├── router/
├── services/
├── stores/
├── views/
├── types/
└── utils/
```

## Regras de autenticação

- Login deve salvar tokens conforme padrão existente.
- Requisições autenticadas devem enviar JWT.
- Quando o access token expirar, usar refresh token conforme implementação existente.
- Rotas privadas devem verificar autenticação.
- Não permitir ações de compra, carrinho, favoritos ou cadastro de produto sem login.

## Guia visual

### Princípios

- Priorizar clareza, legibilidade e rapidez de entendimento sobre sofisticação
  visual; as telas devem ser compreensíveis durante a apresentação do TCC.
- Usar uma linguagem visual acolhedora e simples, relacionada ao comércio rural,
  sem inserir elementos decorativos que prejudiquem a leitura ou o desempenho.
- Manter consistência entre vitrines públicas, carrinho, pedidos e áreas do
  produtor. Mudanças de papel do usuário não devem criar uma identidade visual
  incompatível.
- Manter uma linguagem profissional, objetiva e acolhedora em títulos, botões,
  rótulos, mensagens de ajuda e erros. Evitar termos excessivamente informais,
  promocionais ou ambíguos.
- Não usar emojis como elementos visuais da interface, incluindo navegação,
  botões, títulos, mensagens de estado, cards e campos de busca. Usar texto,
  componentes Bootstrap ou os ícones de `IconeSvg.vue`.
  Emojis recebidos como conteúdo do usuário ou da API devem ser preservados,
  sem que a interface dependa deles para comunicar uma ação ou estado.
- Usar CSS local apenas para comportamento visual que o Bootstrap e os tokens
  globais não resolvam adequadamente.

### Paleta e tokens

Usar nomes semânticos e as variáveis globais existentes. Ao criar ou ajustar
tokens em `src/assets/main.css`, centralizar o valor no arquivo global e nunca
replicar o hexadecimal em views ou componentes.

| Papel | Token ou classe de referência | Valor atual / uso |
| --- | --- | --- |
| Fundo da página | `--cor-fundo` | `#fbf6ec`; fundo geral (creme). |
| Superfície | `--cor-superficie` | `#fffdf9`; cards, campos, menus. |
| Texto principal | `--cor-texto` | `#2c1e13`; títulos e informações principais. |
| Texto secundário | `--cor-texto-secundario` e `text-body-secondary` | `#706052`; descrições e metadados. |
| Ação primária e marca | `--cor-primaria`, `--cor-primaria-hover` e `.btn-primary` | `#225a31` / `#134924`; botões, links, preço e logotipo, com texto `--cor-primaria-texto` (`#fbf8f1`). |
| Superfície de apoio | `--cor-apoio` e `.bg-apoio` | `#f2ebd9`; caixa de preço, resumo do carrinho, hover. |
| Superfície neutra | `--cor-neutra` e `.imagem-placeholder` | `#eee7d9`; fundo de imagens e áreas sem foto. |
| Destaque gráfico | `--cor-destaque` | `#ea6f2f`; somente elementos sem texto: estrelas e coração preenchido. |
| Destaque com texto | `--cor-destaque-forte` e `.badge-destaque` | `#bd4600`; badges de desconto e contadores, com texto branco. |
| Bordas | `--cor-borda` | `#e2dacc`; cards, divisórias e campos. |
| Foco | `--cor-foco` | `#488055`; anel de foco de campos, botões e links. |
| Erro e ação destrutiva | `--danger` e Bootstrap `danger` | `#dc2626`; exclusão, validação inválida e falhas. |
| Feedback | Bootstrap `success`, `warning`, `danger` e `info` | Usar alertas, badges e textos Bootstrap para cada significado. |
| Status do pedido | `--status-{pendente,preparo,pronto,entregue,cancelado}-{fundo,texto}` e `.selo-status.selo-*` | Texto escuro sobre tom claro (contraste de 6,6:1 a 7,6:1). Usar em selos de status de pedido, de produto (ativo/inativo) e de loja; sempre com o texto do status. |

- `main.css` também ajusta as variáveis do Bootstrap (`--bs-body-*`,
  `--bs-primary`, `--bs-border-color`, botões, campos, cards, dropdown e
  paginação) para que os componentes sigam a paleta sem CSS local.
- Os tokens antigos (`--green`, `--green-dark`, `--green-light`, `--white`,
  `--border`, `--star` etc.) são aliases legados dos novos. Não usá-los em
  código novo; migrá-los quando a tela for alterada.
- Nunca usar `--cor-destaque` como fundo de texto: o contraste com branco é
  2,99:1. Para badges com texto, usar `--cor-destaque-forte` (5,2:1).
- Não reutilizar a cor de destaque como alerta, nem a cor de erro para ações
  neutras.
- Uma nova cor só pode ser incluída após definir seu papel semântico, token
  global, estado de contraste e uso pretendido.
- Informações de sucesso, alerta, erro ou status não podem depender somente da
  cor: incluir texto, ícone quando já disponível ou rótulo explícito.

### Tipografia, espaçamento e superfícies

- Texto em `--fonte-texto` (DM Sans, com reserva `system-ui`). `h1` a `h3` e a
  classe `.fonte-titulo` usam `--fonte-titulo` (Fraunces, com reserva Georgia).
- Usar títulos Bootstrap (`h1` a `h6`) em ordem hierárquica: um `h1` por página,
  seções com `h2`/`h3` e textos auxiliares com classes como `small` ou
  `text-body-secondary`.
- Destacar preços por peso e tamanho tipográfico, preservando rótulos que
  expliquem o valor; não usar somente cor para dar destaque financeiro.
- Preferir a escala de espaçamento Bootstrap (`m-*`, `p-*`, `gap-*`) e seu grid
  responsivo, em vez de medidas arbitrárias no componente.
- Cards usam `.card` com `rounded-4` (20px), borda `--cor-borda` e conteúdo bem
  espaçado. Painéis de destaque (banner, galeria, login) usam `rounded-5`
  (24px). Botões de ação, chips e contadores usam `rounded-pill`.
- Usar sombras leves: `.sombra-suave` em repouso e `--sombra-elevada` apenas no
  hover de cards clicáveis.
- Gradiente só é permitido em `.fundo-destaque` (banner do catálogo e painel do
  login). Não criar outros gradientes.
- O conteúdo das páginas fica em `.container.app-container` (largura máxima de
  72rem).

### Componentes e estados

- Para layouts, usar `.container`, `.row` e colunas responsivas do Bootstrap.
- Para ações, usar `.btn` com variante semântica. A ação principal deve ser
  visualmente única; ações secundárias devem usar `outline`, `light` ou link de
  acordo com sua importância.
- A ação principal usa `.btn-primary`. `.btn-success` e `.btn-outline-success`
  seguem a mesma cor apenas por compatibilidade com telas antigas.
- Não redefinir `.btn-primary`, `.btn-success` ou outras classes do Bootstrap
  dentro de cada view. Se uma personalização global for necessária,
  centralizá-la em `src/assets/main.css`.
- `main.css` é importado logo após o Bootstrap, e os estilos dos componentes
  carregam depois dos dois; por isso, CSS local não precisa de `!important` para
  vencer o Bootstrap.
- Formulários devem usar `label` associado ao campo, `form-control` ou
  `form-select`, indicação textual de obrigatoriedade e feedback Bootstrap de
  validação.
- Cards, badges, alerts e placeholders devem usar os componentes Bootstrap antes
  de criar equivalentes próprios. Badges representam estado curto; alertas
  comunicam feedback ou erros que exigem atenção.
- Botões e controles devem ter estado normal, hover, foco visível, desabilitado
  e loading. No loading, impedir ação duplicada e informar o andamento sem
  remover o contexto da tela.
- Toda lista ou carregamento relevante deve prever estados de carregando, vazio,
  erro e sucesso de recarregamento, com mensagem e ação de recuperação quando
  aplicável.

### Componentes compartilhados

- `IconeSvg.vue`: ícones decorativos (`aria-hidden`). Quem usa o ícone fornece o
  texto acessível (rótulo visível, `visually-hidden` ou `aria-label`). Para um
  novo ícone, adicionar o traçado ao mapa do componente.
- `ProductCard.vue`: card do catálogo e dos favoritos. O card inteiro leva ao
  detalhe (`/produto/:id`); o favorito é um botão separado do link.
- `SeletorQuantidade.vue`: quantidade com `v-model`, `min`, `max` e `disabled`
  (detalhe do produto e carrinho).
- `AvaliacaoEstrelas.vue`: nota de 1 a 5 com texto acessível; a estrela vazia usa `--cor-texto-secundario`.
- `SeletorNota.vue`: seletor de nota de 1 a 5 com radios nativos (`fieldset` com `legend`), usado com `v-model`
  (número ou `null`). Props `desabilitado`, `invalido` e `idErro`; expõe `focar()`, que foca a opção marcada ou a primeira.
- `FormularioAvaliacao.vue`: formulário de apresentação da avaliação (nota e comentário de até 500 caracteres, com
  contador). Usa `v-model:nota` e `v-model:comentario`; recebe `nomeProduto`, `pedidoId`, `lojaNome`, `desabilitado`,
  `erro` e `erroNota`; emite `enviar` e expõe `focarNota()`. Não chama a API: quem o usa (ex.: `PedidosView.vue`, dentro
  do `ModalConfirmacao`) coordena o envio.
- `GaleriaProduto.vue`: carrossel com miniaturas do detalhe do produto. Recebe `produto.imagens`
  com a principal primeiro; sem imagens, exibe um único slide "Sem foto cadastrada".
- `src/utils/formatacao.js`: `formatarPreco`, `temDesconto`, máscaras (`mascaraCpf`,
  `mascaraTelefone`, `mascaraCnpj`), `formatarCpf`, `formatarTelefone`, `formatarData`,
  `calcularIdade` e `iniciaisDoNome`; não duplicar formatação de moeda, data ou documentos nas views.
  `mascaraTelefone` aplica `(XX) XXXX-XXXX` até 10 dígitos e `(XX) XXXXX-XXXX` com 11 (máx. 11);
  `placeholderTelefone`, `ajudaTelefone` e `validarTelefonePorTipo` espelham a RN-021 (Celular 11, Fixo 10,
  Comercial 10 ou 11) apenas para exibição.
- `FormularioTelefone.vue`: formulário de apresentação de um telefone (RN-021), com tipo e número, máscara dinâmica
  e erros no próprio campo. Props `idSufixo`, `tipos`, `telefone`, `tipoPadrao`, `erros` (`numero`, `tipo`, `geral`),
  `enviando` e `primeiro`; emite `salvar({ tipo, numero })` com o número só com dígitos e `cancelar`; expõe `focar()`.
  Não chama a API: o `PerfilView.vue` coordena o envio.
- `src/stores/tiposTelefone.js`: tipos de telefone públicos, carregados uma vez (cache) e reaproveitados pelo cadastro
  e pelo perfil; nunca usar ids fixos (localizar Celular pela `descricao`).
- `src/utils/statusPedido.js`: ordem, classe do selo e próxima ação de cada status do pedido
  (espelho de exibição do fluxo do backend, que continua validando as transições).
- `SeloStatus.vue`: badge de status com texto visível; `variante` aplica um selo que não é de pedido.
- `GraficoBarras.vue`: colunas de uma série em CSS, sem biblioteca, com dica ao passar o mouse e
  tabela oculta equivalente para leitores de tela.
- `CartaoPedidoKanban.vue`: cartão do quadro de pedidos do produtor; emite `avancar` e `cancelar`.
- `FormularioProduto.vue`: formulário lateral em offcanvas Bootstrap (cadastro e edição de produto).
  Formulários laterais usam a classe `Offcanvas` do bundle já importado em `main.js`
  (`import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.min.js'`), sem importar o Bootstrap de novo;
  ao desmontar com o painel aberto, fechar antes de `dispose()` e devolver o foco ao botão que o abriu.
  As imagens (até 5) são montadas localmente — envio, remoção, ordem e principal — e aplicadas por
  `useProdutorStore().salvarProduto` depois do produto e do preço; falhas de imagem não desfazem o produto salvo.
  O botão de recorte de cada miniatura abre o `EditorEnquadramento.vue` dentro do próprio painel (não em modal, que
  desligaria o focus trap do offcanvas). Uma imagem já salva ajustada é substituída ao salvar: a antiga entra nas
  remoções e a nova recortada ocupa a mesma posição e a marcação de principal.
- `EditorEnquadramento.vue`: mini editor de enquadramento quadrado (o mesmo `ratio-1x1` do catálogo) com grade 3×3,
  arraste por mouse/toque, setas do teclado, zoom e "Centralizar". Recebe `src` (URL `blob:` do original),
  `enquadramentoInicial`, `nomeArquivo` e `erroExterno`; emite `aplicar({ arquivo, enquadramento })` e `cancelar`.
- `src/utils/imagem.js`: recorte quadrado no navegador (Canvas, saída WEBP ou JPEG de até 1200 px) e download de
  imagens já salvas como blob para edição. O backend continua validando formato, tamanho e quantidade.
- `AvatarImagem.vue`: foto de perfil ou imagem da loja (RN-018). Props `src`, `nome`, `tamanho` (`sm`, `md`, `lg`, `xl`),
  `forma` (`circulo` ou `arredondado`), `quantidadeIniciais` (2 para pessoas, 1 para lojas) e `alt` (padrão vazio, porque o
  nome aparece em texto ao lado). Sem `src` ou quando a imagem falha (`@error`), mostra o marcador de iniciais (`aria-hidden`).
  Recorte por `object-fit: cover`, sem editor. Usado no perfil, no menu da conta, em `DadosLoja`, na criação da loja e no
  detalhe do produto; os cards do catálogo não usam.
- `SeletorImagemUnica.vue`: escolha de uma imagem única com prévia (`createObjectURL`/`revokeObjectURL`) e validação local
  de tipo (JPG, PNG, WEBP) e de 5 MB com as mensagens da RN-018. `v-model` (File ou `null`), `imagemAtual`, `nome`, `id`,
  `rotulo`, `rotuloOculto`, `ajuda`, `textoPendente` (anunciado em `aria-live`), `empilhado` (coluna centralizada, com o slot
  `apos-imagem` entre a imagem e os botões), `forma`, `tamanho`, `quantidadeIniciais`, `desabilitado`, `enviando` e `erro`; emite
  `selecionar`, `remover` (só com imagem salva e sem arquivo pendente) e `erro`; expõe `focar()` e `limparErro()`. Não chama
  a API: o slot `acoes` recebe "Salvar imagem"/"Cancelar" (perfil e `DadosLoja`, com remoção por `ModalConfirmacao`) ou
  "Descartar escolha" (criação da loja, enviada junto com o formulário). No perfil, o avatar do seletor é o único da página. Remoção só por DELETE; `mensagemErroEnvioImagem` e as mensagens
  de falha ficam em `src/utils/imagem.js`.
- `PainelAcesso.vue`: layout das telas de acesso (login, "Esqueci minha senha" e "Nova senha"): painel `.fundo-destaque`
  `rounded-5` à esquerda no md+ (oculto no celular) e `.card rounded-5 sombra-suave` com o formulário. Slot padrão para o
  conteúdo do card e slot `painel` para trocar o painel lateral. Sem o slot, mostra a marca "Bem-vindo à Agro Store"; a
  prop `tituloNoPainel` a renderiza como `h1` (só no login, cujo título principal fica no painel), senão como texto, para
  manter um único `h1` por página.
- `ModalConfirmacao.vue`: modal Bootstrap para confirmar ações (ex.: desativar produto), no lugar de
  `window.confirm`. Recebe `titulo`, `textoConfirmar`, `textoCarregando`, `variante` (padrão `danger`) e
  `carregando` e `rolavel` (padrão `false`; aplica `modal-dialog-scrollable` para o corpo rolar com cabeçalho e
  botões visíveis); a mensagem vai no slot; emite `confirmar` e `fechado` (em `hidden.bs.modal`, depois de devolver o
  foco ao gatilho) e expõe `abrir()`/`fechar()`. Segue o mesmo padrão do
  offcanvas (classe `Modal` do bundle, foco devolvido ao gatilho, fechamento antes de `dispose()`) e não fecha
  por Esc ou clique fora enquanto `carregando`.

### Dados mockados

- Dados que o backend ainda não fornece podem ser simulados no frontend apenas
  para exibição, em `src/data/mock*.js` ou no ponto de uso, sempre com o
  comentário `// MOCK:` explicando o motivo e o que o substituirá.
- Um mock nunca pode substituir uma validação ou regra de negócio do backend e
  deve ser identificado visualmente quando puder ser confundido com dado real
  (por exemplo, um rótulo "Imagem ilustrativa").
- Mock atual: miniatura neutra no carrinho (o item do carrinho não traz
  imagem). A galeria do produto usa as imagens reais da API desde a FE-005, e
  a recuperação de senha usa a API real desde a FE-022 (RN-020).

### Área do produtor

- Rota `/minha-loja` (`AreaProdutorView.vue`) com rotas filhas em `src/views/produtor/`: Painel,
  Pedidos (quadro kanban), Produtos e Minha loja. As abas são links (`nav-underline` com `aria-current`).
- O estado da área fica em `src/stores/produtor.js` (loja, produtos, pedidos, categorias e indicadores);
  as abas reaproveitam os dados carregados ao entrar na área. Limpar a store ao sair da conta.
- Endereços antigos (`/cliente`, `/loja`, `/loja/produtos`, `/loja/pedidos`) redirecionam para as novas rotas.

### Notificações globais

- Usar a store global de notificações para feedbacks que devem persistir entre rotas, como sucesso após login ou cadastro.
- Os tipos permitidos são `success`, `info`, `warning` e `danger`, sempre com texto e botão de fechar.
- O parâmetro opcional `tempo` é expresso em segundos; sem ele, a mensagem só desaparece ao fechar ou atualizar a página.
- Em login e cadastro, validações de entrada e erros retornados pela API devem usar notificação global `danger` permanente.

### CSS e estilos locais

- Novas cores devem usar tokens globais; não usar hexadecimais, RGB ou estilos
  inline em templates para valores já cobertos pelo guia.
- Priorizar classes Bootstrap e, em seguida, classes semânticas do componente.
- Estilos inline ou CSS com valor literal só são permitidos quando indispensáveis
  para um dado dinâmico ou uma exceção visual que não possa ser expressa por
  token ou utilitário; justificar a exceção no código ou na descrição da tarefa.
- Não duplicar em múltiplas views estilos de botão, card, borda ou cor. Extrair a
  regra para o CSS global ou um componente reutilizável quando ela for comum.
- Evitar `!important`. Usá-lo somente para vencer uma regra de terceiros que não
  possa ser resolvida por especificidade, escopo ou ordem de carregamento.

### Legibilidade e manutenção dos componentes

- Cada componente deve ter uma responsabilidade clara. Views compõem a tela e
  coordenam seus dados; componentes reutilizáveis recebem dados por `props` e
  comunicam ações por eventos sempre que não dependerem de estado global.
- Usar nomes descritivos e consistentes para componentes, `props`, eventos,
  variáveis, `computed` e funções. Evitar abreviações pouco claras e valores
  mágicos espalhados no template ou no script.
- Em novos componentes, manter a estrutura Vue legível: `template`, `script
  setup` e `style` separados; no script, organizar imports, `props`/emits,
  estado reativo, `computed`, ciclos de vida/watchers e funções.
- Declarar explicitamente a interface do componente com `defineProps` e,
  quando aplicável, `defineEmits`. Documentar por comentário apenas decisões ou
  regras não óbvias, e não o que o código já expressa claramente.
- Manter templates declarativos: lógica de apresentação simples pode ficar no
  template; condições extensas, formatação, cálculos e decisões reutilizadas
  devem ficar em `computed`, funções nomeadas ou utilitários.
- Dividir um componente quando ele passar a reunir responsabilidades distintas,
  repetir blocos de marcação ou dificultar localizar a regra que controla uma
  parte da tela. Não fragmentar componentes pequenos sem ganho de clareza.
- Centralizar chamadas HTTP nos services e regras/estado compartilhado nas
  stores. Um componente de apresentação não deve fazer chamadas à API
  diretamente.
- Manter estilos do componente próximos ao componente quando forem exclusivos;
  mover estilos e tokens reutilizados para o CSS global em vez de copiá-los.

### Responsividade e acessibilidade

- Usar os breakpoints Bootstrap e validar pelo menos em viewport móvel e desktop.
- Em telas pequenas, empilhar colunas, permitir quebra de textos longos e manter
  as ações principais visíveis sem depender de hover.
- Manter áreas clicáveis confortáveis para toque e não depender exclusivamente de
  ícones para ações importantes; usar `aria-label` em controles iconográficos.
- Garantir foco visível por teclado, contraste suficiente entre texto e fundo e
  associação entre rótulos, campos e mensagens de validação.
- Não transmitir estado apenas por cor, posição ou animação. Mensagens de erro,
  disponibilidade, estoque e status de pedido precisam de texto explícito.
- Respeitar `prefers-reduced-motion` caso uma animação seja realmente necessária;
  animações decorativas não são prioridade do MVP.

### Migração gradual

- Toda nova tela, componente ou estilo deve seguir este guia.
- Uma tela existente deve migrar cores literais, estilos inline e regras locais
  repetidas somente nas áreas modificadas pela tarefa atual. A mesma regra se
  aplica a emojis usados como decoração da interface.
- Não fazer refatoração visual global fora do escopo da demanda. Registrar uma
  oportunidade de padronização quando ela for identificada, se não puder ser
  resolvida sem ampliar a tarefa.

## Fluxos principais

O frontend deve apoiar os fluxos:

- Login.
- Cadastro de usuário.
- Vitrine de produtos.
- Página de loja/produtor.
- Detalhe de produto.
- Carrinho.
- Favoritos.
- Pedidos do cliente.
- Área do produtor.
- Cadastro e gestão de produtos.
- Atualização de status dos pedidos.

## Padrão para alterações

Ao alterar frontend:

1. Identificar tela ou componente afetado.
2. Verificar store relacionada.
3. Verificar service/API relacionada.
4. Verificar rota, se necessário.
5. Garantir que a tela funcione com autenticação.
6. Aplicar o guia visual: Bootstrap, tokens, estados, responsividade e acessibilidade.
7. Garantir tratamento de loading, vazio e erro.
8. Evitar estilos duplicados e migrar apenas o trecho existente tocado pela tarefa.
9. Explicar alterações feitas, regras de negócio impactadas e testes executados.
