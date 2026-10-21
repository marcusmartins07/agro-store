# API do Agro Store — referência de endpoints

Documento derivado do código do backend (`apps/backend/agrostore/`). Descreve os endpoints existentes, os métodos HTTP
realmente habilitados em cada um, o funcionamento, exemplos de payload e de resposta e os erros possíveis.
Os dados dos exemplos são fictícios e ambientados na Feira do Produtor Rural Willi Dummer (Camaquã/RS).

## 1. Introdução

### 1.1 Convenções gerais

- URL base em desenvolvimento: `http://localhost:8000`.
- URL base em produção: `<URL do backend>` (backend publicado no Render; a URL real não é registrada neste documento). O frontend, publicado na Vercel (`<domínio da Vercel>`), consome a API pela variável `VITE_API_URL`, e o backend só aceita chamadas das origens listadas em `CORS_ALLOWED_ORIGINS`. Banco PostgreSQL e armazenamento de imagens ficam no Supabase.
- Formato: JSON (`Content-Type: application/json`). Uploads de imagem usam `multipart/form-data`.
- Não há paginação configurada (`REST_FRAMEWORK` não define classe de paginação): toda listagem devolve um array JSON simples.
- Datas/horas saem em ISO 8601 UTC (ex.: `"2026-10-20T14:32:10.512345Z"`); datas simples em `AAAA-MM-DD`.
- CPF, CNPJ, SKU, código de barras e telefones são sempre texto (somente dígitos no caso de CPF e telefone).
- Arquivos de mídia (imagens) são servidos em `/media/...` apenas com `DEBUG` ativo (ou pelo Supabase Storage quando
  `SUPABASE_STORAGE_BUCKET` está definido). As URLs de imagem devolvidas pela API são absolutas.
- Rotas fora da API REST: `admin/` (Django Admin) e `/media/` (arquivos, somente em `DEBUG`). Não são documentadas aqui.
- Os `ViewSet`s com `DefaultRouter` também expõem uma "raiz da API" do roteador (ex.: `/api/v1/lojas/`); ela não faz parte do contrato e não é documentada.
  O `DefaultRouter` também aceita sufixos de formato (ex.: `/api/v1/produtos/1.json`), igualmente fora do contrato.

### 1.2 Autenticação (JWT)

A autenticação padrão é `JWTAuthentication` (djangorestframework-simplejwt) e a permissão padrão é `IsAuthenticated`.

Fluxo:

1. `POST /api/v1/usuarios/login/` (ou `cadastro/`) devolve `access` e `refresh`.
2. Enviar o `access` em todas as requisições protegidas: `Authorization: Bearer <access>`.
3. O `access` vale **120 minutos**; o `refresh` vale **1 dia** (`SIMPLE_JWT`). Rotação de refresh não está configurada (a resposta do refresh traz só `access`).
4. Com `access` expirado (resposta 401), chamar `POST /api/v1/usuarios/token/refresh/` com o `refresh` e repetir a requisição.

Observação: nos endpoints públicos que usam a autenticação padrão (ex.: `GET /api/v1/produtos/`), um header `Authorization` com token
inválido ou expirado resulta em 401 em vez de ser ignorado. Por isso o frontend não envia o token em alguns endpoints públicos.
Nos endpoints com `authentication_classes = []` (tipos de telefone e redefinição de senha) o header é ignorado.

Papéis usados neste documento:

| Termo | Significado no código |
| --- | --- |
| Público | `AllowAny` |
| Autenticado | `IsAuthenticated` (qualquer usuário logado, inclusive produtor) |
| Produtor | usuário autenticado com `is_produtor = true` |
| Administrador | usuário autenticado com `is_staff = true` |

### 1.3 Erros

Os textos abaixo seguem o idioma `pt-br` configurado (`LANGUAGE_CODE`); mensagens padrão do DRF/simplejwt são indicativas
(o texto exato depende da tradução instalada). As mensagens escritas no código do projeto são citadas literalmente.

| Status | Quando | Corpo típico |
| --- | --- | --- |
| 400 | validação de campos | `{"campo": ["mensagem"]}` ou `{"non_field_errors": ["mensagem"]}` |
| 400 | regra recusada por view/serviço | `{"detail": "mensagem"}` |
| 401 | sem token, token inválido ou expirado | `{"detail": "As credenciais de autenticação não foram fornecidas."}` ou `{"detail": "...", "code": "token_not_valid", "messages": [...]}` |
| 403 | autenticado sem permissão | `{"detail": "Você não tem permissão para executar essa ação."}` ou mensagem própria do código |
| 404 | recurso inexistente ou fora do escopo do usuário | `{"detail": "Não encontrado."}` |
| 405 | método não habilitado na rota | `{"detail": "Método \"PUT\" não permitido."}` |
| 429 | limite de requisições (redefinição de senha) | `{"detail": "Muitas solicitações. Tente novamente mais tarde."}` + header `Retry-After` |

Notas sobre o formato dos erros (comportamento real do código):

- Erros levantados dentro de `validate_<campo>`/`validate` de serializers vêm como lista de mensagens por campo.
- `ValidationError({'campo': 'texto'})` levantado **fora** de um serializer (em view, `get_queryset` ou `perform_*`) sai com o valor como **string**, não lista
  (ex.: `{"imagens": "Envie a lista com todas..."}`). Dentro de `validate()`/`validate_<campo>()` o DRF sempre converte para lista.
  A redefinição de senha (`validar_nova_senha`, chamada pela view) é um caso de string.
- `ValidationError('texto')` sem campo, levantado em `perform_create`, resulta em um **array** como corpo (ex.: `["Produto já está nos favoritos."]`).
- Recursos de outro usuário respondem 404 (não 403) na maioria dos endpoints, para não revelar a existência.

### 1.4 Formato de valores monetários nas respostas

- Campos `DecimalField` de serializers (ex.: `valor_bruto` do pedido e do carrinho, `preco_venda`) saem como **string** (`"12.50"`).
- Campos calculados (`ReadOnlyField`/`SerializerMethodField`: `preco`, `preco_original` do produto; `valor_unitario`, `valor_desconto`, `subtotal` do item do carrinho)
  saem como **número JSON** (`26.1`, `29.0`), porque o encoder do DRF converte `Decimal` em `float` nesses casos.
- Nos payloads de envio, valores monetários podem ser enviados como string (`"29.00"`) ou número.

### 1.5 Regras de negócio citadas

Referência: skill `agro-regras-de-negocio` (RN-008 retirada; RN-010 avaliações; RN-011 pedidos por loja; RN-013 uma loja por produtor;
RN-016 imagens de produto; RN-017 estoque e carrinho; RN-018 imagem da loja e foto de perfil; RN-019 preservação do histórico e snapshot;
RN-020 redefinição de senha; RN-021 telefones; RN-022 confirmação de recebimento).

## 2. Tabela-resumo

Prefixo canônico das rotas de usuário: `/api/v1/usuarios/` (o mesmo conjunto também responde em `/api/`; ver seção 3.1).

| Método | URL | Autenticação / permissão | Descrição curta |
| --- | --- | --- | --- |
| POST | `/api/v1/usuarios/cadastro/` | Público | Cadastra cliente e devolve tokens |
| POST | `/api/v1/usuarios/login/` | Público | Login por CPF e senha |
| POST | `/api/v1/usuarios/token/refresh/` | Público | Renova o `access` |
| POST | `/api/token/refresh/` | Público | Renova o `access` (rota raiz) |
| GET | `/api/v1/usuarios/me/` | Autenticado | Perfil do usuário logado |
| PATCH | `/api/v1/usuarios/me/` | Autenticado | Atualiza perfil e foto |
| DELETE | `/api/v1/usuarios/me/foto/` | Autenticado | Remove a foto de perfil |
| POST | `/api/v1/usuarios/redefinir-senha/` | Público (limite 5/hora) | Solicita link de redefinição |
| POST | `/api/v1/usuarios/redefinir-senha/confirmar/` | Público (limite 10/hora) | Define nova senha com o token |
| GET | `/api/v1/usuarios/me/telefones/` | Autenticado | Lista telefones do usuário |
| POST | `/api/v1/usuarios/me/telefones/` | Autenticado | Adiciona telefone |
| GET | `/api/v1/usuarios/me/telefones/{id}/` | Autenticado (dono) | Detalha telefone |
| PATCH | `/api/v1/usuarios/me/telefones/{id}/` | Autenticado (dono) | Edita telefone / define principal |
| DELETE | `/api/v1/usuarios/me/telefones/{id}/` | Autenticado (dono) | Exclui telefone |
| GET | `/api/v1/tipos-telefone/` | Público | Lista tipos de telefone |
| GET | `/api/v1/lojas/lojas/` | Público | Lista lojas |
| POST | `/api/v1/lojas/lojas/` | Produtor | Cria a loja do produtor |
| GET | `/api/v1/lojas/lojas/{id}/` | Público | Detalha loja |
| GET | `/api/v1/lojas/me/` | Autenticado | Loja do usuário logado |
| PATCH | `/api/v1/lojas/me/` | Autenticado (dono da loja) | Edita nome, descrição, status e imagem |
| DELETE | `/api/v1/lojas/me/imagem/` | Autenticado (dono da loja) | Remove a imagem da loja |
| GET | `/api/v1/produtos/` | Público | Catálogo (ativos, loja ativa, estoque > 0) |
| POST | `/api/v1/produtos/` | Produtor com loja (ou administrador com loja) | Cadastra produto |
| GET | `/api/v1/produtos/{id}/` | Público | Detalha produto ativo de loja ativa |
| PATCH | `/api/v1/produtos/{id}/` | Autenticado (dono) ou administrador | Edita produto |
| GET | `/api/v1/produtos/meus/` | Produtor ou administrador | Produtos da própria loja |
| GET | `/api/v1/produtos/categorias/` | Público | Lista categorias |
| POST | `/api/v1/produtos/categorias/` | Produtor (nasce inativa) ou administrador | Sugere/cria categoria |
| GET | `/api/v1/produtos/categorias/{id}/` | Público | Detalha categoria |
| PATCH | `/api/v1/produtos/categorias/{id}/` | Administrador | Renomeia, ativa ou inativa categoria |
| GET | `/api/v1/produtos/precos/` | Autenticado (escopo próprio) | Lista preços dos produtos da própria loja |
| POST | `/api/v1/produtos/precos/` | Dono do produto ou administrador | Cria novo preço vigente |
| GET | `/api/v1/produtos/precos/{id}/` | Autenticado (escopo próprio) | Detalha preço |
| GET | `/api/v1/produtos/{produto_id}/imagens/` | Público (produto visível) | Lista imagens do produto |
| POST | `/api/v1/produtos/{produto_id}/imagens/` | Dono do produto ou administrador | Envia imagem |
| GET | `/api/v1/produtos/{produto_id}/imagens/{id}/` | Público (produto visível) | Detalha imagem |
| PATCH | `/api/v1/produtos/{produto_id}/imagens/{id}/` | Dono do produto ou administrador | Define imagem principal |
| DELETE | `/api/v1/produtos/{produto_id}/imagens/{id}/` | Dono do produto ou administrador | Exclui imagem |
| POST | `/api/v1/produtos/{produto_id}/imagens/reordenar/` | Dono do produto ou administrador | Reordena imagens |
| GET | `/api/v1/carrinhos/` | Autenticado | Lista carrinhos do usuário (um por loja) |
| GET | `/api/v1/carrinhos/{id}/` | Autenticado (dono) | Detalha carrinho |
| POST | `/api/v1/carrinhos/` | Autenticado | Adiciona produto ao carrinho |
| PATCH | `/api/v1/carrinhos/itens/{item_id}/` | Autenticado (dono) | Altera quantidade do item |
| DELETE | `/api/v1/carrinhos/itens/{item_id}/` | Autenticado (dono) | Remove item do carrinho |
| GET | `/api/v1/pedidos/` | Autenticado | Pedidos feitos pelo usuário |
| GET | `/api/v1/pedidos/{id}/` | Autenticado (cliente do pedido) | Detalha pedido do usuário |
| POST | `/api/v1/pedidos/` | Autenticado | Finaliza itens do carrinho (um pedido por loja) |
| PATCH | `/api/v1/pedidos/{id}/` | Autenticado | Sempre 405 (usar `/status/`) |
| PATCH | `/api/v1/pedidos/{id}/status/` | Produtor da loja ou administrador | Atualiza status |
| PATCH | `/api/v1/pedidos/{id}/cancelar/` | Autenticado (cliente do pedido) | Cliente cancela pedido pendente |
| PATCH | `/api/v1/pedidos/{id}/confirmar-entrega/` | Autenticado (cliente do pedido) | Cliente confirma recebimento |
| GET | `/api/v1/pedidos/minha-loja/` | Produtor ou administrador | Pedidos recebidos pela loja |
| GET | `/api/v1/pedidos/status-disponiveis/` | Produtor ou administrador | Lista status de pedido |
| GET | `/api/v1/favoritos/` | Autenticado | Lista favoritos do usuário |
| POST | `/api/v1/favoritos/` | Autenticado | Favorita produto |
| GET | `/api/v1/favoritos/{id}/` | Autenticado (dono) | Detalha favorito |
| DELETE | `/api/v1/favoritos/{id}/` | Autenticado (dono) | Remove favorito |
| GET | `/api/v1/avaliacoes/` | Público | Lista avaliações (filtro `?produto=`) |
| POST | `/api/v1/avaliacoes/` | Autenticado (dono do pedido entregue) | Avalia item de pedido |
| GET | `/api/v1/avaliacoes/{id}/` | Autenticado | Detalha avaliação |

Total: 60 combinações método + URL documentadas (incluindo o `PATCH /pedidos/{id}/`, que responde sempre 405, e a rota raiz de refresh).

---

## 3. Autenticação e usuários

### 3.1 Prefixos duplicados (alias)

`agrostore/usuarios/urls.py` é montado duas vezes em `agrostore/urls.py`:

- `/api/` (ex.: `/api/login/`, `/api/me/`);
- `/api/v1/usuarios/` (ex.: `/api/v1/usuarios/login/`).

São as mesmas views nos dois prefixos. O frontend usa **`/api/v1/usuarios/`** (`API_BASE_URL` padrão `/api/v1` + `/usuarios/...`, em `apps/frontend/src/services/api.js`).
Este documento usa apenas o prefixo canônico. Além disso, `/api/token/refresh/` existe como rota própria na raiz.

### 3.2 Cadastro de cliente

- Método e URL: `POST /api/v1/usuarios/cadastro/`
- Autenticação: pública
- Para que serve: cria uma conta de **cliente** e já devolve os tokens para iniciar a sessão.

Como funciona:

- Cria apenas cliente; `is_produtor`, `is_staff` e permissões não são aceitos. Não cria loja.
- CPF: aceita com ou sem máscara (até 14 caracteres), é gravado só com dígitos, precisa ser válido e único.
- E-mail: único, sem diferenciar maiúsculas; gravado em minúsculas.
- Telefone (RN-021): um telefone e o seu tipo; o número é validado pela quantidade de dígitos do tipo (Celular 11, Fixo 10, Comercial 10 ou 11) e vira o telefone principal.
- Data de nascimento: idade mínima de 16 anos.
- Gênero: `M`, `F` ou `I` (precisa existir na tabela de gêneros).
- Senha: mínimo de 8 caracteres, validadores de senha do Django (similaridade com atributos, senhas comuns, apenas numérica) e confirmação igual.
- Tudo é criado em uma transação (usuário + telefone).

Payload:

```json
{
  "nome": "Marina Oliveira Duarte",
  "cpf": "529.982.247-25",
  "email": "marina.duarte@example.com",
  "telefone": "(53) 99123-4567",
  "tipo_telefone": 1,
  "data_nascimento": "1992-04-18",
  "genero": "F",
  "password": "SenhaForte#2026",
  "password_confirmacao": "SenhaForte#2026"
}
```

Resposta (201):

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "usuario": {
    "id": 7,
    "nome": "Marina Oliveira Duarte",
    "cpf": "52998224725",
    "email": "marina.duarte@example.com",
    "telefones": [
      { "id": 12, "numero": "53991234567", "tipo": 1, "tipo_descricao": "Celular", "e_principal": true }
    ],
    "data_nascimento": "1992-04-18",
    "genero": "F",
    "foto_perfil": null,
    "is_produtor": false,
    "tem_loja": false,
    "idade": 34
  }
}
```

Erros:

- 400 `{"cpf": ["Informe um CPF válido."]}` ou `["Já existe uma conta cadastrada com este CPF."]`
- 400 `{"email": ["Já existe uma conta cadastrada com este e-mail."]}`
- 400 `{"data_nascimento": ["É necessário ter pelo menos 16 anos para criar uma conta."]}`
- 400 `{"genero": ["Informe uma opção de gênero válida."]}` (ou `"A opção de gênero não está disponível."`)
- 400 `{"tipo_telefone": ["Informe um tipo de telefone válido."]}`
- 400 `{"telefone": ["Celular deve ter 11 dígitos com DDD."]}` (Fixo: `"Telefone fixo deve ter 10 dígitos com DDD."`; Comercial: `"Telefone comercial deve ter 10 ou 11 dígitos com DDD."`)
- 400 `{"password_confirmacao": ["As senhas não coincidem."]}` e `{"password": [ ...mensagens dos validadores... ]}` (no cadastro o erro é relançado dentro de `validate()` e sai como lista)
- 400 campos obrigatórios ausentes: `{"campo": ["Este campo é obrigatório."]}`

### 3.3 Login

- Método e URL: `POST /api/v1/usuarios/login/`
- Autenticação: pública
- Para que serve: autentica por CPF e senha e devolve tokens e perfil.
- Como funciona: o CPF é reduzido a dígitos; usuário inativo não autentica.

Payload:

```json
{ "cpf": "529.982.247-25", "password": "SenhaForte#2026" }
```

Resposta (200): mesmo corpo do cadastro (`refresh`, `access`, `usuario`).

Erros:

- 400 `{"non_field_errors": ["CPF ou senha inválidos."]}`
- 400 `{"cpf": ["Este campo é obrigatório."]}` / `{"password": ["Este campo é obrigatório."]}`

### 3.4 Renovar token

- Método e URL: `POST /api/v1/usuarios/token/refresh/` (também `POST /api/token/refresh/`)
- Autenticação: pública (`TokenRefreshView` do simplejwt)
- Para que serve: gera um novo `access` a partir do `refresh`.

Payload:

```json
{ "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." }
```

Resposta (200):

```json
{ "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." }
```

Erros:

- 400 `{"refresh": ["Este campo é obrigatório."]}`
- 401 `{"detail": "...", "code": "token_not_valid"}` (refresh inválido ou expirado)

### 3.5 Perfil do usuário logado

- Método e URL: `GET /api/v1/usuarios/me/`
- Autenticação: JWT (qualquer usuário)
- Para que serve: devolve os dados do perfil, com os telefones.

Resposta (200): o mesmo objeto `usuario` mostrado no cadastro. Campos: `id`, `nome`, `cpf`, `email`, `telefones[]`, `data_nascimento`, `genero` (`M`/`F`/`I`),
`foto_perfil` (URL absoluta ou `null`), `is_produtor`, `tem_loja`, `idade`. Todos somente leitura.

Erros: 401.

### 3.6 Atualizar perfil e foto

- Método e URL: `PATCH /api/v1/usuarios/me/`
- Autenticação: JWT (qualquer usuário)
- Para que serve: altera dados pessoais e envia/troca a foto de perfil (RN-018). Não existe `PUT` nem `POST` nesta rota.

Como funciona:

- Campos aceitos: `nome`, `email`, `data_nascimento`, `genero`, `foto_perfil`. Qualquer outro campo (CPF, `is_produtor`, `is_staff`, `telefones`...) faz a requisição inteira ser recusada com 400.
- Atualização parcial; validações iguais às do cadastro (e-mail único ignorando o próprio usuário, idade mínima de 16 anos, gênero `M`/`F`/`I`).
- Foto: JPG, PNG ou WEBP de até 5 MB, conferindo extensão e conteúdo; o arquivo é renomeado com nome aleatório. A nova foto substitui a anterior e o arquivo antigo é removido do storage após o commit.
- Enviar JSON para dados de texto; enviar `multipart/form-data` com o campo `foto_perfil` para a imagem.
- A remoção de foto é feita somente por `DELETE /me/foto/` (seção 3.7). Enviar `foto_perfil=''` em multipart resulta em 400 `{"foto_perfil": ["Envie uma imagem JPG, PNG ou WEBP válida."]}`.

Payload JSON:

```json
{ "nome": "Marina O. Duarte", "email": "marina.novo@example.com", "data_nascimento": "1992-04-18", "genero": "F" }
```

Payload multipart: campo `foto_perfil` = arquivo `.jpg`/`.png`/`.webp`.

Resposta (200): objeto de perfil completo (igual ao `GET /me/`), com `foto_perfil` preenchida, por exemplo
`"http://localhost:8000/media/usuarios/9b1deb4d3b7d4bad9bdd2b0d7b3dcb6d.jpg"`.

Erros:

- 400 `{"detail": "Somente nome, e-mail, data de nascimento, gênero e foto de perfil podem ser alterados no perfil. Os telefones são gerenciados em /me/telefones/."}`
- 400 `{"foto_perfil": ["Envie uma imagem JPG, PNG ou WEBP válida."]}` / `["A imagem deve ter no máximo 5 MB."]` (a foto atual é mantida)
- 400 `{"email": ["Já existe uma conta cadastrada com este e-mail."]}` e demais mensagens de validação do cadastro
- 401

### 3.7 Remover foto de perfil

- Método e URL: `DELETE /api/v1/usuarios/me/foto/`
- Autenticação: JWT (qualquer usuário)
- Para que serve: remove a foto de perfil sem enviar outra.
- Como funciona: limpa o campo e remove o arquivo do storage após o commit. Valores legados fora do padrão de nome gerado pelo sistema contam como "sem foto".

Resposta: 204 sem corpo.

Erros:

- 404 `{"detail": "Você não possui foto de perfil."}`
- 401

### 3.8 Solicitar redefinição de senha (RN-020)

- Método e URL: `POST /api/v1/usuarios/redefinir-senha/`
- Autenticação: pública (sem autenticação JWT; header `Authorization` ignorado)
- Para que serve: envia por e-mail um link de redefinição.

Como funciona:

- Resposta sempre igual (200), exista ou não a conta, para não revelar quais e-mails estão cadastrados.
- Só gera link se existir exatamente uma conta **ativa** com o e-mail (comparação sem diferenciar maiúsculas).
- O link contém um token aleatório; o banco guarda apenas o hash (SHA-256). Validade: 30 minutos, uso único. Um novo pedido invalida os links pendentes anteriores.
- O link enviado tem o formato `{FRONTEND_URL}/redefinir-senha#token=<token>`.
- E-mail: console em desenvolvimento; SMTP por variáveis de ambiente em produção.
- Limite por endereço de origem: 5 por hora (`redefinicao_senha`).

Payload:

```json
{ "email": "marina.duarte@example.com" }
```

Resposta (200):

```json
{ "detail": "Se houver uma conta com este e-mail, enviaremos um link para redefinir a senha." }
```

Erros:

- 400 `{"email": ["Informe um endereço de email válido."]}` (e campo obrigatório)
- 429 `{"detail": "Muitas solicitações. Tente novamente mais tarde."}`

### 3.9 Confirmar redefinição de senha (RN-020)

- Método e URL: `POST /api/v1/usuarios/redefinir-senha/confirmar/`
- Autenticação: pública
- Para que serve: define a nova senha a partir do token do link.

Como funciona:

- O token é comparado pelo hash; precisa existir, não ter sido usado, não ter expirado e pertencer a conta ativa.
- A nova senha segue as validações do cadastro (mínimo 8, validadores do Django, confirmação igual).
- Ao concluir, marca o link como usado, invalida os demais links pendentes e **não** autentica o usuário (sem tokens na resposta). Sessões JWT já emitidas continuam válidas até expirar.
- Limite: 10 por hora por endereço de origem (`redefinicao_senha_confirmacao`).

Payload:

```json
{
  "token": "Zr8k1m3...token-recebido-no-link",
  "password": "NovaSenha#2026",
  "password_confirmacao": "NovaSenha#2026"
}
```

Resposta (200):

```json
{ "detail": "Senha redefinida. Entre com a nova senha." }
```

Erros:

- 400 `{"detail": "Este link de redefinição é inválido ou expirou. Solicite um novo."}` (inexistente, expirado, usado, invalidado ou conta inativa)
- 400 `{"password_confirmacao": "As senhas não coincidem."}` ou `{"password": [ ...mensagens dos validadores... ]}`
- 400 campos obrigatórios / `password` com menos de 8 caracteres
- 429 `{"detail": "Muitas solicitações. Tente novamente mais tarde."}`

---

## 4. Telefones do usuário (RN-021)

Prefixo: `/api/v1/usuarios/me/telefones/` (`TelefoneViewSet`, `SimpleRouter`). Métodos habilitados: `GET`, `POST`, `PATCH`, `DELETE` (e `HEAD`/`OPTIONS`). `PUT` não existe.
Autenticação: JWT. O queryset é limitado aos telefones do usuário logado; telefone de outro usuário responde 404. O dono vem sempre do token, nunca do corpo.

Campos do telefone: `id`, `numero` (somente dígitos), `tipo` (id do tipo), `tipo_descricao` (somente leitura), `e_principal`.

Regras (RN-021): número validado pela quantidade de dígitos do tipo (Celular 11, Fixo 10, Comercial 10 ou 11); sem limite de quantidade de telefones; sem unicidade de número;
sempre exatamente um principal; o primeiro telefone do usuário vira principal automaticamente; definir outro principal desmarca o anterior.
A lista vem ordenada com o principal primeiro.

### 4.1 Listar telefones

- `GET /api/v1/usuarios/me/telefones/`

Resposta (200):

```json
[
  { "id": 12, "numero": "53991234567", "tipo": 1, "tipo_descricao": "Celular", "e_principal": true },
  { "id": 15, "numero": "5336711234", "tipo": 2, "tipo_descricao": "Fixo", "e_principal": false }
]
```

Erros: 401.

### 4.2 Adicionar telefone

- `POST /api/v1/usuarios/me/telefones/`

Payload (`e_principal` opcional, padrão `false`):

```json
{ "numero": "(53) 3671-1234", "tipo": 2, "e_principal": false }
```

Resposta (201):

```json
{ "id": 15, "numero": "5336711234", "tipo": 2, "tipo_descricao": "Fixo", "e_principal": false }
```

Erros:

- 400 `{"numero": ["Telefone fixo deve ter 10 dígitos com DDD."]}` (demais mensagens por tipo na seção 3.2)
- 400 `{"tipo": ["Informe um tipo de telefone válido."]}`
- 401

### 4.3 Detalhar telefone

- `GET /api/v1/usuarios/me/telefones/{id}/` — resposta (200) igual a um item da listagem. Erros: 401, 404.

### 4.4 Editar telefone / definir principal

- `PATCH /api/v1/usuarios/me/telefones/{id}/`

Como funciona: altera `numero` e/ou `tipo` (o par é revalidado) e/ou `e_principal: true` (desmarca o anterior). Não é possível desmarcar o principal diretamente: é preciso definir outro como principal.

Payload (exemplos):

```json
{ "numero": "53999887766", "tipo": 1 }
```

```json
{ "e_principal": true }
```

Resposta (200): telefone atualizado (mesmo formato).

Erros:

- 400 `{"numero": ["Celular deve ter 11 dígitos com DDD."]}`
- 400 `{"e_principal": ["Defina outro telefone como principal."]}`
- 401, 404

### 4.5 Excluir telefone

- `DELETE /api/v1/usuarios/me/telefones/{id}/`

Como funciona: não exclui o último telefone nem o principal (não há promoção automática de outro).

Resposta: 204 sem corpo.

Erros:

- 400 `{"detail": "Você precisa manter ao menos um telefone."}`
- 400 `{"detail": "Defina outro telefone como principal antes de excluir este."}`
- 401, 404

---

## 5. Tipos de telefone

- Método e URL: `GET /api/v1/tipos-telefone/`
- Autenticação: pública (sem autenticação JWT; header `Authorization` ignorado). Necessário no cadastro, que é feito sem login.
- Para que serve: lista os tipos fixos (Celular, Fixo, Comercial). Sem paginação. Somente leitura.

Resposta (200):

```json
[
  { "id": 1, "descricao": "Celular" },
  { "id": 2, "descricao": "Fixo" },
  { "id": 3, "descricao": "Comercial" }
]
```

Os ids acima são ilustrativos: os registros são populados por migration, e o cliente deve consultar a lista em vez de fixar ids.

---

## 6. Lojas

Prefixo: `/api/v1/lojas/`. O roteador registra o recurso em `lojas/` (daí a URL `/lojas/lojas/`) e há duas rotas avulsas `me/` e `me/imagem/`.

Campos da loja (`LojaSerializer`): `loja_id`, `proprietario` (id, somente leitura), `proprietario_nome` (somente leitura), `nome`, `descricao`, `cnpj`, `imagem_perfil` (URL absoluta ou `null`), `ativa`.

### 6.1 Listar lojas

- `GET /api/v1/lojas/lojas/` — público. Devolve todas as lojas (inclusive inativas), sem filtros nem paginação.

Resposta (200):

```json
[
  {
    "loja_id": 3,
    "proprietario": 5,
    "proprietario_nome": "Joaquim Rosa",
    "nome": "Sítio Boa Esperança",
    "descricao": "Hortaliças e mel direto do produtor.",
    "cnpj": "11222333000181",
    "imagem_perfil": "http://localhost:8000/media/lojas/4c6f0e9d1a2b4c3d8e7f6a5b4c3d2e1f.jpg",
    "ativa": true
  }
]
```

### 6.2 Criar loja (RN-013, RN-018)

- `POST /api/v1/lojas/lojas/` — autenticado; a validação exige `is_produtor`.

Como funciona:

- O proprietário é sempre o usuário logado (campo `proprietario` ignorado).
- Cada produtor pode ter somente uma loja: validada na API e garantida por restrição única no banco (cobre pedidos simultâneos).
- Imagem opcional: JSON (sem imagem) ou `multipart/form-data` com `imagem_perfil` (JPG/PNG/WEBP até 5 MB). Se a imagem for inválida, a loja não é criada.
- `ativa` padrão `true`. `cnpj` é texto de até 14 caracteres e único; **não há validação de dígitos verificadores** no código.

Payload (JSON):

```json
{
  "nome": "Sítio Boa Esperança",
  "descricao": "Hortaliças e mel direto do produtor.",
  "cnpj": "11222333000181"
}
```

Resposta (201): objeto da loja (como em 6.1).

Erros:

- 400 `{"non_field_errors": ["Usuário precisa ser produtor para criar uma loja."]}`
- 400 `{"non_field_errors": ["Cada produtor pode possuir somente uma loja."]}`
- 400 `{"cnpj": ["..."]}` (CNPJ já cadastrado ou com mais de 14 caracteres)
- 400 `{"imagem_perfil": ["Envie uma imagem JPG, PNG ou WEBP válida."]}` / `["A imagem deve ter no máximo 5 MB."]`
- 401

### 6.3 Detalhar loja

- `GET /api/v1/lojas/lojas/{loja_id}/` — público. Resposta (200): objeto da loja. Erros: 404.

`PUT`, `PATCH` e `DELETE` **não** estão habilitados em `/lojas/lojas/{id}/` (`http_method_names = ['get', 'post']`); a edição é feita por `/lojas/me/`.

### 6.4 Minha loja

- `GET /api/v1/lojas/me/` — autenticado. Devolve a loja de que o usuário é proprietário. Resposta (200): objeto da loja.
- Erros: 404 `{"detail": "Você não possui uma loja cadastrada."}`; 401.

### 6.5 Atualizar minha loja (RN-018)

- `PATCH /api/v1/lojas/me/` — autenticado, dono da loja.

Como funciona:

- Campos aceitos: `nome`, `descricao`, `ativa`, `imagem_perfil`. Qualquer outro campo (CNPJ, proprietário...) recusa a requisição inteira.
- `ativa: false` desativa a loja: preserva histórico e impede novas compras; a loja inativa continua editável.
- Imagem: `multipart/form-data` com `imagem_perfil`. A nova imagem substitui a anterior; o arquivo antigo é removido do storage após o commit (e só se não for usado por outra loja).
- Mesmo neste PATCH, a validação do serializer exige que o usuário seja produtor.

Payload JSON:

```json
{ "nome": "Sítio Boa Esperança - Hortifruti", "descricao": "Colhido no sábado de manhã.", "ativa": true }
```

Resposta (200): objeto da loja atualizado.

Erros:

- 400 `{"detail": "Somente nome, descrição, imagem e status da loja podem ser alterados nesta área."}`
- 400 `{"imagem_perfil": ["Envie uma imagem JPG, PNG ou WEBP válida."]}` / `["A imagem deve ter no máximo 5 MB."]`
- 404 `{"detail": "Você não possui uma loja cadastrada."}`
- 401

### 6.6 Remover imagem da loja

- `DELETE /api/v1/lojas/me/imagem/` — autenticado, dono da loja.
- Remove a imagem sem enviar outra; o arquivo é apagado do storage após o commit (se não usado por outra loja).
- Resposta: 204 sem corpo.
- Erros: 404 `{"detail": "Você não possui uma loja cadastrada."}` ou `{"detail": "A loja não possui imagem."}`; 401.

---

## 7. Produtos

Prefixo: `/api/v1/produtos/` (`ProdutoViewSet`). Métodos habilitados: `GET`, `POST`, `PATCH`. **Não há `PUT` nem `DELETE`**: produtos não são excluídos, são desativados (`ativo: false`).

Campos do produto (`ProdutoSerializer`):

| Campo | Tipo | Observação |
| --- | --- | --- |
| `produto_id` | int | somente leitura |
| `loja` | int | somente leitura; vem da loja do usuário logado |
| `loja_nome` | string | somente leitura |
| `nome` | string (até 155) | obrigatório |
| `descricao` | string | opcional |
| `categoria` | int | obrigatório; precisa ser categoria ativa |
| `categoria_nome` | string | somente leitura |
| `codigo_barras` | string (até 13) | opcional, texto |
| `estoque` | int | padrão 0; não pode ser negativo |
| `estoque_baixo` | bool | somente leitura; `true` com estoque de 1 a 5 (RN-017) |
| `sku` | string | somente leitura; gerado automaticamente (14 dígitos: loja 4 + categoria 4 + produto 6) |
| `ativo` | bool | padrão `true` |
| `preco` | número ou `null` | somente leitura; preço de venda menos desconto do preço vigente |
| `preco_original` | número ou `null` | somente leitura; `preco_venda` vigente |
| `desconto` | int ou `null` | somente leitura; percentual do preço vigente |
| `imagem` | string ou `null` | somente leitura; URL absoluta da imagem principal |
| `imagens` | array | somente leitura; ver seção 10 |

O preço vigente é o registro de preço sem `vigencia_fim` (último). Um produto recém-criado não tem preço (`preco` = `null`) até que se crie um preço (seção 9).

Exemplo de produto (resposta):

```json
{
  "produto_id": 12,
  "loja": 3,
  "loja_nome": "Sítio Boa Esperança",
  "nome": "Mel de laranjeira 500 g",
  "descricao": "Mel puro, safra 2026.",
  "categoria": 4,
  "categoria_nome": "Mel e derivados",
  "codigo_barras": "7891234567895",
  "estoque": 18,
  "estoque_baixo": false,
  "sku": "00030004000012",
  "ativo": true,
  "preco": 26.1,
  "preco_original": 29.0,
  "desconto": 10,
  "imagem": "http://localhost:8000/media/produtos/9b1deb4d3b7d4bad9bdd2b0d7b3dcb6d.jpg",
  "imagens": [
    { "id": 40, "imagem": "http://localhost:8000/media/produtos/9b1deb4d3b7d4bad9bdd2b0d7b3dcb6d.jpg", "ordem": 0, "e_principal": true }
  ]
}
```

### 7.1 Listar produtos (catálogo)

- `GET /api/v1/produtos/` — público.
- Retorna apenas produtos **ativos**, de loja **ativa** e com **estoque > 0** (RN-017). Produto sem estoque não aparece na listagem.
- Query: `categoria` (id numérico) filtra por categoria.
- Resposta (200): array de produtos (formato acima).

Erros:

- 400 `{"categoria": "Informe o identificador numérico da categoria."}`

### 7.2 Detalhar produto

- `GET /api/v1/produtos/{produto_id}/` — público.
- Retorna apenas produto **ativo** de loja **ativa** (estoque 0 é aceito: o detalhe pelo link direto continua acessível, com compra bloqueada: o backend recusa a inclusão no carrinho e a finalização, RN-017).
- Produto inativo ou de loja inativa responde 404, inclusive para o próprio dono (o dono consulta pelo `meus`).

Erros: 404, 400 (`categoria` inválida, se usado na query).

### 7.3 Cadastrar produto

- `POST /api/v1/produtos/` — autenticado; somente produtor (ou administrador) com loja.

Como funciona:

- A loja é definida pelo backend (primeira loja do usuário); o campo `loja` do corpo é ignorado.
- O SKU é gerado automaticamente e não pode ser alterado.
- A categoria precisa estar ativa.
- O preço **não** é criado aqui: usar `POST /produtos/precos/`. Imagens: `POST /produtos/{id}/imagens/`.

Payload:

```json
{
  "nome": "Mel de laranjeira 500 g",
  "descricao": "Mel puro, safra 2026.",
  "categoria": 4,
  "codigo_barras": "7891234567895",
  "estoque": 18,
  "ativo": true
}
```

Resposta (201): produto (formato acima), com `preco`, `preco_original`, `desconto` e `imagem` nulos e `imagens` vazio.

Erros:

- 400 `{"categoria": ["A categoria selecionada está inativa e não pode ser usada em novos cadastros ou alterações."]}`
- 400 `{"estoque": ["O estoque não pode ser negativo."]}`
- 400 `{"nome": ["Este campo é obrigatório."]}` / `{"categoria": ["Este campo é obrigatório."]}`
- 401
- 403 `{"detail": "Somente produtores podem cadastrar produtos."}`
- 403 `{"detail": "Cadastre uma loja antes de cadastrar produtos."}`

### 7.4 Editar produto

- `PATCH /api/v1/produtos/{produto_id}/` — dono do produto (proprietário da loja) ou administrador.

Como funciona:

- Edição parcial de `nome`, `descricao`, `categoria`, `codigo_barras`, `estoque`, `ativo`. `loja` e `sku` são somente leitura.
- Produtor só encontra produtos da própria loja; produto de outra loja responde **404**. Administrador acessa qualquer produto.
- Produto já vinculado a categoria inativa pode ter os demais dados editados; só é recusada a troca para uma categoria inativa.
- Se `estoque` for alterado, as quantidades dos carrinhos de clientes que passam do novo estoque são reduzidas ao estoque atual, podendo chegar a 0 (RN-017). A reposição não restaura a quantidade.
- Desativar o produto (`ativo: false`) o remove do catálogo e impede novas compras.

Payload:

```json
{ "estoque": 4, "ativo": true }
```

Resposta (200): produto atualizado (com `estoque_baixo: true` neste exemplo).

Erros: 400 (`estoque` negativo, categoria inativa), 401, 404.

### 7.5 Meus produtos

- `GET /api/v1/produtos/meus/` — produtor ou administrador.
- Lista todos os produtos da loja do usuário (ativos e inativos, com ou sem estoque). Administrador vê os produtos de todas as lojas.
- Query: `categoria` (id numérico).
- Resposta (200): array de produtos.

Erros:

- 400 `{"categoria": "Informe o identificador numérico da categoria."}`
- 401
- 403 `{"detail": "Somente produtores podem consultar seus produtos."}`

---

## 8. Categorias

Prefixo: `/api/v1/produtos/categorias/` (`CategoriaViewSet`). Métodos habilitados: `GET`, `POST`, `PATCH` (e `HEAD`/`OPTIONS`). Sem `PUT` e sem `DELETE`: categorias não são excluídas, apenas inativadas.

Campos: `categoria_id`, `nome` (único, até 100), `ativo` (padrão `true`).

### 8.1 Listar categorias

- `GET /api/v1/produtos/categorias/` — público.
- Query: `ativo=true` ou `ativo=false` (o frontend usa `?ativo=true`). Sem o parâmetro, devolve todas (inclusive as sugeridas e ainda inativas).

Resposta (200):

```json
[
  { "categoria_id": 1, "nome": "Hortaliças", "ativo": true },
  { "categoria_id": 4, "nome": "Mel e derivados", "ativo": true },
  { "categoria_id": 9, "nome": "Plantas medicinais", "ativo": false }
]
```

Erros: 400 `{"ativo": "Informe true ou false."}`.

### 8.2 Detalhar categoria

- `GET /api/v1/produtos/categorias/{categoria_id}/` — público. Resposta (200): objeto da categoria. Erros: 404, 400 (`ativo` inválido, se informado).

### 8.3 Sugerir ou criar categoria

- `POST /api/v1/produtos/categorias/` — autenticado.

Como funciona:

- Produtor: a categoria é criada **inativa** (`ativo: false`, forçado pelo backend, mesmo que o corpo envie `true`) e fica visível publicamente na listagem completa; é uma sugestão.
- Administrador: cria categoria com o `ativo` informado (padrão `true`).
- Usuário autenticado que não é produtor nem administrador: recusado.

Payload:

```json
{ "nome": "Plantas medicinais" }
```

Resposta (201), quando criada por produtor:

```json
{ "categoria_id": 9, "nome": "Plantas medicinais", "ativo": false }
```

Erros:

- 400 `{"nome": ["..."]}` (nome já existente — mensagem padrão de campo único — ou obrigatório)
- 401
- 403 `{"detail": "Somente produtores podem sugerir categorias."}`

### 8.4 Renomear, ativar ou inativar categoria

- `PATCH /api/v1/produtos/categorias/{categoria_id}/` — **somente administrador** (`IsAdminUser`).

Payload:

```json
{ "ativo": true }
```

Resposta (200): categoria atualizada.

Erros: 400 (nome duplicado), 401, 403 (`{"detail": "Você não tem permissão para executar essa ação."}` para quem não é administrador), 404.

---

## 9. Preços

Prefixo: `/api/v1/produtos/precos/` (`PrecoProdutoViewSet`). Métodos habilitados: `GET` e `POST` (e `HEAD`/`OPTIONS`). Não há edição nem exclusão: o histórico de preços é preservado.
Autenticação: JWT. Listagem e detalhe mostram apenas preços dos produtos das lojas do próprio usuário (administrador vê todos).

Campos: `id`, `produto` (id), `preco_venda`, `preco_custo` (opcional), `preco_desconto` (somente leitura, calculado), `porcentagem_desconto` (inteiro de 0 a 100, opcional),
`vigencia_inicio` (somente leitura), `vigencia_fim` (somente leitura; `null` no preço vigente).

### 9.1 Listar e detalhar preços

- `GET /api/v1/produtos/precos/` — array de preços (histórico completo dos produtos da própria loja).
- `GET /api/v1/produtos/precos/{id}/` — um preço. Preço de produto de outra loja responde 404.

Resposta (200) de um item:

```json
{
  "id": 21,
  "produto": 12,
  "preco_venda": "29.00",
  "preco_custo": "18.00",
  "preco_desconto": "2.90",
  "porcentagem_desconto": 10,
  "vigencia_inicio": "2026-10-20T12:00:00.123456Z",
  "vigencia_fim": null
}
```

Erros: 401, 404.

### 9.2 Criar preço

- `POST /api/v1/produtos/precos/` — dono do produto ou administrador.

Como funciona:

- O novo registro vira o **preço vigente** e o preço vigente anterior do produto recebe `vigencia_fim` (agora). O preço vigente é o considerado na compra e na finalização do pedido.
- `preco_desconto` não é enviado: é calculado como `preco_venda * porcentagem_desconto / 100`. Sem `porcentagem_desconto`, não há desconto (`preco_desconto` e `porcentagem_desconto` ficam `null`).
- Valores negativos são recusados; desconto fora de 0 a 100 é recusado.
- Produto de outra loja é recusado com 403.

Payload:

```json
{ "produto": 12, "preco_venda": "29.00", "preco_custo": "18.00", "porcentagem_desconto": 10 }
```

Resposta (201): preço criado (formato acima).

Erros:

- 400 `{"preco_venda": ["O preço de venda não pode ser negativo."]}`
- 400 `{"preco_custo": ["O preço de custo não pode ser negativo."]}`
- 400 `{"porcentagem_desconto": ["Informe um desconto entre 0 e 100%."]}`
- 400 `{"produto": [...]}` (produto inexistente ou campo ausente)
- 401
- 403 `{"detail": "Você não pode alterar o preço de um produto de outra loja."}`

---

## 10. Imagens de produto (RN-016)

Prefixo: `/api/v1/produtos/{produto_id}/imagens/` (`ImagemProdutoViewSet`). Métodos habilitados: `GET`, `POST`, `PATCH`, `DELETE` (e `HEAD`/`OPTIONS`); `PUT` não existe.
O `produto_id` precisa ser numérico (`\d+`).

Campos: `id`, `imagem` (URL absoluta), `ordem` (somente leitura), `e_principal`.

Regras:

- Cada produto tem de 0 a 5 imagens. A primeira enviada vira principal automaticamente; definir outra como principal desmarca a anterior; ao excluir a principal, a próxima pela ordem é promovida.
- Aceita JPG, PNG ou WEBP de até 5 MB (extensão e conteúdo conferidos); o arquivo é renomeado com nome aleatório.
- Uma imagem enviada não é substituída: para trocar, exclui-se a imagem e envia-se outra.
- Leitura: pública, para produtos ativos de loja ativa (o dono e o administrador também leem produtos inativos). Escrita: somente o dono do produto ou o administrador; para os demais o produto "não existe" (404).

### 10.1 Listar e detalhar

- `GET /api/v1/produtos/{produto_id}/imagens/` — público. Array ordenado por `ordem`.
- `GET /api/v1/produtos/{produto_id}/imagens/{id}/` — público.

Resposta (200):

```json
[
  { "id": 40, "imagem": "http://localhost:8000/media/produtos/9b1deb4d3b7d4bad9bdd2b0d7b3dcb6d.jpg", "ordem": 0, "e_principal": true },
  { "id": 41, "imagem": "http://localhost:8000/media/produtos/0a1b2c3d4e5f60718293a4b5c6d7e8f9.png", "ordem": 1, "e_principal": false }
]
```

Erros: 404 (produto inexistente, não visível ou imagem de outro produto).

### 10.2 Enviar imagem

- `POST /api/v1/produtos/{produto_id}/imagens/` — dono do produto ou administrador. `multipart/form-data`.

Payload (campos do formulário):

- `imagem`: arquivo (obrigatório)
- `e_principal`: `true` para torná-la a principal (opcional)

Resposta (201):

```json
{ "id": 42, "imagem": "http://localhost:8000/media/produtos/5d6e7f8091a2b3c4d5e6f708192a3b4c.webp", "ordem": 2, "e_principal": false }
```

A `ordem` é definida pelo backend (última ordem + 1).

Erros:

- 400 `{"imagem": ["Envie uma imagem JPG, PNG ou WEBP válida."]}` ou `["A imagem deve ter no máximo 5 MB."]`; extensão fora de JPG/JPEG/PNG/WEBP é recusada pelo validador de extensão do Django
- 400 `{"imagem": "Cada produto pode ter no máximo 5 imagens."}` (valor em string)
- 401
- 404 (produto de outra loja ou inexistente)

### 10.3 Definir imagem principal

- `PATCH /api/v1/produtos/{produto_id}/imagens/{id}/` — dono do produto ou administrador.
- Na prática só `e_principal: true` tem efeito. Enviar `imagem` é recusado; desmarcar a principal diretamente é recusado.

Payload:

```json
{ "e_principal": true }
```

Resposta (200): imagem atualizada.

Erros:

- 400 `{"e_principal": ["Defina outra imagem como principal para desmarcar esta."]}`
- 400 `{"imagem": ["Para trocar a imagem, exclua esta e envie uma nova."]}`
- 401, 404

### 10.4 Excluir imagem

- `DELETE /api/v1/produtos/{produto_id}/imagens/{id}/` — dono do produto ou administrador.
- Remove o registro e o arquivo do storage; se era a principal, a próxima pela ordem é promovida.
- Resposta: 204 sem corpo. Erros: 401, 404.

### 10.5 Reordenar imagens

- `POST /api/v1/produtos/{produto_id}/imagens/reordenar/` — dono do produto ou administrador.
- Recebe a lista **completa** de ids das imagens do produto na nova ordem (inteiros).

Payload:

```json
{ "imagens": [41, 40, 42] }
```

Resposta (200): array com as imagens na nova ordem (`ordem` 0, 1, 2...).

Erros:

- 400 `{"imagens": "Envie a lista com todas as imagens do produto, na nova ordem."}` (lista incompleta, com ids de outro produto ou não inteiros; valor em string)
- 401, 404

---

## 11. Carrinho (RN-017)

Prefixo: `/api/v1/carrinhos/` (`CarrinhoViewSet`). Autenticação: JWT em todas as rotas. Métodos habilitados: `GET`, `POST`, `PATCH`, `DELETE` (conforme cada rota abaixo).
O carrinho é salvo no backend, **um carrinho por cliente e por loja** (decisão v1); o frontend agrega os carrinhos para exibição.
O usuário só acessa os próprios carrinhos (de outro usuário, 404).

Carrinho (`CarrinhoSerializer`): `carrinho_id`, `loja`, `loja_nome`, `valor_bruto`, `valor_desconto`, `valor_liquido` (strings, calculados pelo backend com o preço vigente) e `itens[]`.

Item (`CarrinhoProdutoSerializer`): `carrinho_produto_id`, `carrinho`, `produto`, `produto_nome`, `loja`, `loja_nome`, `valor_unitario`, `valor_desconto` (números),
`quantidade`, `estoque` (estoque atual do produto), `disponivel` (ativo, loja ativa e estoque > 0), `subtotal` (número: `(valor_unitario - valor_desconto) * quantidade`).
Sem preço vigente, o item sai com `valor_unitario: null`, `valor_desconto: 0.0` e `subtotal: 0.0`.

Item com `quantidade` 0 (estoque reduzido por outro pedido ou pelo produtor) permanece no carrinho como "sem estoque" e não pode ser finalizado.

### 11.1 Listar carrinhos

- `GET /api/v1/carrinhos/`

Resposta (200):

```json
[
  {
    "carrinho_id": 8,
    "loja": 3,
    "loja_nome": "Sítio Boa Esperança",
    "valor_bruto": "58.00",
    "valor_desconto": "5.80",
    "valor_liquido": "52.20",
    "itens": [
      {
        "carrinho_produto_id": 15,
        "carrinho": 8,
        "produto": 12,
        "produto_nome": "Mel de laranjeira 500 g",
        "loja": 3,
        "loja_nome": "Sítio Boa Esperança",
        "valor_unitario": 29.0,
        "valor_desconto": 2.9,
        "quantidade": 2,
        "estoque": 18,
        "disponivel": true,
        "subtotal": 52.2
      }
    ]
  }
]
```

Erros: 401.

### 11.2 Detalhar carrinho

- `GET /api/v1/carrinhos/{carrinho_id}/` — resposta (200) igual a um elemento da listagem. Erros: 401, 404.

### 11.3 Adicionar produto ao carrinho

- `POST /api/v1/carrinhos/`

Como funciona:

- Produto precisa estar ativo e de loja ativa.
- Produto já presente em qualquer carrinho do usuário: **soma** a quantidade ao item existente (não duplica).
- A soma não pode ultrapassar o estoque atual.
- O carrinho da loja é criado se não existir e os totais são recalculados.

Payload (`quantidade` opcional, padrão 1, mínimo 1):

```json
{ "produto": 12, "quantidade": 2 }
```

Resposta (201): o **item** (não o carrinho), no formato de item da seção 11:

```json
{
  "carrinho_produto_id": 15,
  "carrinho": 8,
  "produto": 12,
  "produto_nome": "Mel de laranjeira 500 g",
  "loja": 3,
  "loja_nome": "Sítio Boa Esperança",
  "valor_unitario": 29.0,
  "valor_desconto": 2.9,
  "quantidade": 2,
  "estoque": 18,
  "disponivel": true,
  "subtotal": 52.2
}
```

Erros:

- 400 `{"detail": "Produto sem estoque suficiente para a quantidade solicitada."}`
- 400 `{"produto": ["Produto inativo não pode ser adicionado ao carrinho."]}`
- 400 `{"produto": ["Produto de loja inativa não pode ser adicionado ao carrinho."]}`
- 400 `{"produto": ["Pk inválido ..."]}` (produto inexistente), `{"quantidade": ["Certifique-se de que este valor seja maior ou igual a 1."]}`
- 401

### 11.4 Alterar quantidade de um item

- `PATCH /api/v1/carrinhos/itens/{item_id}/` — `item_id` é o `carrinho_produto_id`.
- Define a nova quantidade (valor absoluto, não soma). Mínimo 1; para zerar/remover, use o `DELETE`. Não pode ultrapassar o estoque.

Payload:

```json
{ "quantidade": 3 }
```

Resposta (200): o item atualizado (formato de item).

Erros:

- 400 `{"detail": "Produto sem estoque suficiente para a quantidade solicitada."}`
- 400 `{"quantidade": ["Certifique-se de que este valor seja maior ou igual a 1."]}`
- 401, 404 (item inexistente ou de outro usuário)

### 11.5 Remover item

- `DELETE /api/v1/carrinhos/itens/{item_id}/`
- Remove o item; se o carrinho ficar sem itens, ele é removido; senão, os totais são recalculados.
- Resposta: 204 sem corpo. Erros: 401, 404.

Não há rota para esvaziar todo o carrinho nem para `PUT`. O carrinho é limpo dos itens finalizados na criação do pedido (seção 12.3).

---

## 12. Pedidos (RN-011, RN-017, RN-019, RN-021, RN-022)

Prefixo: `/api/v1/pedidos/` (`PedidoViewSet`). Autenticação: JWT em todas as rotas. Métodos habilitados na classe: `GET`, `POST`, `PATCH`.
Não há `PUT` nem `DELETE`: pedidos não são excluídos nem editados; encerra-se um pedido com o status `Cancelado`.
O pedido representa uma solicitação de **retirada presencial** na feira (sem pagamento online, entrega ou frete).

Status e transições permitidas (`STATUS_TRANSICOES`):

```text
Pendente -> Em preparo -> Pronto para retirada -> Entregue
Pendente -> Cancelado
Em preparo -> Cancelado
```

`Entregue` e `Cancelado` são finais, sem retorno.

Pedido (`PedidoSerializer`), usado para o cliente:

| Campo | Observação |
| --- | --- |
| `pedido_id`, `loja`, `loja_nome` | identificação do pedido e da loja |
| `status` | id do status; `status_nome` é o texto (`Pendente`, `Em preparo`, `Pronto para retirada`, `Entregue`, `Cancelado`) |
| `valor_bruto`, `valor_desconto`, `valor_liquido` | strings; calculados pelo backend |
| `data_criacao` | ISO 8601 UTC |
| `itens[]` | `pedido_produto_id`, `produto` (id ou `null` se o produto foi excluído), `nome_produto`, `quantidade`, `valor_unitario`, `valor_desconto`, `subtotal` (strings, snapshot) e `avaliacao` (`null` ou `{avaliacao_id, nota, comentario}`) |
| `cliente` | snapshot do cliente: `pedido_cliente_id`, `nome`, `cpf`, `email`, `data_nascimento`, `genero` (texto, ex.: `"Feminino"`). **Sem telefone** (RN-021) |

Exemplo de pedido:

```json
{
  "pedido_id": 31,
  "loja": 3,
  "loja_nome": "Sítio Boa Esperança",
  "status": 1,
  "status_nome": "Pendente",
  "valor_bruto": "58.00",
  "valor_desconto": "5.80",
  "valor_liquido": "52.20",
  "data_criacao": "2026-10-20T14:32:10.512345Z",
  "itens": [
    {
      "pedido_produto_id": 57,
      "produto": 12,
      "nome_produto": "Mel de laranjeira 500 g",
      "quantidade": 2,
      "valor_unitario": "29.00",
      "valor_desconto": "2.90",
      "subtotal": "52.20",
      "avaliacao": null
    }
  ],
  "cliente": {
    "pedido_cliente_id": 31,
    "nome": "Marina Oliveira Duarte",
    "cpf": "52998224725",
    "email": "marina.duarte@example.com",
    "data_nascimento": "1992-04-18",
    "genero": "Feminino"
  }
}
```

### 12.1 Listar meus pedidos

- `GET /api/v1/pedidos/` — pedidos **feitos** pelo usuário logado (como cliente, inclusive produtor comprando em outra loja). Sem filtros e sem paginação.
- Resposta (200): array de pedidos (formato acima). Erros: 401.

### 12.2 Detalhar pedido

- `GET /api/v1/pedidos/{pedido_id}/` — somente se o usuário for o cliente do pedido; caso contrário 404 (não revela o pedido).
- Resposta (200): pedido. Erros: 401, 404.

### 12.3 Finalizar carrinho (criar pedidos)

- `POST /api/v1/pedidos/` — autenticado.

Como funciona (tudo em uma transação; se um item for recusado, **nenhum** pedido é criado):

1. Recebe os ids dos itens selecionados do carrinho (`carrinho_produto_ids`); apenas esses itens são finalizados.
2. Todos os itens precisam pertencer a carrinhos do usuário logado.
3. Trava os produtos e valida cada item: produto da loja do carrinho, produto ativo, loja ativa, quantidade ≥ 1 (item "sem estoque" é recusado), estoque suficiente e preço vigente existente.
4. **Split por loja (RN-011):** cria um pedido para cada loja/produtor, com status `Pendente`. A compra não agrupa os pedidos.
5. Calcula os totais no backend com o preço vigente (o frontend não define valores).
6. **Snapshot (RN-019, RN-021):** grava os dados do cliente (nome, CPF, e-mail, data de nascimento, gênero; sem telefone) e, em cada item, nome do produto, valor unitário, desconto, quantidade e subtotal.
7. Baixa o estoque (RN-017).
8. Remove os itens finalizados do carrinho (carrinho vazio é apagado, senão recalculado) e ajusta os carrinhos de outros clientes que passaram do novo estoque (RN-017).

Payload:

```json
{ "carrinho_produto_ids": [15, 16, 17] }
```

Resposta (201): **array** com os pedidos criados, um por loja (formato de pedido da seção 12), por exemplo dois pedidos quando os itens são de duas lojas.

Erros:

- 400 `{"carrinho_produto_ids": ["Certifique-se de que este campo tenha pelo menos 1 elementos."]}` (lista vazia)
- 400 `{"carrinho_produto_ids": ["Este campo é obrigatório."]}` (campo ausente)
- 400 `{"detail": "Um ou mais itens do carrinho são inválidos."}`
- 400 `{"detail": "O produto <nome> não pertence à loja do carrinho."}`
- 400 `{"detail": "O produto <nome> está inativo."}`
- 400 `{"detail": "A loja <nome> está inativa."}`
- 400 `{"detail": "O produto <nome> está sem estoque. Remova-o da seleção para finalizar."}`
- 400 `{"detail": "O produto <nome> não possui estoque suficiente."}`
- 400 `{"detail": "O produto <nome> não possui preço vigente."}`
- 401

### 12.4 Atualizar pedido genérico

- `PATCH /api/v1/pedidos/{pedido_id}/` — sempre 405 `{"detail": "Use o endpoint de status para atualizar pedidos."}`. Usar os endpoints 12.5 a 12.7.

### 12.5 Atualizar status (produtor)

- `PATCH /api/v1/pedidos/{pedido_id}/status/` — produtor da loja do pedido ou administrador.

Como funciona:

- Somente `is_produtor` ou `is_staff` (os demais recebem 403 antes de qualquer consulta).
- O produtor só alcança pedidos da própria loja (outros: 404); o administrador, qualquer pedido.
- O campo `status` recebe o **id** do status (`status_pedido_id`), obtido em `GET /pedidos/status-disponiveis/`, e não o texto.
  Atenção: enviar o texto (ex.: `"Em preparo"`) hoje resulta em 500 em vez de 400 (ver "Limitações conhecidas").
- Respeita estritamente as transições (sem retorno). Cancelar restaura o estoque de cada item uma única vez (itens cujo produto foi excluído são ignorados).
- A transição `Pronto para retirada -> Entregue` também pode ser feita pelo cliente (12.7).

Payload:

```json
{ "status": 2 }
```

Resposta (200): pedido na visão do produtor (`PedidoProdutorSerializer`): mesmos campos do pedido, mas `cliente` contém apenas `nome` e `telefone`
(telefone principal **atual** do cliente, somente nos status `Pendente`, `Em preparo` e `Pronto para retirada`; `null` em `Entregue`/`Cancelado` ou se o cliente não tiver telefone, RN-021):

```json
{
  "pedido_id": 31,
  "loja": 3,
  "loja_nome": "Sítio Boa Esperança",
  "status": 2,
  "status_nome": "Em preparo",
  "valor_bruto": "58.00",
  "valor_desconto": "5.80",
  "valor_liquido": "52.20",
  "data_criacao": "2026-10-20T14:32:10.512345Z",
  "itens": [ { "pedido_produto_id": 57, "produto": 12, "nome_produto": "Mel de laranjeira 500 g", "quantidade": 2, "valor_unitario": "29.00", "valor_desconto": "2.90", "subtotal": "52.20", "avaliacao": null } ],
  "cliente": { "nome": "Marina Oliveira Duarte", "telefone": "53991234567" }
}
```

Erros:

- 400 `{"detail": "Status inválido."}`
- 400 `{"detail": "Não é possível alterar um pedido de Pendente para Entregue."}` (texto com os status atual e solicitado)
- 401
- 403 `{"detail": "Somente produtores podem atualizar o status de pedidos."}`
- 404

### 12.6 Cancelar pedido (cliente)

- `PATCH /api/v1/pedidos/{pedido_id}/cancelar/` — cliente do pedido. Sem corpo.

Como funciona: só atua sobre pedidos feitos pelo próprio usuário (inclusive para administrador); somente pedido `Pendente`; cancelamento imediato, sem motivo (MVP);
o pedido continua no histórico como `Cancelado` e o estoque de cada item é restaurado uma única vez.

Resposta (200): pedido (visão do cliente) com `status_nome: "Cancelado"`.

Erros:

- 400 `{"detail": "Somente pedidos pendentes podem ser cancelados pelo cliente."}`
- 401, 404 (pedido inexistente ou de outro cliente)

### 12.7 Confirmar recebimento (cliente, RN-022)

- `PATCH /api/v1/pedidos/{pedido_id}/confirmar-entrega/` — cliente do pedido. Sem corpo.

Como funciona: somente pedidos próprios `Pronto para retirada`; muda para `Entregue` (final, sem retorno). Não altera estoque. Vale para qualquer usuário que compre, inclusive produtor em pedido de outra loja.
Depois disso, os itens podem ser avaliados (seção 14) e o produtor deixa de ver o telefone. O sistema não registra quem confirmou nem a data da retirada.

Resposta (200): pedido (visão do cliente) com `status_nome: "Entregue"`.

Erros:

- 400 `{"detail": "Somente pedidos prontos para retirada podem ter o recebimento confirmado."}`
- 401, 404

### 12.8 Pedidos recebidos pela minha loja

- `GET /api/v1/pedidos/minha-loja/` — produtor ou administrador.
- Produtor: pedidos da própria loja. Administrador: pedidos de todas as lojas.
- Resposta (200): array de pedidos na visão do produtor (12.5): `cliente` com `nome` (snapshot) e `telefone` (principal atual, conforme o status).

Erros:

- 401
- 403 `{"detail": "Somente produtores podem consultar pedidos da loja."}`

### 12.9 Status disponíveis

- `GET /api/v1/pedidos/status-disponiveis/` — produtor ou administrador.
- Lista os cinco status (criando-os se não existirem). Usado para obter o id a enviar em 12.5.

Resposta (200) (ids ilustrativos; use os devolvidos pela API):

```json
[
  { "status_pedido_id": 1, "status": "Pendente" },
  { "status_pedido_id": 2, "status": "Em preparo" },
  { "status_pedido_id": 3, "status": "Pronto para retirada" },
  { "status_pedido_id": 4, "status": "Entregue" },
  { "status_pedido_id": 5, "status": "Cancelado" }
]
```

Erros:

- 401
- 403 `{"detail": "Somente produtores podem consultar os status de pedidos."}`

---

## 13. Favoritos

Prefixo: `/api/v1/favoritos/` (`FavoritoViewSet`). Autenticação: JWT (qualquer usuário, inclusive produtor). Métodos habilitados: `GET`, `POST`, `DELETE`. Sem `PUT`/`PATCH`.
O usuário só vê e remove os próprios favoritos (de outro usuário, 404). Lista ordenada do mais recente para o mais antigo.

Campos: `favorito_id`, `produto` (id; escrita), `dados_produto` (somente leitura: produto completo da seção 7 mais `disponivel`) e `data_criacao`.
`disponivel` é `true` quando o produto está ativo, a loja está ativa e há estoque; produtos inativos, sem estoque ou de loja inativa permanecem na lista, mas não podem ir ao carrinho.

### 13.1 Listar e detalhar

- `GET /api/v1/favoritos/` — array.
- `GET /api/v1/favoritos/{favorito_id}/` — um favorito.

Resposta (200) de um item:

```json
{
  "favorito_id": 9,
  "produto": 12,
  "dados_produto": {
    "produto_id": 12,
    "loja": 3,
    "loja_nome": "Sítio Boa Esperança",
    "nome": "Mel de laranjeira 500 g",
    "descricao": "Mel puro, safra 2026.",
    "categoria": 4,
    "categoria_nome": "Mel e derivados",
    "codigo_barras": "7891234567895",
    "estoque": 18,
    "estoque_baixo": false,
    "sku": "00030004000012",
    "ativo": true,
    "preco": 26.1,
    "preco_original": 29.0,
    "desconto": 10,
    "imagem": "http://localhost:8000/media/produtos/9b1deb4d3b7d4bad9bdd2b0d7b3dcb6d.jpg",
    "imagens": [],
    "disponivel": true
  },
  "data_criacao": "2026-10-20T15:01:44.100000Z"
}
```

Erros: 401, 404.

### 13.2 Favoritar produto

- `POST /api/v1/favoritos/`

Como funciona: o usuário vem do token; o mesmo produto não pode ser favoritado duas vezes pelo mesmo usuário.

Payload:

```json
{ "produto": 12 }
```

Resposta (201): favorito (formato acima).

Erros:

- 400 `["Produto já está nos favoritos."]` (corpo é um array)
- 400 `{"produto": ["Pk inválido ..."]}` (produto inexistente) / `{"produto": ["Este campo é obrigatório."]}`
- 401

### 13.3 Remover favorito

- `DELETE /api/v1/favoritos/{favorito_id}/` — o id é o `favorito_id`, não o id do produto.
- Resposta: 204 sem corpo. Erros: 401, 404.

---

## 14. Avaliações (RN-010)

Prefixo: `/api/v1/avaliacoes/` (`AvaliacaoViewSet`). Métodos habilitados: `GET` e `POST`. Não há edição nem exclusão pelo autor (a remoção é moderação pelo administrador, na área administrativa do Django).

Campos: `avaliacao_id`, `pedido_produto` (id do item do pedido; escrita), `produto` (somente leitura; id ou `null` se o produto foi excluído), `produto_nome`,
`usuario_nome` (nome abreviado: primeiro nome e inicial do último sobrenome, ex.: `"Marina D."`; o nome completo não é exposto), `nota` (inteiro 1 a 5), `comentario` (opcional, até 500 caracteres).

### 14.1 Listar avaliações

- `GET /api/v1/avaliacoes/` — público.
- Query: `produto` (id) filtra por produto (usado no detalhe do produto). Sem o parâmetro, devolve todas as avaliações. Sem paginação e **sem média** (a média é calculada no frontend).

Resposta (200):

```json
[
  {
    "avaliacao_id": 5,
    "pedido_produto": 57,
    "produto": 12,
    "produto_nome": "Mel de laranjeira 500 g",
    "usuario_nome": "Marina D.",
    "nota": 5,
    "comentario": "Mel delicioso, retirei na feira no sábado."
  }
]
```

### 14.2 Detalhar avaliação

- `GET /api/v1/avaliacoes/{avaliacao_id}/` — exige autenticação (diferente da listagem, que é pública). Qualquer usuário autenticado pode consultar qualquer avaliação pelo id; o conteúdo é o mesmo da listagem pública (a diferença é apenas exigir login).
- Resposta (200): objeto da avaliação. Erros: 401, 404.

### 14.3 Avaliar item de pedido

- `POST /api/v1/avaliacoes/` — autenticado.

Como funciona:

- Avalia-se um **item do pedido** (`pedido_produto`), não o produto. O backend vincula automaticamente o usuário autenticado e o produto do item.
- O item precisa pertencer a um pedido do próprio usuário, e o pedido precisa estar `Entregue`. Vale para qualquer usuário que compre, inclusive produtor.
- Cada item pode ser avaliado uma única vez (também garantido por unicidade no banco). Itens do mesmo produto em pedidos diferentes são avaliados separadamente.
- Item cujo produto foi excluído e que ainda não foi avaliado não pode mais ser avaliado.

Payload (`comentario` opcional):

```json
{ "pedido_produto": 57, "nota": 5, "comentario": "Mel delicioso, retirei na feira no sábado." }
```

Resposta (201): avaliação (formato acima).

Erros:

- 400 `{"pedido_produto": ["Este item não pertence ao seu pedido."]}` (item inexistente ou de pedido de outro usuário)
- 400 `{"pedido_produto": ["Só é possível avaliar pedidos entregues."]}`
- 400 `{"pedido_produto": ["Este produto não está mais disponível para avaliação."]}`
- 400 `{"pedido_produto": ["Este item já foi avaliado."]}`
- 400 `{"comentario": ["O comentário deve ter no máximo 500 caracteres."]}`
- 400 `{"nota": ["Este campo é obrigatório."]}` ou fora de 1 a 5 (validador padrão do Django)
- 401

---

## 15. Limitações conhecidas

Comportamentos atuais confirmados que divergem do esperado (documentados, não corrigidos):

- `PATCH` e `DELETE` em `/api/v1/carrinhos/itens/{item_id}/` com `item_id` não numérico respondem **500** (o regex da rota aceita letras).
- `PATCH` em `/api/v1/pedidos/{id}/status/`, `/cancelar/` e `/confirmar-entrega/` com `id` não numérico respondem **500**.
- `PATCH /api/v1/pedidos/{id}/status/` com `status` em texto (ex.: `"Em preparo"`) responde **500** em vez de 400; o campo deve ser o id numérico do status.
- `GET /api/v1/avaliacoes/?produto=abc` (endpoint público) responde **500**.
- Os detalhes padrão com id não numérico (ex.: `/api/v1/pedidos/abc/`, `/api/v1/produtos/abc/`) respondem 404, não 500.
- Inconsistência de contrato: a listagem de avaliações é pública, mas o detalhe (`/avaliacoes/{id}/`) exige login, embora traga o mesmo conteúdo.
