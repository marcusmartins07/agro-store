# Telas do Agro Store — referência das telas do frontend

Documento derivado do código do frontend (`apps/frontend/src/`). Apresenta todas as telas do sistema, descreve o que cada uma faz e indica os
endpoints da API que ela consome. Os exemplos citados são fictícios e ambientados na Feira do Produtor Rural Willi Dummer (Camaquã/RS).

## 1. Introdução

### 1.1 Objetivo

Servir de base para a apresentação das telas no TCC e para consulta técnica: para cada tela, o documento registra a rota, o acesso, os componentes,
os estados (carregando, vazio, erro, sem login), as regras de negócio exibidas e as chamadas à API. Descreve apenas o que existe no código; telas
ou endpoints planejados não são documentados.

### 1.2 Fontes

O conteúdo foi levantado a partir de:

- `src/router/index.js` (rotas e guard de navegação) e `src/App.vue` (cabeçalho e elementos globais);
- `src/views/` e `src/views/produtor/` (telas);
- `src/components/` (componentes compartilhados);
- `src/stores/` (`auth.js`, `index.js` com carrinho e favoritos, `produtor.js`, `tiposTelefone.js`, `generos.js`, `notificacoes.js`);
- `src/services/api.js` (único ponto de comunicação HTTP com a API).

### 1.3 URL base e autenticação

- URL base da API: `/api/v1` (valor padrão de `API_BASE_URL`, que pode ser alterado pela variável `VITE_API_URL`). Todas as URLs das tabelas
  deste documento são relativas a essa base (ex.: `GET /produtos/` corresponde a `GET /api/v1/produtos/`). Em desenvolvimento, o Vite encaminha `/api`
  e `/media` para o backend (`http://127.0.0.1:8000`). Em produção, o frontend é publicado na Vercel (`<domínio da Vercel>`) e não usa esse proxy: `VITE_API_URL`
  e `VITE_BACKEND_URL` apontam para o backend publicado no Render (`<URL do backend>`).
- Formato: JSON; envios de imagem usam `multipart/form-data`.
- Sessão: após login ou cadastro, os tokens `access` e `refresh` e o objeto do usuário ficam no `localStorage`. A tela considera o usuário
  "logado" quando existe `access_token` salvo (`authStore.estaLogado`); a validade só é conferida quando a API responde 401.
- Todas as chamadas passam por `request()` em `services/api.js`, que envia `Authorization: Bearer <access>` quando há token salvo.
- Refresh automático: ao receber 401, `request()` chama `POST /usuarios/token/refresh/` com o `refresh` salvo, grava o novo `access` e repete a
  requisição uma única vez. Se o endpoint de refresh responder com erro, os tokens `access_token` e `refresh_token` são removidos e o navegador é levado para `/login`
  (a chave `usuario` do `localStorage` não é removida). Sem `refresh_token` salvo, ou com falha de rede na chamada de refresh, a função apenas lança uma exceção, sem remover tokens nem redirecionar.
  Login, cadastro, as duas chamadas de redefinição de senha, `GET /tipos-telefone/`, `GET /generos/` e `GET /lojas/lojas/{id}/` são enviados com `retry = false` (não tentam refresh);
  `api.auth.refresh` também, mas nenhuma tela a usa.
- Endpoints chamados sem token (`autenticar: false`): `GET /tipos-telefone/`, `GET /generos/`, `GET /lojas/lojas/{id}/`, `POST /usuarios/redefinir-senha/` e
  `POST /usuarios/redefinir-senha/confirmar/`. As demais chamadas, inclusive as de leitura pública (catálogo, detalhe do produto, categorias,
  avaliações) e as de login e cadastro, enviam o token quando ele existe.
- Erros: o service lança `{ status, data }` com o corpo JSON da resposta; cada tela traduz esse objeto em mensagem. Resposta 204 devolve `null`.
- Payloads, respostas e erros de cada endpoint estão em [`api-endpoints.md`](api-endpoints.md). Este documento só indica quais endpoints cada tela usa.

### 1.4 Prints das telas (`docs/telas/`)

Cada tela tem um espaço reservado para a captura de tela, no formato `![Figura N - <Nome>](telas/tela-NN-<slug>.png)`, com a legenda
"Figura N - <Nome>" logo abaixo. Os caminhos são relativos à pasta `docs/`, como no `TCC.md` (convertido com pandoc a partir de `docs/`).
As imagens ficam em `docs/telas/`. A pasta e os arquivos ainda não existem: a lista da seção 6 indica o que capturar em cada figura.

### 1.5 Convenções das tabelas de endpoints

- Método e URL seguem o `api-endpoints.md` (sem o prefixo `/api/v1`).
- A coluna "Função do service / store" indica a função de `services/api.js` (`api.grupo.funcao`) e, quando a chamada passa por uma store Pinia,
  a store e a ação.
- "Quando é chamado" descreve o gatilho na tela.

---

## 2. Mapa de rotas

Acesso: **público** (qualquer visitante), **autenticado** (exige login), **produtor** (usuário com `is_produtor`) e **produtor com loja**
(produtor que já possui loja).

| Rota | Nome | Tela (componente) | Acesso |
| --- | --- | --- | --- |
| `/` | `produtos` | Catálogo (`ProdutosView`) | público |
| `/produto/:id` | `produto` | Detalhe do produto (`ProdutoDetalheView`) | público (adicionar ao carrinho e favoritar pedem login) |
| `/loja/:id` | `loja` | Loja pública (`LojaView`) | público |
| `/carrinho` | `carrinho` | Carrinho (`CarrinhoView`) | autenticado, tratado na própria tela |
| `/favoritos` | `favoritos` | Favoritos (`FavoritosView`) | autenticado, tratado na própria tela |
| `/pedidos` | `pedidos` | Meus pedidos (`PedidosView`) | autenticado, tratado na própria tela |
| `/perfil` | `perfil` | Perfil (`PerfilView`) | autenticado, tratado na própria tela |
| `/login` | `login` | Login e Cadastro (`LoginView`) | público |
| `/esqueci-senha` | `esqueci-senha` | Esqueci a senha (`EsqueciSenhaView`) | público |
| `/redefinir-senha` | `redefinir-senha` | Redefinir senha (`RedefinirSenhaView`) | público (exige o token no fragmento da URL) |
| `/criar-loja` | `criar-loja` | Criar loja (`CriarLojaView`) | produtor sem loja |
| `/minha-loja` | `minha-loja` | Área do produtor (`AreaProdutorView`) com Painel (`PainelProdutor`) | produtor |
| `/minha-loja/pedidos` | `pedidos-produtor` | Pedidos em Kanban (`PedidosKanban`) | produtor com loja |
| `/minha-loja/produtos` | `produtos-produtor` | Produtos da loja (`ProdutosLoja`) | produtor com loja |
| `/minha-loja/loja` | `dados-loja` | Dados da loja (`DadosLoja`) | produtor com loja |

Redirecionamentos (endereços antigos):

| Rota | Destino |
| --- | --- |
| `/cliente` | `/perfil` |
| `/avaliacoes/:id` | `/pedidos` |
| `/loja` | `/minha-loja` |
| `/loja/produtos` | `/minha-loja/produtos` |
| `/loja/pedidos` | `/minha-loja/pedidos` |

Não existe rota de captura (página "não encontrado"): um caminho desconhecido mostra o cabeçalho com a área principal vazia.

### 2.1 Guard de navegação (`router.beforeEach`)

O guard só atua nas rotas com `meta.produtor` (`/minha-loja` e filhas, `/criar-loja`). Nas demais, a navegação segue livre.

1. Sem login (`estaLogado` falso): redireciona para `/login?retorno=<caminho original>`.
2. Com login: consulta `GET /usuarios/me/`, atualiza o usuário na store de autenticação e decide:
   - `is_produtor` falso: redireciona para o catálogo (`produtos`);
   - rota com `meta.loja` (`/minha-loja/pedidos`, `/minha-loja/produtos`, `/minha-loja/loja`) e usuário sem loja (`tem_loja` falso): redireciona para
     `/minha-loja`, que exibe o convite para criar a loja;
   - rota com `meta.semLoja` (`/criar-loja`) e usuário que já tem loja: redireciona para `/minha-loja`;
   - caso contrário, libera.
3. Qualquer falha na consulta a `/usuarios/me/` (inclusive de rede) redireciona para `/login?retorno=...`.

Como a consulta é feita a cada navegação para uma rota de produtor, trocar de aba dentro da Área do produtor dispara `GET /usuarios/me/` de novo.

### 2.2 Telas de cliente e usuário não logado

As rotas `/carrinho`, `/favoritos`, `/pedidos` e `/perfil` **não têm guard**: qualquer visitante abre a página. Cada view verifica `authStore.estaLogado` e, se
falso, mostra um cartão no lugar do conteúdo, sem chamar a API:

| Tela | Mensagem exibida sem login | Ação |
| --- | --- | --- |
| Carrinho | "Entre para usar o carrinho" — "Seu carrinho fica salvo na sua conta." | botão "Entrar" para `/login?retorno=<rota atual>` |
| Favoritos | "Entre para ver seus favoritos" | botão "Entrar" com `retorno` |
| Meus pedidos | "Entre para ver seus pedidos" — "Os pedidos ficam vinculados à sua conta." | botão "Entrar" com `retorno` |
| Perfil | "Entre para ver seu perfil" — "Seus dados ficam vinculados à sua conta." | botão "Entrar" com `retorno` |

O componente `PainelAcesso` **não** é usado para isso: ele é apenas o layout das telas de login, "Esqueci a senha" e "Redefinir senha" (seção 3.4).
No catálogo e no detalhe do produto, as ações que exigem login (favoritar, adicionar ao carrinho) redirecionam para `/login?retorno=<rota atual>`.
Depois do login ou do cadastro, a tela de acesso volta para `retorno` (apenas caminhos internos que começam com `/`) ou, sem ele, para o catálogo.

---

## 3. Elementos globais

### 3.1 Cabeçalho e navegação (`App.vue`)

Presente em todas as telas, acima da área principal (`RouterView`):

- **Marca "Agro Store"**: link para o catálogo (`/`).
- **Busca**: campo "Buscar cenoura, maçã, cuca, lojas..."; ao enviar, navega para `/?q=<termo>`. Não chama a API: o filtro é aplicado no navegador pelo catálogo.
- **Favoritos**: link para `/favoritos` com contador (`favoritosStore.itens.length`), exibido quando maior que zero.
- **Carrinho**: link para `/carrinho` com contador (`carrinhoStore.totalItens`, soma das quantidades de todos os itens de todos os carrinhos), exibido quando maior que zero.
- **Menu do usuário**:
  - logado: botão "Minha conta" (foto de perfil ou iniciais) com os itens "Meu perfil", "Minha loja" (somente quando `tem_loja` é verdadeiro), "Meus pedidos" e "Sair";
  - não logado: botão "Entrar" para `/login`.
- "Sair" não chama a API: remove os tokens e o usuário do `localStorage`, limpa as stores de carrinho, favoritos e produtor e vai para `/login`.

Chamadas disparadas pelo cabeçalho:

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| GET | `/carrinhos/` | ao montar o app já logado e quando `estaLogado` passa a verdadeiro | `api.carrinhos.listar` / `useCarrinhoStore().carregar` |
| GET | `/favoritos/` | idem (a store só recarrega se ainda não carregou) | `api.favoritos.listar` / `useFavoritosStore().carregar` |
| GET | `/usuarios/me/` | idem, e a cada mudança para as rotas `perfil` e `minha-loja`; define `tem_loja` e mantém a foto do menu atualizada | `api.usuarios.me` (função `carregarStatusLoja`) |

Quando `estaLogado` volta a falso, o cabeçalho limpa as stores locais sem chamar a API. Contadores e menu dependem apenas do estado local.

### 3.2 Notificações globais (`NotificacoesGlobais`)

Contêiner fixo no canto superior direito que exibe as notificações da store `notificacoes` (tipos `success`, `info`, `warning` e `danger`),
com botão de fechar e, opcionalmente, fechamento automático após `tempo` segundos. É usado por login, cadastro, redefinição de senha, catálogo e favoritos
(pelo `ProductCard`), detalhe do produto ("Produto adicionado ao carrinho." e favoritos), meus pedidos, perfil, criar loja ("Loja criada! Agora cadastre seus produtos.")
e Área do produtor. O carrinho não usa notificações: exibe os erros em alertas na própria tela. Não chama a API.

### 3.3 Modal de confirmação (`ModalConfirmacao`)

Modal Bootstrap reutilizável para confirmar ações, no lugar de `window.confirm`. Recebe título, textos dos botões, variante e estado `carregando`
(que bloqueia fechamento por Esc ou clique fora durante a ação); o corpo vem por slot. Não chama a API: a tela que o usa executa a chamada ao
receber o evento `confirmar`.

| Tela | Modais |
| --- | --- |
| Meus pedidos | "Avaliar produto", "Cancelar pedido", "Confirmar recebimento" |
| Perfil | "Remover foto de perfil?", "Excluir telefone?" |
| Pedidos em Kanban | "Cancelar pedido" |
| Produtos da loja | "Desativar produto" |
| Dados da loja | "Remover imagem da loja?", "Desativar loja?" |

### 3.4 Painel de acesso (`PainelAcesso`)

Layout das telas de acesso: painel de destaque à esquerda (oculto no celular) com a marca "Bem-vindo à Agro Store" e um cartão com o formulário. É
usado por `LoginView`, `EsqueciSenhaView` e `RedefinirSenhaView`. Não verifica login nem chama a API.

### 3.5 Outros componentes que disparam chamadas

- `ProductCard` (catálogo e favoritos): o botão de coração chama `favoritosStore.alternar`, que usa `POST /favoritos/` ou `DELETE /favoritos/{favorito_id}/`.
  Sem login, o botão leva ao login.
- `FormularioProduto` (Produtos da loja): ao salvar, chama `produtorStore.salvarProduto`, que dispara as chamadas de produto, preço e imagens da seção 4.3.5.
  O componente também baixa por `fetch`, a partir da URL de mídia, a imagem já salva que será ajustada (`carregarImagemParaEdicao`, em `utils/imagem.js`); isso não é endpoint da API.
- Os demais componentes (`GaleriaProduto`, `SeletorQuantidade`, `SeletorImagemUnica`, `FormularioTelefone`, `FormularioAvaliacao`, `CartaoPedidoKanban`,
  `GraficoBarras`, `EditorEnquadramento` etc.) são de apresentação e não chamam a API.

---

## 4. Telas

### 4.1 Acesso

#### 4.1.1 Login e Cadastro (`LoginView`)

- Rota: `/login`
- Acesso: público

![Figura 1 - Login](telas/tela-01-login.png)

Figura 1 - Login

![Figura 2 - Cadastro de cliente](telas/tela-02-cadastro.png)

Figura 2 - Cadastro de cliente

**Para que serve.** Tela única com duas abas: "Entrar" e "Criar conta". No login, o usuário informa CPF e senha; há o link "Esqueci minha senha" e
os campos de senha têm o botão "Mostrar/Ocultar". No cadastro, informa nome completo, CPF, tipo e número do telefone, e-mail, data de nascimento,
gênero (Masculino, Feminino, Prefiro não informar), senha e confirmação. Em caso de sucesso, a sessão é salva, aparece uma notificação de sucesso
(10 s) e o usuário é levado a `retorno` ou ao catálogo.

**Componentes principais.** `PainelAcesso`, store `auth` (`login`, `cadastrar`), store `tiposTelefone`, `NotificacoesGlobais`. Máscaras de CPF e telefone em `utils/formatacao.js`.

**Estados e regras.**

- Carregando: botões mostram "Entrando..." e "Criando conta..." com spinner.
- Erros de validação local (campos obrigatórios, telefone conforme o tipo, senha com no mínimo 8 caracteres, confirmação igual) e erros devolvidos pela API
  aparecem como notificação `danger` permanente; sem resposta do servidor, a mensagem é "Não foi possível conectar ao servidor. Tente novamente." (login) ou
  "Não foi possível criar a conta. Tente novamente." (cadastro).
- O frontend não valida a validade do CPF nem a idade mínima: essas recusas vêm do backend.
- Tipos de telefone: ao abrir a aba "Criar conta", a lista é carregada ("Carregando tipos..."); se falhar, um alerta com "Tentar novamente" aparece e o
  botão "Criar conta" fica desabilitado até a lista estar disponível. O tipo "Celular" vem pré-selecionado.
- A rota não redireciona quem já está logado.
- Regras: o cadastro público cria somente conta de cliente e inicia a sessão automaticamente; telefone e tipo informados no cadastro viram o telefone principal
  (RN-021); CPF único, idade mínima de 16 anos e senha validados no backend.

**Endpoints.**

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| POST | `/usuarios/login/` | ao enviar a aba "Entrar" | `api.auth.login` / `useAuthStore().login` |
| POST | `/usuarios/cadastro/` | ao enviar a aba "Criar conta" | `api.auth.cadastrar` / `useAuthStore().cadastrar` |
| GET | `/tipos-telefone/` | ao abrir a aba "Criar conta" e em "Tentar novamente", somente se a store ainda não tiver os tipos (cache); sem token | `api.tiposTelefone.listar` / `useTiposTelefoneStore().carregar` |
| GET | `/generos/` | ao abrir a aba "Criar conta", somente se a store ainda não tiver as opções (cache); sem token; o formulário envia o `codigo` | `api.generos.listar` / store `generos` |

#### 4.1.2 Esqueci a senha (`EsqueciSenhaView`)

- Rota: `/esqueci-senha`
- Acesso: público

![Figura 3 - Esqueci a senha](telas/tela-03-esqueci-senha.png)

Figura 3 - Esqueci a senha

![Figura 4 - Esqueci a senha, link solicitado](telas/tela-04-esqueci-senha-enviado.png)

Figura 4 - Esqueci a senha, link solicitado

**Para que serve.** O usuário informa o e-mail da conta e solicita o link de redefinição (válido por 30 minutos). Depois do envio, a tela mostra a
mensagem neutra devolvida pela API e o botão "Usar outro e-mail". Há o link "Voltar para o login".

**Componentes principais.** `PainelAcesso`; `utils/redefinicaoSenha.js` (mensagens de erro geral).

**Estados e regras.**

- Validação local: e-mail vazio ("Informe o e-mail da sua conta.") ou em formato inválido ("Informe um e-mail válido, como nome@exemplo.com.").
- Carregando: botão "Enviando...".
- Sucesso: alerta com a mensagem da API (a mesma exista ou não conta, RN-020) e aviso para verificar o spam.
- Resposta 400: marca o campo como inválido; 429: alerta `warning` com a mensagem de limite ("Muitas solicitações. Tente novamente mais tarde."); falha de rede ou outro erro:
  alerta `danger`.
- RN-020: resposta neutra, limite de solicitações por origem e link de uso único.

**Endpoints.**

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| POST | `/usuarios/redefinir-senha/` | ao enviar o formulário; sem token | `api.auth.solicitarRedefinicaoSenha` |

#### 4.1.3 Redefinir senha (`RedefinirSenhaView`)

- Rota: `/redefinir-senha#token=<token>` (o token vem do link enviado por e-mail)
- Acesso: público

![Figura 5 - Redefinir senha](telas/tela-05-redefinir-senha.png)

Figura 5 - Redefinir senha

**Para que serve.** Permite cadastrar a nova senha a partir do link recebido. A tela lê o token do fragmento da URL e o remove do endereço logo após abrir
(`router.replace`). O usuário informa a nova senha e a confirmação (com botões "Mostrar/Ocultar").

**Componentes principais.** `PainelAcesso`; stores `auth`, `notificacoes` e `produtor`.

**Estados e regras.**

- Sem token na URL, ou quando a API recusa o token: mensagem "Este link de redefinição é inválido ou expirou. Solicite um novo." e botão "Solicitar novo link" (`/esqueci-senha`).
- Validação local: senha obrigatória com no mínimo 8 caracteres; confirmação obrigatória e igual à senha. Erros de `password` e `password_confirmacao` devolvidos pela API aparecem
  abaixo dos campos.
- Carregando: botão "Salvando...".
- Sucesso: a sessão local é encerrada (`authStore.logout()` e limpeza da store do produtor), aparece a notificação "Senha redefinida. Entre com a nova senha." (10 s) e o usuário vai para `/login`.
  O usuário não é autenticado automaticamente (RN-020).
- Falhas de rede ou 429: alerta geral.

**Endpoints.**

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| POST | `/usuarios/redefinir-senha/confirmar/` | ao enviar a nova senha; sem token de sessão | `api.auth.confirmarRedefinicaoSenha` |

### 4.2 Cliente

#### 4.2.1 Catálogo (`ProdutosView`)

- Rota: `/`
- Acesso: público

![Figura 6 - Catálogo de produtos](telas/tela-06-catalogo.png)

Figura 6 - Catálogo de produtos

**Para que serve.** Vitrine de produtos. Mostra um banner com a informação de retirada na feira (texto fixo de `data/feira.js`, RN-008), os filtros por categoria
("Todos" mais as categorias ativas), a ordenação (Relevância, Menor preço, Maior preço e Com desconto, que também filtra apenas os produtos com desconto maior que zero) e a grade de cartões de produto, com 9 itens por página e paginação.
Busca (`q`), categoria, ordenação e página ficam na URL (`/?q=&categoria=&ordem=&pagina=`). O usuário pode abrir o detalhe de um produto e favoritar pelo coração do cartão.

**Componentes principais.** `ProductCard`, `IconeSvg`, store `favoritos`.

**Estados e regras.**

- Carregando: seis cartões de espaço reservado.
- Erro: alerta "Não foi possível carregar os produtos." com "Tentar novamente".
- Vazio: "Nenhum produto encontrado." com "Limpar filtros".
- Busca (nome, descrição, loja e categoria), filtro de categoria, ordenação e paginação são feitos no navegador sobre a lista completa recebida; nenhum parâmetro é enviado à API.
- A API só devolve produtos ativos, de loja ativa e com estoque maior que zero (RN-017); por isso produto sem estoque não aparece no catálogo.
- O cartão mostra imagem principal, loja, nome, descrição, preço, preço original riscado e selo de desconto; "Sem foto" quando não há imagem.
- Favoritar sem login leva ao login com `retorno`.

**Endpoints.**

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| GET | `/produtos/` | ao abrir a tela (em paralelo com as categorias) e em "Tentar novamente" | `api.produtos.listar` |
| GET | `/produtos/categorias/?ativo=true` | idem | `api.categorias.listar` |
| POST | `/favoritos/` | ao favoritar pelo coração do cartão | `api.favoritos.adicionar` / `useFavoritosStore().alternar` |
| DELETE | `/favoritos/{favorito_id}/` | ao desfavoritar pelo coração do cartão | `api.favoritos.remover` / `useFavoritosStore().alternar` |

#### 4.2.2 Detalhe do produto (`ProdutoDetalheView`)

- Rota: `/produto/:id`
- Acesso: público (adicionar ao carrinho e favoritar exigem login)

![Figura 7 - Detalhe do produto](telas/tela-07-detalhe-produto.png)

Figura 7 - Detalhe do produto

![Figura 8 - Avaliações do produto](telas/tela-08-detalhe-produto-avaliacoes.png)

Figura 8 - Avaliações do produto

**Para que serve.** Apresenta um produto: galeria de imagens (a principal primeiro; "Sem foto cadastrada" quando não há imagem), loja com imagem ou inicial (sem link), nome,
média e quantidade de avaliações (com atalho para a seção), preço com desconto, disponibilidade, seletor de quantidade, botões "Adicionar ao carrinho" e "Favoritar",
o texto de retirada e a descrição. Abaixo, a seção "Avaliações" lista nota, nome abreviado do avaliador e comentário.

**Componentes principais.** `GaleriaProduto`, `AvatarImagem`, `AvaliacaoEstrelas`, `SeletorQuantidade`, stores `carrinho`, `favoritos`, `auth`.

**Estados e regras.**

- Carregando: espaços reservados; produto inexistente, inativo ou de loja inativa (404): "Produto não encontrado ou indisponível" com "Voltar ao catálogo"; outro erro: alerta com "Tentar novamente".
- Disponibilidade: "Disponível: N em estoque", "Produto inativo", "Preço indisponível no momento" ou "Sem estoque" (o texto "Produto inativo" existe no código, mas na prática não aparece: a API responde 404 para produto inativo). Fora do primeiro caso, quantidade e botão de compra ficam desabilitados
  (o backend também recusa a compra, RN-017). O detalhe de produto sem estoque abre pelo link direto.
- A quantidade vai de 1 até o estoque. Sucesso ao adicionar: notificação "Produto adicionado ao carrinho." (4 s); erro: notificação `danger` com a mensagem da API.
- Sem login, "Adicionar ao carrinho" e "Favoritar" levam ao login com `retorno`.
- Avaliações: carregando, erro (alerta com "Tentar novamente") e vazio ("Este produto ainda não possui avaliações."). A média é calculada no navegador apenas para exibição (RN-010); o nome do avaliador
  já chega abreviado da API.
- A imagem da loja é buscada à parte; se a busca falhar ou a loja não tiver imagem, aparece a inicial do nome (RN-018).
- Regras citadas: RN-008 (retirada), RN-010 (avaliações públicas), RN-016 (galeria), RN-017 (estoque), RN-018 (imagem da loja).

**Endpoints.**

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| GET | `/produtos/{id}/` | ao abrir a tela e ao trocar de produto | `api.produtos.obter` |
| GET | `/avaliacoes/?produto={id}` | ao abrir a tela | `api.avaliacoes.listarPorProduto` |
| GET | `/lojas/lojas/{loja_id}/` | depois de carregar o produto, só para a imagem da loja; sem token | `api.lojas.obter` |
| POST | `/carrinhos/` | em "Adicionar ao carrinho" (depois recarrega `GET /carrinhos/`) | `api.carrinhos.adicionar` / `useCarrinhoStore().adicionar` |
| GET | `/carrinhos/` | após adicionar ao carrinho | `api.carrinhos.listar` / `useCarrinhoStore().carregar` |
| POST | `/favoritos/` | em "Favoritar" | `api.favoritos.adicionar` / `useFavoritosStore().alternar` |
| DELETE | `/favoritos/{favorito_id}/` | em "Favoritado" (desfavoritar) | `api.favoritos.remover` / `useFavoritosStore().alternar` |

#### 4.2.3 Loja pública (`LojaView`)

- Rota: `/loja/:id`
- Acesso: público

![Figura 9 - Loja pública](telas/tela-09-loja-publica.png)

Figura 9 - Loja pública

**Para que serve.** A tela ainda é um espaço reservado: exibe apenas o cartão "Em breve — Esta tela estará disponível em breve.". Não lê o parâmetro `:id`, não usa store e
**não chama a API**; não há dados simulados nem listagem de produtos da loja. A página pública da loja consta como funcionalidade futura nas regras de negócio.

A tela é alvo de dois links: o nome da loja em cada cartão de pedido (Meus pedidos) e o botão "Ver minha vitrine" (Dados da loja).

**Componentes principais.** Nenhum além do próprio cartão.

**Endpoints.** Nenhum.

#### 4.2.4 Carrinho (`CarrinhoView`)

- Rota: `/carrinho`
- Acesso: autenticado (verificado na própria tela; sem login, mostra o cartão da seção 2.2)

![Figura 10 - Carrinho](telas/tela-10-carrinho.png)

Figura 10 - Carrinho

**Para que serve.** Reúne os itens do cliente agrupados por loja. Cada item tem caixa de seleção, miniatura neutra (o item do carrinho não traz imagem), nome com link para o
produto, preço unitário líquido, seletor de quantidade, subtotal e botão de remover. O resumo mostra itens selecionados, subtotal, descontos e total; com itens de mais de uma loja,
lista o valor por loja e informa que será gerado um pedido para cada uma (RN-011). Há o texto de retirada (RN-008), o botão "Finalizar pedido" e o link "Continuar comprando".
Ao carregar, todos os itens finalizáveis vêm selecionados; só os itens selecionados são enviados na finalização. Sucesso leva a `/pedidos`.

**Componentes principais.** `SeletorQuantidade`, `SeloStatus`, `IconeSvg`, store `carrinho`.

**Estados e regras.**

- Sem login, carregando ("Carregando carrinho..."), erro de carregamento (com "Tentar novamente"), vazio ("Seu carrinho está vazio" com "Explorar produtos"), erro de ação (alerta sobre a lista),
  erro de finalização (alerta no resumo) e finalizando ("Finalizando...").
- Situação por item (RN-017):
  - "Indisponível": produto ou loja indisponível com estoque maior que zero; não entra no pedido;
  - "Sem estoque": item indisponível sem estoque; não entra no pedido;
  - "Disponível novamente": item com quantidade 0 cujo estoque voltou; o cliente precisa aumentar a quantidade para incluí-lo;
  - "Máximo disponível: N" quando a quantidade chegou ao estoque.
- Itens não finalizáveis ficam com a caixa desabilitada e são contados na mensagem "N itens do carrinho não entram no pedido".
- Reduzir abaixo de 1 não é permitido no seletor; para tirar o item, usa-se o botão de remover.
- Totais exibidos são calculados no navegador a partir dos valores do item; o backend recalcula tudo na finalização com o preço vigente.
- Regras citadas: RN-008, RN-011, RN-017. O carrinho é salvo no backend, um por loja, e o frontend os agrega.

**Endpoints.**

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| GET | `/carrinhos/` | ao abrir a tela (logado), após cada alteração e após a finalização | `api.carrinhos.listar` / `useCarrinhoStore().carregar` |
| PATCH | `/carrinhos/itens/{item_id}/` | ao mudar a quantidade de um item | `api.carrinhos.atualizarItem` / `useCarrinhoStore().alterarQuantidade` |
| DELETE | `/carrinhos/itens/{item_id}/` | no botão de remover | `api.carrinhos.removerItem` / `useCarrinhoStore().remover` |
| POST | `/pedidos/` | em "Finalizar pedido", com `carrinho_produto_ids` dos itens selecionados | `api.pedidos.finalizarCarrinho` / `useCarrinhoStore().finalizar` |

#### 4.2.5 Favoritos (`FavoritosView`)

- Rota: `/favoritos`
- Acesso: autenticado (verificado na própria tela)

![Figura 11 - Favoritos](telas/tela-11-favoritos.png)

Figura 11 - Favoritos

**Para que serve.** Lista os produtos favoritados, do mais recente para o mais antigo, usando o mesmo cartão do catálogo. O coração do cartão remove o favorito; o cartão leva ao detalhe.
Há o botão "Ver catálogo".

**Componentes principais.** `ProductCard`, store `favoritos`.

**Estados e regras.**

- Sem login (cartão da seção 2.2), carregando (três cartões de espaço reservado), erro (com "Tentar novamente", que força o recarregamento), vazio ("Nenhum favorito ainda" com "Explorar produtos").
- Produtos inativos, sem estoque ou de loja inativa permanecem na lista com a mensagem "Produto inativo", "Sem estoque" ou "Produto indisponível" no cartão; a compra só é possível pelo detalhe do produto,
  que bloqueia o que não está disponível.
- A store só carrega a lista uma vez por sessão (o cabeçalho já a carrega), salvo recarregamento forçado.

**Endpoints.**

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| GET | `/favoritos/` | ao abrir a tela, se a lista ainda não foi carregada, e em "Tentar novamente" | `api.favoritos.listar` / `useFavoritosStore().carregar` |
| DELETE | `/favoritos/{favorito_id}/` | ao clicar no coração de um favorito | `api.favoritos.remover` / `useFavoritosStore().alternar` |

#### 4.2.6 Meus pedidos (`PedidosView`)

- Rota: `/pedidos`
- Acesso: autenticado (verificado na própria tela)

![Figura 12 - Meus pedidos](telas/tela-12-pedidos.png)

Figura 12 - Meus pedidos

![Figura 13 - Avaliar produto](telas/tela-13-pedidos-avaliar.png)

Figura 13 - Avaliar produto

![Figura 14 - Cancelar pedido](telas/tela-14-pedidos-cancelar.png)

Figura 14 - Cancelar pedido

![Figura 15 - Confirmar recebimento](telas/tela-15-pedidos-confirmar-recebimento.png)

Figura 15 - Confirmar recebimento

**Para que serve.** Acompanhamento dos pedidos do cliente, do mais recente para o mais antigo, com filtro por status (Todos e os cinco status, cada um com a contagem). Cada pedido mostra número, data,
loja (link para `/loja/:id`), selo de status, tabela de itens (produto, quantidade, subtotal) e resumo de valores (bruto, desconto, total). Ações:

- **Cancelar pedido** (somente status `Pendente`): abre o modal "Cancelar pedido" ("Os produtos voltam ao estoque da loja e o pedido fica no seu histórico como Cancelado."), com os botões "Cancelar pedido" e "Manter pedido".
- **Confirmar recebimento** (somente `Pronto para retirada`): abre o modal "Confirmar recebimento" (o pedido passa a `Entregue`; a ação não pode ser desfeita), com os botões "Confirmar recebimento" e "Voltar".
- **Avaliar** (por item, em pedidos `Entregue` ainda não avaliados): abre o modal "Avaliar produto" com nota de 1 a 5 (obrigatória), comentário opcional de até 500 caracteres e o aviso de que a avaliação não pode ser
  editada nem removida. Item já avaliado mostra as estrelas, "Avaliado" e o link "Ver no produto" (seção de avaliações). Item cujo produto foi excluído mostra "Produto não está mais disponível".

**Componentes principais.** `ModalConfirmacao` (três instâncias), `FormularioAvaliacao` (que usa `SeletorNota`), `AvaliacaoEstrelas`, `SeloStatus`.

**Estados e regras.**

- Sem login (cartão da seção 2.2), carregando (espaços reservados), erro (com "Tentar novamente"), vazio ("Você ainda não fez pedidos" com "Explorar produtos") e filtro sem resultado
  (com "Ver todos os pedidos").
- Cancelamento e confirmação atualizam o pedido na lista com a resposta da API e disparam notificação de sucesso; falhas geram notificação `danger`. Na confirmação, um erro 400 recarrega a lista.
- Avaliação: sem nota, o modal mostra "Escolha uma nota de 1 a 5 estrelas."; "Este item já foi avaliado." fecha o modal, mostra aviso e recarrega a lista; falha de rede mostra mensagem no modal.
  Sucesso: notificação "Avaliação enviada. Obrigado por ajudar outros clientes.".
- O texto de retirada (RN-008) aparece no topo. O telefone do cliente não faz parte desta tela.
- Regras citadas: RN-010 (avaliação de item entregue, uma vez por item, nome abreviado público), RN-011 (um pedido por loja), RN-019 (snapshot do item: nome e valores permanecem mesmo com produto excluído),
  RN-022 (confirmação de recebimento pelo cliente), cancelamento de pedido pendente com restauração de estoque. A validação final de todas as regras é do backend.

**Endpoints.**

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| GET | `/pedidos/` | ao abrir a tela (logado), em "Tentar novamente" e após avaliação já registrada ou erro 400 na confirmação | `api.pedidos.listar` |
| PATCH | `/pedidos/{id}/cancelar/` | ao confirmar o modal "Cancelar pedido" | `api.pedidos.cancelar` |
| PATCH | `/pedidos/{id}/confirmar-entrega/` | ao confirmar o modal "Confirmar recebimento" | `api.pedidos.confirmarEntrega` |
| POST | `/avaliacoes/` | ao enviar o modal "Avaliar produto" (`pedido_produto`, `nota`, `comentario`) | `api.avaliacoes.criar` |

#### 4.2.7 Perfil (`PerfilView`)

- Rota: `/perfil` (`/cliente` redireciona para cá)
- Acesso: autenticado (verificado na própria tela)

![Figura 16 - Perfil](telas/tela-16-perfil.png)

Figura 16 - Perfil

![Figura 17 - Telefones do perfil](telas/tela-17-perfil-telefones.png)

Figura 17 - Telefones do perfil

**Para que serve.** Reúne os dados da conta, em quatro blocos:

- **Foto e identificação**: foto de perfil (ou iniciais) com "Escolher/Trocar imagem", "Salvar imagem", "Cancelar" e "Remover imagem" (com modal de confirmação), nome, e-mail e selo "Produtor rural" ou "Cliente" (RN-018).
- **Loja**: para quem tem loja, resumo (nome, status, descrição) e "Gerenciar minha loja"; para produtor sem loja, "Gostaria de abrir uma loja?" com "Criar minha loja"; para quem não é produtor, apenas a
  orientação de procurar a organização da Feira para solicitar a habilitação (sem botão de criação de loja).
- **Informações pessoais**: leitura de nome, e-mail, CPF, data de nascimento, idade e gênero, com o botão "Editar" para alterar nome, e-mail, data de nascimento e gênero. O CPF não pode ser alterado.
- **Telefones** (RN-021): lista com tipo e selo "Principal", "Adicionar telefone", "Editar", "Definir como principal" e "Excluir" (com modal). Formulário de telefone com tipo e número com máscara.

**Componentes principais.** `SeletorImagemUnica`, `AvatarImagem`, `FormularioTelefone`, `ModalConfirmacao`, stores `auth` e `tiposTelefone`.

**Estados e regras.**

- Sem login (cartão da seção 2.2), carregando, erro (com "Tentar novamente"); a falha ao buscar a loja não impede exibir o perfil.
- Telefones: carregando, erro (com "Tentar novamente"), lista vazia (aviso "Você ainda não tem um telefone cadastrado.", para contas legadas), erro de carregamento dos tipos (alerta com "Tentar novamente").
  A exclusão é bloqueada com texto explicativo quando é o único telefone ("Mantenha ao menos um telefone cadastrado.") ou o principal ("Para excluir o principal, defina outro telefone como principal antes.").
- Erros de campo (nome, e-mail, data de nascimento, gênero, número, tipo) aparecem no próprio campo; recusas de foto mostram a mensagem de RN-018 (JPG, PNG ou WEBP de até 5 MB), mantendo a foto atual.
- Alterações bem-sucedidas geram notificação de sucesso (4 s) e atualizam o usuário na store de autenticação (a foto do menu acompanha).
- Regras citadas: RN-018 (foto única, opcional, visível só ao próprio usuário), RN-021 (um ou mais telefones, exatamente um principal, validação por tipo no backend), e a regra de que CPF e papéis não são alterados pelo usuário.

**Endpoints.**

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| GET | `/usuarios/me/` | ao abrir a tela; a resposta já traz os telefones | `api.usuarios.me` |
| GET | `/lojas/me/` | ao abrir a tela, se `tem_loja` for verdadeiro | `api.lojas.me` |
| GET | `/tipos-telefone/` | ao abrir a tela, somente se a store ainda não tiver os tipos (cache); sem token | `api.tiposTelefone.listar` / `useTiposTelefoneStore().carregar` |
| GET | `/generos/` | ao abrir a tela, somente se a store ainda não tiver as opções (cache); sem token | `api.generos.listar` / store `generos` |
| PATCH | `/usuarios/me/` (JSON) | ao salvar "Informações pessoais" | `api.usuarios.atualizar` |
| PATCH | `/usuarios/me/` (multipart, campo `foto_perfil`) | em "Salvar imagem" | `api.usuarios.atualizarFoto` |
| DELETE | `/usuarios/me/foto/` | ao confirmar "Remover foto de perfil?" (404 é tratado como já removida) | `api.usuarios.removerFoto` |
| GET | `/usuarios/me/telefones/` | após cada alteração de telefone e em "Tentar novamente" (ou se `/me/` não trouxer a lista) | `api.telefones.listar` |
| POST | `/usuarios/me/telefones/` | ao salvar um telefone novo | `api.telefones.criar` |
| PATCH | `/usuarios/me/telefones/{id}/` | ao editar número/tipo e em "Definir como principal" (`e_principal: true`) | `api.telefones.atualizar` |
| DELETE | `/usuarios/me/telefones/{id}/` | ao confirmar "Excluir telefone?" | `api.telefones.excluir` |

### 4.3 Produtor

#### 4.3.1 Criar loja (`CriarLojaView`)

- Rota: `/criar-loja`
- Acesso: produtor sem loja (`meta.produtor` e `meta.semLoja`; produtor com loja é levado a `/minha-loja`)

![Figura 18 - Criar loja](telas/tela-18-criar-loja.png)

Figura 18 - Criar loja

**Para que serve.** O produtor cria a sua loja informando nome, descrição, CNPJ (máscara; 14 dígitos exigidos no formulário) e, opcionalmente, a imagem da loja (com prévia e "Descartar escolha").
Os botões são "Cancelar" (volta à tela anterior) e "Criar loja". Sucesso: notificação "Loja criada! Agora cadastre seus produtos." (6 s) e redirecionamento para `/minha-loja`.

**Componentes principais.** `SeletorImagemUnica` (que usa `AvatarImagem` para a prévia, com a inicial da loja), store `notificacoes`.

**Estados e regras.**

- Carregando: botão "Criando...".
- Validação local: "Informe o nome da loja e um CNPJ com 14 dígitos.". Erros da API: CNPJ ("CNPJ inválido ou já cadastrado."), mensagem geral (ex.: regra de uma loja por produtor) e imagem recusada
  (mensagem no campo, arquivo descartado e foco devolvido ao seletor).
- Regras citadas: RN-013 (uma loja por produtor, validada no backend), RN-018 (imagem opcional na criação; se inválida, a loja não é criada).

**Endpoints.**

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| POST | `/lojas/lojas/` | ao enviar o formulário (JSON; multipart quando há imagem) | `api.lojas.criar` |

(O guard consulta `GET /usuarios/me/` antes de abrir a tela; ver seção 2.1.)

#### 4.3.2 Área do produtor (`AreaProdutorView`, layout)

- Rota: `/minha-loja` (rotas filhas em `/minha-loja/...`; `/loja` redireciona para cá)
- Acesso: produtor

![Figura 19 - Área do produtor sem loja](telas/tela-19-area-produtor-sem-loja.png)

Figura 19 - Área do produtor sem loja

**Para que serve.** Moldura comum das telas do produtor. Mostra o título "Área do produtor", o nome da loja com o selo "Loja ativa/Loja inativa", o botão "Novo produto"
(leva a `/minha-loja/produtos?novo=1`, que abre o formulário), cinco indicadores (Produtos ativos, Produtos inativos, Pedidos pendentes, Em andamento — `Em preparo` mais
`Pronto para retirada` — e Vendas do mês) e a navegação por abas: Painel, Pedidos, Produtos e Minha loja. A aba selecionada é exibida pela rota filha (`RouterView`).

**Componentes principais.** `IconeSvg`, store `produtor` (concentra loja, produtos, pedidos, categorias e indicadores).

**Estados e regras.**

- Carregando (espaços reservados), erro (mensagem da API ou "Não foi possível carregar a área do produtor." com "Tentar novamente").
- Sem loja (`GET /lojas/me/` responde 404): cartão "Você ainda não possui uma loja" com "Criar minha loja"; as abas não são exibidas. Também é este o destino quando o produtor sem loja tenta abrir uma aba que exige loja.
- Ao entrar na área, os dados são sempre recarregados; trocar de aba reaproveita o que já foi carregado.
- Os indicadores são calculados no navegador, só para acompanhamento, considerando pedidos não cancelados (regra "Indicadores da área do produtor").

**Endpoints.**

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| GET | `/lojas/me/` | ao entrar na área, em "Tentar novamente" e em "Atualizar pedidos" (ambos chamam `carregar({ forcar: true })`, que repete as cinco chamadas) | `api.lojas.me` / `useProdutorStore().carregar` |
| GET | `/produtos/meus/` | logo após a loja, em paralelo com os três seguintes | `api.produtos.listarMeus` / `carregar` |
| GET | `/pedidos/minha-loja/` | idem | `api.pedidos.listarMinhaLoja` / `carregar` |
| GET | `/pedidos/status-disponiveis/` | idem (monta o mapa nome do status para id) | `api.pedidos.listarStatusDisponiveis` / `carregar` |
| GET | `/produtos/categorias/?ativo=true` | idem (alimenta o formulário de produto) | `api.categorias.listar` / `carregar` |

(O guard consulta `GET /usuarios/me/` a cada navegação para a área; ver seção 2.1.)

#### 4.3.3 Painel (`PainelProdutor`)

- Rota: `/minha-loja`
- Acesso: produtor (com ou sem loja; sem loja a moldura mostra o convite para criar)

![Figura 20 - Painel do produtor](telas/tela-20-painel-produtor.png)

Figura 20 - Painel do produtor

**Para que serve.** Resumo comercial da loja: cartões "Vendas do mês", "Pedidos no mês" e "Ticket médio"; gráfico de barras "Vendas dos últimos 7 dias"; lista "Produtos mais vendidos"
(cinco primeiros, por quantidade, com o total em reais; produto excluído aparece como "(produto removido)", RN-019). A nota final informa que os indicadores usam os pedidos não cancelados e servem apenas
para acompanhamento.

**Componentes principais.** `GraficoBarras`, store `produtor`.

**Estados e regras.**

- Sem vendas: "Nenhuma venda registrada nos últimos 7 dias." e "Os produtos aparecerão aqui assim que a loja receber pedidos.".
- Os valores somam o `valor_liquido` dos pedidos não cancelados e são agrupados pela data de criação; a validação e os relatórios oficiais continuam no backend.
- A tela não faz chamadas próprias: usa os dados já carregados pela Área do produtor (principalmente `GET /pedidos/minha-loja/`).

**Endpoints.** Nenhum próprio (dados da store `produtor`, carregados conforme a seção 4.3.2).

#### 4.3.4 Pedidos em Kanban (`PedidosKanban`)

- Rota: `/minha-loja/pedidos` (`/loja/pedidos` redireciona para cá)
- Acesso: produtor com loja

![Figura 21 - Pedidos em Kanban](telas/tela-21-pedidos-kanban.png)

Figura 21 - Pedidos em Kanban

![Figura 22 - Cancelar pedido no Kanban](telas/tela-22-pedidos-kanban-cancelar.png)

Figura 22 - Cancelar pedido no Kanban

**Para que serve.** Quadro com uma coluna por status — Pendente, Em preparo, Pronto para retirada e Entregue — e uma seção recolhível "Cancelados (N)". Cada cartão mostra número, data, nome do cliente,
telefone do cliente (link `tel:`, quando a API o envia), itens, total e as ações permitidas:

| Status | Ação de avanço | Cancelar |
| --- | --- | --- |
| Pendente | "Iniciar preparo" (para Em preparo) | sim |
| Em preparo | "Marcar como pronto" (para Pronto para retirada) | sim |
| Pronto para retirada | "Confirmar entrega" (para Entregue) | não |
| Entregue, Cancelado | nenhuma | não |

O cancelamento abre o modal "Cancelar pedido" (os produtos voltam ao estoque; a ação não pode ser desfeita), com "Cancelar pedido" e "Manter pedido". O botão "Atualizar pedidos" recarrega os dados da área.

**Componentes principais.** `CartaoPedidoKanban`, `SeloStatus`, `ModalConfirmacao`, store `produtor`, `utils/statusPedido.js`.

**Estados e regras.**

- Coluna sem pedidos: "Nenhum pedido nesta etapa."; botões ficam desabilitados e com spinner enquanto a mudança está em andamento.
- Sucesso: notificação "Pedido #N movido para <status>." ou "Pedido #N cancelado." (4 s); falha: notificação `danger` com a mensagem da API.
- O frontend traduz o nome do status no id obtido de `status-disponiveis` e só oferece o passo seguinte do fluxo (sem retorno de status); o backend valida as transições.
- Após cancelar, a lista de produtos é recarregada porque o estoque foi restaurado.
- Regras citadas: fluxo de status (Pendente, Em preparo, Pronto para retirada, Entregue; cancelamento a partir de Pendente e Em preparo), RN-021 (o telefone só vem nos pedidos em aberto),
  RN-022 (o produtor pode marcar Entregue), RN-019 (nome do cliente do snapshot).

**Endpoints.**

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| GET | `/pedidos/minha-loja/` | carga da área e "Atualizar pedidos" | `api.pedidos.listarMinhaLoja` / `useProdutorStore().carregar` |
| GET | `/pedidos/status-disponiveis/` | idem | `api.pedidos.listarStatusDisponiveis` / `useProdutorStore().carregar` |
| PATCH | `/pedidos/{id}/status/` | ao avançar ou cancelar um pedido (corpo `{ "status": <id> }`) | `api.pedidos.atualizarStatus` / `useProdutorStore().atualizarStatus` |
| GET | `/produtos/meus/` | em "Atualizar pedidos" (junto com `GET /lojas/me/` e `GET /produtos/categorias/?ativo=true`, que também são repetidos) e após cancelar um pedido | `api.produtos.listarMeus` / `carregar`; `recarregarProdutos` (via `atualizarStatus`) |

#### 4.3.5 Produtos da loja (`ProdutosLoja` + `FormularioProduto`)

- Rota: `/minha-loja/produtos` (`/loja/produtos` redireciona para cá; `?novo=1` abre o formulário de novo produto)
- Acesso: produtor com loja

![Figura 23 - Produtos da loja](telas/tela-23-produtos-loja.png)

Figura 23 - Produtos da loja

![Figura 24 - Formulário de novo produto](telas/tela-24-produto-formulario-novo.png)

Figura 24 - Formulário de novo produto

![Figura 25 - Formulário de edição de produto](telas/tela-25-produto-formulario-edicao.png)

Figura 25 - Formulário de edição de produto

![Figura 26 - Editor de enquadramento da imagem](telas/tela-26-produto-editor-enquadramento.png)

Figura 26 - Editor de enquadramento da imagem

**Para que serve.** Gestão dos produtos da loja. A tabela (ordenada por nome) mostra miniatura, nome, SKU, categoria, estoque, preço bruto, desconto, preço líquido, status (Ativo/Inativo) e as ações "Editar" e "Desativar/Reativar".
Há filtros Todos, Ativos e Inativos (com contagem) e um aviso de estoque quando há produtos ativos com estoque baixo ou sem estoque.

O formulário lateral (offcanvas "Novo produto"/"Editar produto") tem:

- Nome, categoria (somente categorias ativas), estoque e descrição;
- Imagens: até 5, JPG, PNG ou WEBP de até 5 MB; cada miniatura permite remover, mover para a esquerda ou direita, definir como principal e ajustar o enquadramento;
- Preço: preço de venda e desconto em %, com a prévia "Preço final ao cliente"; na edição, o campo é "Novo preço de venda" e, em branco, mantém o preço atual;
- Na edição, a caixa "Produto disponível para compra" (ativo).

O editor de enquadramento (`EditorEnquadramento`, dentro do próprio painel) recorta a imagem em quadrado no navegador, com arraste, setas do teclado, zoom e "Centralizar"; a imagem recortada (WEBP ou JPEG, até 1200 px)
é a que será enviada.

**Componentes principais.** `FormularioProduto`, `EditorEnquadramento`, `ModalConfirmacao` ("Desativar produto"), `SeloStatus`, store `produtor`, `utils/imagem.js`.

**Estados e regras.**

- Vazio: "Nenhum produto cadastrado" com "Cadastrar produto"; filtro sem resultado com "Ver todos". Produto sem preço mostra "Sem preço".
- Estoque (RN-017): produto com estoque 0 mostra "Sem estoque" e "Fora do catálogo"; estoque de 1 a 5 mostra "Estoque baixo" (indicador visual, vindo de `estoque_baixo`).
- Desativar abre modal ("deixará de aparecer no catálogo e não poderá ser comprado"; pedidos preservados); reativar é direto. Produtos não são excluídos.
- Validação local do formulário: nome, categoria e estoque inteiro maior ou igual a zero obrigatórios; preço obrigatório no cadastro e maior que zero; desconto entre 0 e 100. Produto com categoria hoje inativa a exibe desabilitada.
- Imagens (RN-016): a primeira vira principal; excedentes além de 5 são recusados com mensagem; o backend valida formato, tamanho e quantidade.
- O SKU é gerado pelo backend e só é exibido. Cada alteração de preço cria um novo preço vigente (o histórico é preservado).
- Salvamento (`produtorStore.salvarProduto`), nesta ordem: (1) cria (`POST /produtos/`) ou edita (`PATCH /produtos/{id}/`); (2) cria o preço (`POST /produtos/precos/`) — sempre no cadastro; na edição, somente se o produtor informou
  novo preço ou mudou o desconto; (3) sincroniza as imagens: remove as marcadas, envia as novas (a principal já no envio), define a principal entre as já salvas e reordena quando a ordem difere; (4) recarrega `GET /produtos/meus/`.
  Falhas nas imagens não desfazem o produto: aparece notificação `warning` ("Produto cadastrado. Nem todas as imagens foram salvas: ..." ou "Produto atualizado. Nem todas as imagens foram salvas: ...", 8 s). Falha nos passos 1 ou 2 aparece no formulário. Sucesso: "Produto cadastrado." ou "Produto atualizado." (4 s).
  Imagem já salva que foi ajustada é substituída ao salvar (a antiga é removida e a recortada é enviada).

**Endpoints.**

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| GET | `/produtos/meus/` | carga da área e após salvar produto | `api.produtos.listarMeus` / `useProdutorStore().carregar`, `recarregarProdutos` |
| GET | `/produtos/categorias/?ativo=true` | carga da área (opções do formulário) | `api.categorias.listar` / `useProdutorStore().carregar` |
| POST | `/produtos/` | ao salvar um produto novo | `api.produtos.criar` / `useProdutorStore().salvarProduto` |
| PATCH | `/produtos/{id}/` | ao salvar edição e em Desativar/Reativar (`{ "ativo": ... }`) | `api.produtos.atualizar` / `salvarProduto`, `alternarAtivo` |
| POST | `/produtos/precos/` | ao salvar, conforme descrito acima | `api.produtos.criarPreco` / `salvarProduto` |
| POST | `/produtos/{id}/imagens/` | para cada imagem nova (multipart; `e_principal` na escolhida) | `api.produtos.enviarImagem` / `salvarProduto` |
| PATCH | `/produtos/{id}/imagens/{imagem_id}/` | ao mudar a principal entre imagens já salvas | `api.produtos.definirImagemPrincipal` / `salvarProduto` |
| DELETE | `/produtos/{id}/imagens/{imagem_id}/` | para cada imagem removida | `api.produtos.removerImagem` / `salvarProduto` |
| POST | `/produtos/{id}/imagens/reordenar/` | quando a ordem final difere da atual | `api.produtos.reordenarImagens` / `salvarProduto` |

(Para ajustar uma imagem já salva, o `FormularioProduto` a baixa diretamente da URL de mídia, com `fetch` (`carregarImagemParaEdicao`), e a entrega ao editor de enquadramento; isso não é um endpoint da API.)

#### 4.3.6 Dados da loja (`DadosLoja`)

- Rota: `/minha-loja/loja`
- Acesso: produtor com loja

![Figura 27 - Dados da loja](telas/tela-27-dados-loja.png)

Figura 27 - Dados da loja

**Para que serve.** Edição da loja do produtor, em quatro blocos:

- **Dados da loja**: nome (obrigatório), descrição e CNPJ (somente leitura, "não pode ser alterado por aqui"); botões "Descartar alterações" e "Salvar alterações" (habilitados somente quando há mudança).
- **Imagem da loja**: escolher/trocar, "Salvar imagem", "Cancelar" e "Remover imagem" (modal "Remover imagem da loja?"); sem imagem, mostra a inicial do nome (RN-018).
- **Vitrine pública**: botão "Ver minha vitrine", que leva a `/loja/:id` (hoje o espaço "Em breve", seção 4.2.3).
- **Status da loja**: selo Ativa/Inativa e botão "Desativar loja" (modal "Desativar loja?"). Com a loja inativa, a tela informa que ela não aceita novas compras; a tela não oferece reativação.

**Componentes principais.** `SeletorImagemUnica`, `AvatarImagem`, `ModalConfirmacao`, store `produtor`.

**Estados e regras.**

- Carregando ("Salvando..."), erros por campo (nome, descrição) e erro geral; falha de imagem mostra a mensagem de RN-018, e a imagem recusada sai da prévia.
- Sucesso: notificações "Dados da loja atualizados.", "Imagem da loja atualizada.", "Imagem da loja removida." e, na desativação, `warning` "Loja desativada. Produtos e pedidos foram preservados.".
- Regras citadas: RN-013 (CNPJ e proprietário não são alterados nesta área), RN-018 (imagem única; loja inativa continua editável), desativação que preserva o histórico e impede novas compras.
- Os dados da loja vêm da store `produtor`, carregada pela Área do produtor.

**Endpoints.**

| Método | URL | Quando é chamado | Função do service / store |
| --- | --- | --- | --- |
| PATCH | `/lojas/me/` (JSON) | em "Salvar alterações" (`nome`, `descricao`) e em "Desativar loja" (`{ "ativa": false }`) | `api.lojas.atualizarMinha` / `useProdutorStore().salvarLoja` |
| PATCH | `/lojas/me/` (multipart, campo `imagem_perfil`) | em "Salvar imagem" | `api.lojas.atualizarImagem` / `useProdutorStore().salvarImagemLoja` |
| DELETE | `/lojas/me/imagem/` | ao confirmar "Remover imagem da loja?" (404 é tratado como já removida) | `api.lojas.removerImagem` / `useProdutorStore().removerImagemLoja` |

---

## 5. Matriz Tela x Endpoint

### 5.1 Endpoints usados pelo frontend

O frontend usa **45** combinações método + URL (44 chamadas feitas pelas telas e stores e o refresh de token, feito internamente por `request()`).
As variações JSON e multipart de `PATCH /usuarios/me/` e de `PATCH /lojas/me/` contam uma vez cada.

| # | Método | URL | Telas / elementos que consomem | Função do service |
| --- | --- | --- | --- | --- |
| 1 | POST | `/usuarios/login/` | Login | `api.auth.login` |
| 2 | POST | `/usuarios/cadastro/` | Cadastro | `api.auth.cadastrar` |
| 3 | POST | `/usuarios/token/refresh/` | todas as telas com chamadas à API, ao receber 401 (interno de `request()`) | função interna `refreshAccessToken` |
| 4 | POST | `/usuarios/redefinir-senha/` | Esqueci a senha | `api.auth.solicitarRedefinicaoSenha` |
| 5 | POST | `/usuarios/redefinir-senha/confirmar/` | Redefinir senha | `api.auth.confirmarRedefinicaoSenha` |
| 6 | GET | `/usuarios/me/` | Cabeçalho, guard de rotas do produtor, Perfil | `api.usuarios.me` |
| 7 | PATCH | `/usuarios/me/` | Perfil (dados pessoais e foto) | `api.usuarios.atualizar`, `api.usuarios.atualizarFoto` |
| 8 | DELETE | `/usuarios/me/foto/` | Perfil | `api.usuarios.removerFoto` |
| 9 | GET | `/tipos-telefone/` | Login (aba Criar conta), Perfil | `api.tiposTelefone.listar` |
| 9a | GET | `/generos/` | Login (aba Criar conta), Perfil | `api.generos.listar` |
| 10 | GET | `/usuarios/me/telefones/` | Perfil | `api.telefones.listar` |
| 11 | POST | `/usuarios/me/telefones/` | Perfil | `api.telefones.criar` |
| 12 | PATCH | `/usuarios/me/telefones/{id}/` | Perfil | `api.telefones.atualizar` |
| 13 | DELETE | `/usuarios/me/telefones/{id}/` | Perfil | `api.telefones.excluir` |
| 14 | POST | `/lojas/lojas/` | Criar loja | `api.lojas.criar` |
| 15 | GET | `/lojas/lojas/{id}/` | Detalhe do produto (imagem da loja) | `api.lojas.obter` |
| 16 | GET | `/lojas/me/` | Área do produtor (e abas), Perfil | `api.lojas.me` |
| 17 | PATCH | `/lojas/me/` | Dados da loja (dados, imagem, desativação) | `api.lojas.atualizarMinha`, `api.lojas.atualizarImagem` |
| 18 | DELETE | `/lojas/me/imagem/` | Dados da loja | `api.lojas.removerImagem` |
| 19 | GET | `/produtos/` | Catálogo | `api.produtos.listar` |
| 20 | GET | `/produtos/{id}/` | Detalhe do produto | `api.produtos.obter` |
| 21 | GET | `/produtos/meus/` | Área do produtor, Produtos da loja, Pedidos em Kanban ("Atualizar pedidos" e após cancelar) | `api.produtos.listarMeus` |
| 22 | POST | `/produtos/` | Produtos da loja (formulário) | `api.produtos.criar` |
| 23 | PATCH | `/produtos/{id}/` | Produtos da loja (edição, Desativar/Reativar) | `api.produtos.atualizar` |
| 24 | GET | `/produtos/categorias/?ativo=true` | Catálogo, Área do produtor (formulário de produto) | `api.categorias.listar` |
| 25 | POST | `/produtos/precos/` | Produtos da loja (formulário) | `api.produtos.criarPreco` |
| 26 | POST | `/produtos/{id}/imagens/` | Produtos da loja (formulário) | `api.produtos.enviarImagem` |
| 27 | PATCH | `/produtos/{id}/imagens/{imagem_id}/` | Produtos da loja (formulário) | `api.produtos.definirImagemPrincipal` |
| 28 | DELETE | `/produtos/{id}/imagens/{imagem_id}/` | Produtos da loja (formulário) | `api.produtos.removerImagem` |
| 29 | POST | `/produtos/{id}/imagens/reordenar/` | Produtos da loja (formulário) | `api.produtos.reordenarImagens` |
| 30 | GET | `/carrinhos/` | Cabeçalho, Carrinho, Detalhe do produto (após adicionar) | `api.carrinhos.listar` |
| 31 | POST | `/carrinhos/` | Detalhe do produto | `api.carrinhos.adicionar` |
| 32 | PATCH | `/carrinhos/itens/{item_id}/` | Carrinho | `api.carrinhos.atualizarItem` |
| 33 | DELETE | `/carrinhos/itens/{item_id}/` | Carrinho | `api.carrinhos.removerItem` |
| 34 | GET | `/favoritos/` | Cabeçalho, Favoritos | `api.favoritos.listar` |
| 35 | POST | `/favoritos/` | Catálogo, Detalhe do produto | `api.favoritos.adicionar` |
| 36 | DELETE | `/favoritos/{favorito_id}/` | Catálogo, Detalhe do produto, Favoritos | `api.favoritos.remover` |
| 37 | GET | `/pedidos/` | Meus pedidos | `api.pedidos.listar` |
| 38 | POST | `/pedidos/` | Carrinho (finalizar) | `api.pedidos.finalizarCarrinho` |
| 39 | GET | `/pedidos/minha-loja/` | Área do produtor, Pedidos em Kanban, Painel (dados) | `api.pedidos.listarMinhaLoja` |
| 40 | GET | `/pedidos/status-disponiveis/` | Área do produtor, Pedidos em Kanban | `api.pedidos.listarStatusDisponiveis` |
| 41 | PATCH | `/pedidos/{id}/status/` | Pedidos em Kanban | `api.pedidos.atualizarStatus` |
| 42 | PATCH | `/pedidos/{id}/cancelar/` | Meus pedidos | `api.pedidos.cancelar` |
| 43 | PATCH | `/pedidos/{id}/confirmar-entrega/` | Meus pedidos | `api.pedidos.confirmarEntrega` |
| 44 | GET | `/avaliacoes/?produto={id}` | Detalhe do produto | `api.avaliacoes.listarPorProduto` |
| 45 | POST | `/avaliacoes/` | Meus pedidos (modal de avaliação) | `api.avaliacoes.criar` |

Telas sem chamada própria: Loja pública (`LojaView`, espaço reservado) e Painel (`PainelProdutor`, usa a store já carregada).

### 5.2 Endpoints do `api-endpoints.md` que nenhuma tela usa

São 15 combinações das 60 documentadas:

- `POST /api/token/refresh/` (rota raiz de refresh; o frontend usa `/usuarios/token/refresh/`);
- `GET /usuarios/me/telefones/{id}/`;
- `GET /lojas/lojas/` (listagem de lojas);
- `GET /produtos/categorias/{id}/`;
- `POST /produtos/categorias/` (sugestão ou criação de categoria);
- `PATCH /produtos/categorias/{id}/`;
- `GET /produtos/precos/`;
- `GET /produtos/precos/{id}/`;
- `GET /produtos/{produto_id}/imagens/` (as imagens vêm no campo `imagens` do produto);
- `GET /produtos/{produto_id}/imagens/{id}/`;
- `GET /carrinhos/{id}/`;
- `GET /pedidos/{id}/`;
- `PATCH /pedidos/{id}/` (responde sempre 405);
- `GET /favoritos/{id}/`;
- `GET /avaliacoes/{id}/`.

Também há uma função do service sem uso: `api.auth.refresh` (o refresh efetivo é feito por `refreshAccessToken`, interno a `services/api.js`).

---

## 6. Lista de prints a capturar

Os arquivos devem ser salvos em `docs/telas/`. Recomenda-se usar dados fictícios (CPF, e-mail e telefones de exemplo) e a janela em tamanho de desktop, exceto onde indicado.

- [ ] `tela-01-login.png` — aba "Entrar" da tela `/login`, com o painel lateral visível.
- [ ] `tela-02-cadastro.png` — aba "Criar conta" preenchida com dados fictícios, incluindo tipo e número de telefone.
- [ ] `tela-03-esqueci-senha.png` — `/esqueci-senha` com o campo de e-mail.
- [ ] `tela-04-esqueci-senha-enviado.png` — `/esqueci-senha` após o envio, com a mensagem neutra e "Usar outro e-mail".
- [ ] `tela-05-redefinir-senha.png` — `/redefinir-senha` aberta pelo link do e-mail, com os dois campos de senha.
- [ ] `tela-06-catalogo.png` — `/` com banner, filtros de categoria, ordenação e cartões de produto (um com desconto).
- [ ] `tela-07-detalhe-produto.png` — `/produto/:id` com galeria, preço, quantidade e botões, logado.
- [ ] `tela-08-detalhe-produto-avaliacoes.png` — seção "Avaliações" do detalhe de um produto com avaliações.
- [ ] `tela-09-loja-publica.png` — `/loja/:id` com o cartão "Em breve".
- [ ] `tela-10-carrinho.png` — `/carrinho` com itens de duas lojas, resumo e botão "Finalizar pedido".
- [ ] `tela-11-favoritos.png` — `/favoritos` com ao menos um produto favoritado.
- [ ] `tela-12-pedidos.png` — `/pedidos` com filtros de status e pedidos em status variados (Pendente, Pronto para retirada, Entregue).
- [ ] `tela-13-pedidos-avaliar.png` — modal "Avaliar produto" aberto, com nota e comentário.
- [ ] `tela-14-pedidos-cancelar.png` — modal "Cancelar pedido" aberto.
- [ ] `tela-15-pedidos-confirmar-recebimento.png` — modal "Confirmar recebimento" aberto.
- [ ] `tela-16-perfil.png` — `/perfil` com foto, informações pessoais e bloco da loja.
- [ ] `tela-17-perfil-telefones.png` — bloco "Telefones" com telefone principal, outro telefone e o formulário de adicionar aberto.
- [ ] `tela-18-criar-loja.png` — `/criar-loja` com o formulário e o seletor de imagem.
- [ ] `tela-19-area-produtor-sem-loja.png` — `/minha-loja` de um produtor sem loja, com o cartão "Você ainda não possui uma loja".
- [ ] `tela-20-painel-produtor.png` — `/minha-loja` com indicadores, abas, cartões do mês, gráfico dos 7 dias e produtos mais vendidos.
- [ ] `tela-21-pedidos-kanban.png` — `/minha-loja/pedidos` com cartões nas quatro colunas e a seção "Cancelados".
- [ ] `tela-22-pedidos-kanban-cancelar.png` — modal "Cancelar pedido" aberto no quadro do produtor.
- [ ] `tela-23-produtos-loja.png` — `/minha-loja/produtos` com a tabela (incluir um produto com "Estoque baixo" e um inativo).
- [ ] `tela-24-produto-formulario-novo.png` — formulário lateral "Novo produto" com imagens e preço preenchidos.
- [ ] `tela-25-produto-formulario-edicao.png` — formulário lateral "Editar produto" com a caixa "Produto disponível para compra".
- [ ] `tela-26-produto-editor-enquadramento.png` — editor de enquadramento aberto dentro do formulário ("Ajustar imagem").
- [ ] `tela-27-dados-loja.png` — `/minha-loja/loja` com dados, imagem da loja, vitrine e status.
