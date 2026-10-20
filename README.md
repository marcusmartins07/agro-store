# Agro Store

Monorepo com API Django e aplicação web Vue.

## Funcionalidades principais

- Catálogo público de produtos com filtro por categoria e imagens por produto (até 5, com uma principal).
- Controle de disponibilidade por estoque: produto com estoque 0 sai da listagem do catálogo (o detalhe continua acessível, com a compra bloqueada) e volta quando o estoque é reposto. Detalhes em [Disponibilidade por estoque](#disponibilidade-por-estoque-rn-017).
- Indicador de estoque baixo (1 a 5 unidades) na área do produtor.
- Carrinho salvo no backend, com ajuste automático da quantidade quando o estoque diminui.
- Finalização do carrinho com um pedido por loja, baixa de estoque e snapshot de cliente (sem o telefone, ver RN-021) e de produtos.
- Cancelamento de pedidos pendentes pelo cliente, com restauração do estoque.
- Confirmação de recebimento pelo cliente (RN-022): em "Meus pedidos", o botão "Confirmar recebimento" muda pedidos `Pronto para retirada` para `Entregue` e libera a avaliação dos itens. Detalhes em [Confirmação de recebimento](#confirmação-de-recebimento-rn-022).
- Avaliação de produtos comprados: na tela "Meus pedidos" (`/pedidos`), o cliente avalia cada item de pedido entregue (nota de 1 a 5 e comentário opcional). A rota antiga `/avaliacoes/:id` redireciona para `/pedidos`. Detalhes em [Avaliações](#avaliações-rn-010).
- Favoritos, perfil do usuário e cadastro de clientes.
- Telefones do usuário: um ou mais por conta, com tipo (Celular, Fixo ou Comercial) e exatamente um principal, gerenciados no perfil. Detalhes em [Telefones do usuário](#telefones-do-usuário-rn-021).
- Foto de perfil do usuário: opcional, enviada, trocada ou removida pelo próprio usuário. Detalhes em [Imagem da loja e foto de perfil](#imagem-da-loja-e-foto-de-perfil-rn-018).
- Imagem da loja: opcional, enviada na criação da loja ou depois, na área do produtor (`/minha-loja`, aba Minha loja). A página pública da loja ainda não exibe essa imagem (não implementada).
- Redefinição de senha por e-mail (`/esqueci-senha` e `/redefinir-senha`), com link de uso único e validade de 30 minutos. Detalhes em [Redefinição de senha](#redefinição-de-senha-rn-020).
- Área do produtor (`/minha-loja`): painel de indicadores, pedidos, produtos, preços, imagens e dados da loja.
- Informação de retirada presencial na feira (sem pagamento online, entrega ou frete no MVP).

## Estrutura

```text
apps/
  backend/   API Django REST Framework
  frontend/  SPA Vue + Vite
scripts/
  dev.mjs    inicia os dois serviços
```

## Requisitos

- Python 3.14.2
- Node.js 20.19+ ou 22.12+

## Instalação

No diretório raiz:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r apps/backend/requirements.txt
npm install
npm run migrate
```

No Linux/macOS, ative o ambiente com `source .venv/bin/activate`.

## Desenvolvimento

Com o ambiente virtual ativado:

```powershell
npm run dev
```

- Frontend: http://localhost:5173
- Backend: http://127.0.0.1:8000
- Admin Django: http://127.0.0.1:8000/admin/

O Vite encaminha `/api` e `/media` ao Django. Assim, o frontend não depende
de uma URL local fixa e a mesma origem pode ser usada em produção.

Comandos separados:

```powershell
npm run dev:backend
npm run dev:frontend
```

Validação:

```powershell
npm run check
```

O arquivo `.env` da raiz (copie de `.env.example`) só é carregado quando o backend é iniciado por `node scripts/backend.mjs <comando>` ou pelos scripts do `package.json`. Rodar `python apps/backend/manage.py` direto não lê o `.env`. Para aplicar migrations de um app específico, use, por exemplo, `node scripts/backend.mjs migrate usuarios 0005`.

## Variáveis de ambiente

Os nomes e os valores de exemplo estão em `.env.example`. Nunca versione valores reais, principalmente senhas, chaves e `DJANGO_SECRET_KEY`.

| Variável | Finalidade |
| --- | --- |
| `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` | Configuração básica do Django. |
| `CORS_ALLOWED_ORIGINS` | Origens do frontend autorizadas a chamar a API. |
| `DRF_NUM_PROXIES` | Quantidade de proxies reversos entre o cliente e o Django. O padrão é `0` (o cabeçalho `X-Forwarded-For` é ignorado). Defina `1` quando o backend rodar atrás de um proxy reverso; assim o limite de requisições por IP usa o IP real do cliente. Um valor errado faz o limite contar o IP do proxy ou aceitar IP forjado. |
| `FRONTEND_URL` | Endereço do frontend usado no link do e-mail de redefinição de senha. Em desenvolvimento, o padrão é `http://localhost:5173`; com `DJANGO_DEBUG=false` é obrigatória, e o backend não inicia sem ela. |
| `EMAIL_BACKEND` | Backend de e-mail do Django. O padrão (`console`) imprime as mensagens no terminal; em produção use `django.core.mail.backends.smtp.EmailBackend`. |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS` | Dados do servidor SMTP (usados com o backend SMTP). |
| `EMAIL_TIMEOUT` | Segundos de espera pelo servidor SMTP (padrão `10`). |
| `DEFAULT_FROM_EMAIL` | Remetente dos e-mails enviados. |
| `VITE_API_URL`, `VITE_BACKEND_URL` | Endereço da API usado pelo frontend; vazio em desenvolvimento para usar o proxy do Vite. |
| `DATABASE_URL`, `DATABASE_SSLMODE`, `DATABASE_CONN_MAX_AGE` | Banco de dados (vazio usa SQLite). |
| `SUPABASE_STORAGE_BUCKET`, `SUPABASE_URL`, `SUPABASE_S3_REGION`, `SUPABASE_S3_ACCESS_KEY_ID`, `SUPABASE_S3_SECRET_ACCESS_KEY` | Armazenamento de imagens. Com `SUPABASE_STORAGE_BUCKET` vazio, os arquivos ficam em `apps/backend/media` (`MEDIA_ROOT`, servidos em `/media/`). Com o bucket definido (produção, Supabase Storage com bucket público), `SUPABASE_URL`, `SUPABASE_S3_REGION`, `SUPABASE_S3_ACCESS_KEY_ID` e `SUPABASE_S3_SECRET_ACCESS_KEY` passam a ser obrigatórios, e o backend não inicia se faltar alguma. As chaves ficam só no `.env` do ambiente. |

## Contrato de categorias

- Cada produto possui uma categoria obrigatória; o MVP não usa subcategorias.
- `GET /api/v1/produtos/?categoria=<id>` filtra produtos por categoria.
- `GET /api/v1/produtos/categorias/` é público e inclui categorias inativas/sugestões; use `?ativo=true` para obter somente categorias ativas.
- Produtores autenticados podem enviar sugestões de categoria por `POST /api/v1/produtos/categorias/`; elas sempre nascem inativas.
- Somente administradores podem alterar ou ativar/inativar categorias. Categorias não podem ser excluídas.

## Operação do produtor

Os endpoints abaixo exigem JWT de um produtor com loja cadastrada. O backend sempre limita produtos e pedidos à loja do usuário autenticado.

- `GET /api/v1/produtos/meus/`: lista todos os produtos da loja, inclusive inativos.
- `POST /api/v1/produtos/` e `PATCH /api/v1/produtos/{id}/`: cadastra ou altera produtos da própria loja. Estoque negativo retorna `400` (ver [Disponibilidade por estoque](#disponibilidade-por-estoque-rn-017)).
- `POST /api/v1/produtos/precos/`: registra um novo preço vigente, encerrando automaticamente o preço anterior. Recebe `produto`, `preco_venda` e, opcionalmente, `porcentagem_desconto` entre 0 e 100. Valor zero é aceito. `preco_venda` negativo retorna `400` com `{"preco_venda": ["O preço de venda não pode ser negativo."]}`; `preco_custo` negativo retorna `400` com `{"preco_custo": ["O preço de custo não pode ser negativo."]}` (`preco_custo` nulo ou ausente é aceito).
- `GET /api/v1/pedidos/minha-loja/`: lista pedidos da loja com itens, valores, data de criação (`data_criacao`) e somente nome/telefone do cliente (`cliente: {nome, telefone}`). O `telefone` é o telefone principal atual do cliente e só vem nos pedidos `Pendente`, `Em preparo` e `Pronto para retirada`; em pedidos `Entregue` e `Cancelado`, ou se o cliente não tem telefone, vem `null` (ver [Telefones do usuário](#telefones-do-usuário-rn-021)). O mesmo vale para a resposta de `PATCH /api/v1/pedidos/{id}/status/`. Nos itens, `produto` pode vir `null` quando o produto foi excluído (ver [Vínculo do pedido com o cliente](#vínculo-do-pedido-com-o-cliente)); o snapshot do item (`nome_produto`, `quantidade`, `valor_unitario`, `valor_desconto`, `subtotal`) permanece.
- `GET /api/v1/pedidos/status-disponiveis/` e `PATCH /api/v1/pedidos/{id}/status/`: consulta e atualiza o status pelo fluxo `Pendente → Em preparo → Pronto para retirada → Entregue`, com cancelamento permitido antes da retirada.
- `PATCH /api/v1/lojas/me/`: altera apenas `nome`, `descricao`, `ativa` e `imagem_perfil`; outros campos (como `cnpj`) retornam `400`. Uma loja inativa preserva o histórico e não aceita novas compras. Detalhes da imagem em [Imagem da loja e foto de perfil](#imagem-da-loja-e-foto-de-perfil-rn-018).

Produtos não são excluídos: para tirá-los do catálogo, o produtor altera `ativo` para `false`, preservando o histórico dos pedidos.

### Criar loja (loja única por produtor, RN-013)

- Método: POST
- URL: `/api/v1/lojas/lojas/`
- Autenticação: JWT (produtor)

Payload esperado: `nome`, `descricao` e `cnpj`. O proprietário é sempre o usuário autenticado.

Resposta esperada (`201`): dados da loja, incluindo `loja_id`, `proprietario` e `ativa`.

Possíveis erros:
- 400 — `{"non_field_errors": ["Cada produtor pode possuir somente uma loja."]}` quando o produtor já possui loja. A regra é validada na API e garantida no banco pela restrição única `uq_loja_proprietario`; em requisições simultâneas, o `IntegrityError` do banco é convertido na mesma resposta `400`.
- 400 — `{"non_field_errors": ["Usuário precisa ser produtor para criar uma loja."]}` para usuário que não é produtor.
- 401 — sem autenticação.

A API não tem `DELETE` de loja nem de usuário. Como `Loja.proprietario` usa `PROTECT`, um produtor com loja não pode ser excluído, mesmo sem pedidos (no Admin do Django aparece a tela de objetos protegidos). O encerramento é feito pela desativação da loja (`ativa=false`) e pela inativação do usuário.

### Imagens do produto

Cada produto pode ter até 5 imagens (JPG, PNG ou WEBP, até 5 MB cada), com exatamente uma principal quando houver imagem. A resposta de produto traz `imagens` (lista `{ id, imagem, ordem, e_principal }` em ordem de exibição) e `imagem`, com a URL da principal ou `null`.

| Método e URL | Autenticação | Descrição |
| --- | --- | --- |
| `GET /api/v1/produtos/{id}/imagens/` | Pública | Lista as imagens de um produto visível no catálogo; o dono e administradores também veem as de produtos inativos. |
| `POST /api/v1/produtos/{id}/imagens/` | Dono ou admin | `multipart/form-data` com `imagem` e, opcionalmente, `e_principal=true`. A primeira imagem vira principal e as novas entram no fim da ordem. Retorna `201`. |
| `PATCH /api/v1/produtos/{id}/imagens/{imagem_id}/` | Dono ou admin | `{ "e_principal": true }` define a principal e desmarca a anterior. O arquivo não pode ser trocado. |
| `DELETE /api/v1/produtos/{id}/imagens/{imagem_id}/` | Dono ou admin | Exclui a imagem e remove o arquivo do storage; se era a principal, a próxima pela ordem assume. Retorna `204`. |
| `POST /api/v1/produtos/{id}/imagens/reordenar/` | Dono ou admin | `{ "imagens": [3, 1, 2] }` com todos os IDs do produto na nova ordem. Retorna a lista atualizada. |

Erros: `400` para arquivo inválido ou acima de 5 MB, sexta imagem, tentativa de trocar o arquivo, desmarcar a principal diretamente ou lista de reordenação incompleta; `401` sem autenticação; `404` quando o produto não pertence à loja do usuário ou não está visível.

No frontend, a área do produtor fica em `/minha-loja`, com as abas Painel, Pedidos, Produtos e Minha loja. Os indicadores do painel (vendas do mês, ticket médio, vendas dos últimos 7 dias e produtos mais vendidos) são calculados a partir dos pedidos não cancelados, apenas para exibição.

Na aba Produtos, a desativação é confirmada em um modal (`ModalConfirmacao.vue`) que informa que o produto sai do catálogo e que os pedidos são preservados; a reativação é imediata.

Cada produtor pode cadastrar somente uma loja. Alertas configuráveis de estoque permanecem como evolução futura.

## Imagem da loja e foto de perfil (RN-018)

Cada loja pode ter uma imagem e cada usuário (cliente ou produtor) pode ter uma foto de perfil. Ambas são opcionais e únicas. Sem imagem, a API devolve `null` e o frontend exibe um marcador (inicial do nome da loja ou iniciais do usuário).

Regras comuns:

- Formatos JPG, PNG e WEBP, de até 5 MB. O backend confere a extensão e o conteúdo do arquivo (assinatura), e salva com nome aleatório (`lojas/<uuid>.<ext>` e `usuarios/<uuid>.<ext>`).
- Mensagens de recusa (`400`, no campo da imagem): "Envie uma imagem JPG, PNG ou WEBP válida." (extensão, conteúdo, campo vazio, `null` ou valor que não é arquivo) e "A imagem deve ter no máximo 5 MB.". Quando o envio é recusado, a imagem atual é mantida.
- Enviar uma nova imagem substitui a anterior. Para remover sem enviar outra, use o `DELETE` da respectiva rota; enviar `""` ou `null` no `PATCH` retorna `400`.
- O arquivo anterior é apagado do storage somente depois que a alteração é confirmada no banco e, no caso da loja, só se nenhuma outra loja usar o mesmo arquivo. Nomes fora do padrão gerado pelo sistema (valores antigos) são exibidos como `null` e nunca são apagados.
- As imagens são devolvidas como URL absoluta. Os envios usam `multipart/form-data`.
- Armazenamento: disco local (`MEDIA_ROOT`) em desenvolvimento; Supabase Storage em produção, quando `SUPABASE_STORAGE_BUCKET` está definido (ver [Variáveis de ambiente](#variáveis-de-ambiente)).
- A imagem da loja e a foto do usuário não entram no snapshot do pedido.

### Enviar ou trocar a foto de perfil

- Método: PATCH
- URL: `/api/v1/usuarios/me/`
- Autenticação: JWT (qualquer usuário autenticado, apenas a própria conta)

Payload esperado (`multipart/form-data`; os demais campos do perfil continuam opcionais):

```text
foto_perfil=<arquivo JPG, PNG ou WEBP>
```

Resposta esperada (`200`): o perfil completo, com `foto_perfil` como URL absoluta.

```json
{ "id": 7, "nome": "Maria Souza", "foto_perfil": "http://127.0.0.1:8000/media/usuarios/3f2a9c0d5b1e4f6a8c7d2e1b0a9f8e7d.png" }
```

O exemplo mostra só alguns campos; a resposta traz também `cpf`, `email`, `telefones`, `data_nascimento`, `genero`, `is_produtor`, `tem_loja` e `idade`.

Possíveis erros:
- 400 — `{"foto_perfil": ["Envie uma imagem JPG, PNG ou WEBP válida."]}` ou `{"foto_perfil": ["A imagem deve ter no máximo 5 MB."]}`.
- 400 — campo não permitido (por exemplo `cpf`, `is_produtor`): `{"detail": "Somente nome, e-mail, data de nascimento, gênero e foto de perfil podem ser alterados no perfil. Os telefones são gerenciados em /me/telefones/."}` (inclui o envio de `telefone`).
- 401 — sem autenticação.

`foto_perfil` (URL absoluta ou `null`) também aparece, dentro de `usuario`, nas respostas de `POST /api/v1/usuarios/login/` e `POST /api/v1/usuarios/cadastro/`, e em `GET /api/v1/usuarios/me/`. O cadastro não aceita foto. A foto só é exposta ao próprio usuário: nenhuma outra rota (avaliações, pedidos, loja) a devolve.

### Remover a foto de perfil

- Método: DELETE
- URL: `/api/v1/usuarios/me/foto/`
- Autenticação: JWT (própria conta)

Resposta esperada (`204`), sem corpo.

Possíveis erros:
- 401 — sem autenticação.
- 404 — `{"detail": "Você não possui foto de perfil."}` (sem foto ou com valor antigo fora do padrão, que é preservado).

### Criar loja com imagem

- Método: POST
- URL: `/api/v1/lojas/lojas/`
- Autenticação: JWT (produtor)

Payload esperado (`multipart/form-data` ou JSON; `descricao`, `imagem_perfil` e `ativa` são opcionais, e `ativa` é `true` por padrão):

```text
nome=Loja Exemplo
descricao=Mel e derivados
cnpj=12345678000190
imagem_perfil=<arquivo JPG, PNG ou WEBP>
```

Resposta esperada (`201`): a loja criada, com `imagem_perfil` como URL absoluta ou `null`.

```json
{
  "loja_id": 1,
  "proprietario": 7,
  "proprietario_nome": "Maria Souza",
  "nome": "Loja Exemplo",
  "descricao": "Mel e derivados",
  "cnpj": "12345678000190",
  "imagem_perfil": "http://127.0.0.1:8000/media/lojas/9b1d4c7e2a5f4c3b8d6e0f1a2b3c4d5e.jpg",
  "ativa": true
}
```

Possíveis erros:
- 400 — imagem inválida ou acima de 5 MB (a loja não é criada e o produtor corrige o arquivo); usuário que não é produtor ("Usuário precisa ser produtor para criar uma loja."); produtor que já possui loja ("Cada produtor pode possuir somente uma loja."); campos obrigatórios ausentes ou CNPJ já cadastrado.
- 401 — sem autenticação.

### Consultar lojas

- Método: GET
- URL: `/api/v1/lojas/lojas/` e `/api/v1/lojas/lojas/{id}/`
- Autenticação: pública

Resposta esperada (`200`): loja(s) no mesmo formato acima, incluindo `imagem_perfil` (URL absoluta ou `null`).

`PATCH`, `PUT` e `DELETE` em `/api/v1/lojas/lojas/{id}/` retornam `405`: a loja só é alterada por `/api/v1/lojas/me/`, e não há exclusão (ver RN-019).

### Consultar e alterar a própria loja

- Método: GET | PATCH
- URL: `/api/v1/lojas/me/`
- Autenticação: JWT (produtor dono da loja)

`GET` não recebe payload e retorna a loja do usuário. Payload esperado do `PATCH` (`multipart/form-data` ou JSON; todos os campos opcionais):

```text
nome=Novo nome
descricao=Nova descrição
ativa=true
imagem_perfil=<arquivo JPG, PNG ou WEBP>
```

Resposta esperada (`200`): a loja atualizada, no formato da criação.

Possíveis erros:
- 400 — campo fora de `nome`, `descricao`, `ativa` e `imagem_perfil`: `{"detail": "Somente nome, descrição, imagem e status da loja podem ser alterados nesta área."}`
- 400 — imagem inválida, acima de 5 MB, vazia ou `null`: `{"imagem_perfil": ["..."]}` (a imagem atual é mantida).
- 401 — sem autenticação.
- 404 — `{"detail": "Você não possui uma loja cadastrada."}`

### Remover a imagem da loja

- Método: DELETE
- URL: `/api/v1/lojas/me/imagem/`
- Autenticação: JWT (produtor dono da loja)

Resposta esperada (`204`), sem corpo. A desativação da loja não apaga a imagem.

Possíveis erros:
- 401 — sem autenticação.
- 404 — `{"detail": "Você não possui uma loja cadastrada."}` ou `{"detail": "A loja não possui imagem."}`

### Limitações aceitas no v1

- Se o banco falhar depois do upload do arquivo novo, o arquivo fica órfão no storage.
- No Supabase, o bucket é público também para a foto do usuário. O nome do arquivo é um UUID e nenhum endpoint de terceiros devolve a foto, mas quem souber a URL consegue abri-la.
- Troca de imagem pelo Admin do Django não é validada nem remove o arquivo anterior. A moderação de imagens é trabalho futuro.
- Valores antigos fora do padrão gerado aparecem como `null` e permanecem no banco.
- A mensagem de extensão inválida da imagem do produto (RN-016) é diferente da usada na loja e na foto do usuário.

## Disponibilidade por estoque (RN-017)

Regras implementadas:

- Produto com estoque 0 não aparece na listagem do catálogo (`GET /api/v1/produtos/`). Ele continua acessível em `GET /api/v1/produtos/{id}/` (com `estoque: 0`), em `GET /api/v1/produtos/meus/` e na lista de favoritos. O campo `ativo` não muda por causa do estoque; quando o estoque é reposto, o produto volta ao catálogo.
- Estoque baixo: o campo `estoque_baixo` é verdadeiro quando o estoque está entre 1 e 5 unidades. O limite é único e global (`Produto.LIMITE_ESTOQUE_BAIXO = 5`). É apenas um indicador visual; não há notificação por e-mail ou push.
- O estoque não pode ser negativo. A trava equivalente no banco de dados ainda não foi implementada (pendente na tarefa DB-012 / SCRUM-99).
- Quando o estoque de um produto diminui (finalização de pedido de qualquer cliente ou `PATCH` de estoque pelo produtor), os itens desse produto em todos os carrinhos com quantidade acima do novo estoque passam a ter quantidade igual ao estoque, podendo chegar a 0, e os totais dos carrinhos são recalculados. O item e o carrinho permanecem. A reposição do estoque e o cancelamento de pedido não restauram a quantidade anterior. O ajuste fica em `apps/backend/agrostore/carrinhos/services.py` (`ajustar_carrinhos_ao_estoque`).

### Listar produtos do catálogo

- Método: GET
- URL: `/api/v1/produtos/`
- Autenticação: pública

Resposta esperada (`200`), lista de produtos ativos, de lojas ativas e com estoque maior que zero (aceita `?categoria=<id>`):

```json
[
  {
    "produto_id": 12,
    "nome": "Mel de laranjeira",
    "estoque": 4,
    "estoque_baixo": true,
    "ativo": true
  }
]
```

O exemplo mostra apenas os campos relacionados a estoque; a resposta traz também `loja`, `loja_nome`, `descricao`, `categoria`, `categoria_nome`, `codigo_barras`, `sku`, `preco`, `preco_original`, `desconto`, `imagem` e `imagens`.

Possíveis erros:
- 400 — `categoria` não numérico.

`estoque_baixo` (booleano, somente leitura) também aparece em `GET /api/v1/produtos/{id}/`, `GET /api/v1/produtos/meus/`, nas respostas de `POST` e `PATCH` de produto e em `dados_produto` de `GET /api/v1/favoritos/`.

### Cadastrar ou alterar produto (estoque)

- Método: POST | PATCH
- URL: `/api/v1/produtos/` e `/api/v1/produtos/{id}/`
- Autenticação: JWT (produtor dono da loja ou administrador)

Payload esperado (parcial, apenas o campo de estoque):

```json
{ "estoque": 10 }
```

Resposta esperada: `201` (POST) ou `200` (PATCH), com o produto incluindo `estoque` e `estoque_baixo`. Um `PATCH` que informa `estoque` aciona o ajuste automático dos carrinhos.

Possíveis erros:
- 400 — estoque negativo: `{"estoque": ["O estoque não pode ser negativo."]}`
- 401 — sem autenticação.
- 403 — usuário que não é produtor (POST) ou produtor sem loja cadastrada.
- 404 — produto de outra loja (PATCH).

### Consultar carrinhos

- Método: GET
- URL: `/api/v1/carrinhos/`
- Autenticação: JWT (cliente)

Resposta esperada (`200`): lista de carrinhos do usuário, um por loja, cada um com `itens`.

```json
[
  {
    "carrinho_id": 3,
    "loja": 1,
    "loja_nome": "Loja Exemplo",
    "valor_bruto": "20.00",
    "valor_desconto": "0.00",
    "valor_liquido": "20.00",
    "itens": [
      {
        "carrinho_produto_id": 7,
        "carrinho": 3,
        "produto": 12,
        "produto_nome": "Mel de laranjeira",
        "loja": 1,
        "loja_nome": "Loja Exemplo",
        "valor_unitario": "10.00",
        "valor_desconto": "0.00",
        "quantidade": 2,
        "estoque": 2,
        "disponivel": true,
        "subtotal": "20.00"
      }
    ]
  }
]
```

Campos novos do item (somente leitura): `estoque` (inteiro, estoque atual do produto) e `disponivel` (booleano: produto ativo, loja ativa e estoque maior que zero). O campo `disponivel` não considera a quantidade do item: um item com `quantidade: 0` e `disponivel: true` indica produto reposto, mas ainda sem quantidade. `quantidade` pode ser 0 por causa do ajuste automático; nesse caso o `subtotal` é 0.

Possíveis erros:
- 401 — sem autenticação.

O campo `loja` do carrinho é somente leitura. A rota `/api/v1/carrinhos/{id}/` aceita apenas `GET` (detalhe, somente do dono do carrinho); `PUT`, `PATCH` e `DELETE` nela respondem `405`. A alteração de quantidade e a remoção de itens são feitas pelas rotas `/api/v1/carrinhos/itens/{id}/`.

### Adicionar produto ao carrinho

- Método: POST
- URL: `/api/v1/carrinhos/`
- Autenticação: JWT (cliente)

Payload esperado:

```json
{ "produto": 12, "quantidade": 1 }
```

Resposta esperada (`201`): o item do carrinho, no mesmo formato de `itens[]` acima, com `estoque` e `disponivel`. Produto repetido soma a quantidade ao item existente.

Possíveis erros:
- 400 — produto ou loja inativa, quantidade menor que 1, ou `{"detail": "Produto sem estoque suficiente para a quantidade solicitada."}` quando a soma ultrapassa o estoque.
- 401 — sem autenticação.

### Alterar quantidade de um item do carrinho

- Método: PATCH
- URL: `/api/v1/carrinhos/itens/{id}/`
- Autenticação: JWT (cliente dono do carrinho)

Payload esperado:

```json
{ "quantidade": 2 }
```

Resposta esperada (`200`): o item atualizado, com `estoque` e `disponivel`. O cliente só pode definir quantidade de 1 até o estoque; a quantidade 0 é aplicada apenas pelo ajuste automático.

Possíveis erros:
- 400 — quantidade menor que 1, ou `{"detail": "Produto sem estoque suficiente para a quantidade solicitada."}`.
- 401 — sem autenticação.
- 404 — item inexistente ou de outro usuário.

`DELETE /api/v1/carrinhos/itens/{id}/` remove o item (`204`) e apaga o carrinho quando ele fica vazio.

### Finalizar carrinho (criar pedidos)

- Método: POST
- URL: `/api/v1/pedidos/`
- Autenticação: JWT (cliente)

Payload esperado: os identificadores dos itens do carrinho selecionados; apenas eles são finalizados.

```json
{ "carrinho_produto_ids": [7, 8] }
```

Resposta esperada (`201`): lista de pedidos criados, um por loja. Os produtos são travados durante a validação e a baixa de estoque, os itens finalizados saem do carrinho e os carrinhos de outros clientes afetados pela baixa são ajustados.

Possíveis erros (nenhum pedido é criado em caso de erro):
- 400 — item com quantidade 0: `{"detail": "O produto <nome> está sem estoque. Remova-o da seleção para finalizar."}`
- 400 — `{"detail": "O produto <nome> não possui estoque suficiente."}`
- 400 — `{"detail": "O produto <nome> não pertence à loja do carrinho."}` (a finalização inteira é recusada, sem criar pedidos nem baixar estoque).
- 400 — produto inativo, loja inativa, produto sem preço vigente ou item inválido (`"Um ou mais itens do carrinho são inválidos."`).
- 401 — sem autenticação.

### Comportamento no frontend

- Carrinho (`CarrinhoView.vue`): cada item exibe uma situação — "Sem estoque" (produto indisponível e sem estoque), "Disponível novamente" (quantidade 0 com produto de volta ao estoque; o cliente deve aumentar a quantidade) e "Indisponível" (produto ou loja inativa com estoque). Itens com essas situações não podem ser selecionados para finalizar.
- Área do produtor (`/minha-loja/produtos`): selos "Estoque baixo" e "Sem estoque — fora do catálogo" por produto, e um aviso resumido que conta somente os produtos ativos.

## Retirada na feira

A retirada dos pedidos é presencial, em um dia e horário únicos para toda a plataforma (não varia por loja/produtor):

- Todos os sábados, das 6h às 12h.
- Rua Major Lúcio Meireles, nº 61, Centro, Camaquã (junto ao prédio nos fundos da Igreja Imaculada / escritório da Emater).

Essa informação é exibida ao cliente no carrinho e nos pedidos (`apps/frontend/src/data/feira.js`) apenas para orientação.

## Cancelamento de pedidos

O cliente autenticado pode cancelar somente seus próprios pedidos com status `Pendente`.

- `PATCH /api/v1/pedidos/{id}/cancelar/`: não recebe payload e retorna o pedido atualizado com status `Cancelado`.
- Retorna `400` se o pedido não estiver pendente e `404` se o pedido não pertencer ao cliente autenticado.
- O cancelamento preserva o pedido no histórico e restaura o estoque de seus itens. Cancelamentos permitidos pelo produtor também restauram o estoque.

## Confirmação de recebimento (RN-022)

O comprador dono do pedido (qualquer usuário que compre, inclusive um produtor em pedido feito em outra loja) confirma o recebimento somente de pedidos `Pronto para retirada`. O pedido passa para `Entregue`. O produtor (ou o administrador) continua podendo marcar `Entregue` pelo quadro de pedidos (`PATCH /api/v1/pedidos/{id}/status/`).

### Confirmar recebimento do pedido

- Método: PATCH
- URL: /api/v1/pedidos/{id}/confirmar-entrega/
- Autenticação: JWT (dono do pedido)

Payload esperado: nenhum (sem corpo).

Resposta esperada (`200`): o pedido atualizado, no mesmo formato de `PATCH /api/v1/pedidos/{id}/cancelar/`, com status `Entregue`.

Possíveis erros:
- 400 — `{"detail": "Somente pedidos prontos para retirada podem ter o recebimento confirmado."}`, quando o status não é `Pronto para retirada`.
- 401 — sem autenticação.
- 404 — pedido inexistente ou de outro usuário.

Comportamento:
- A confirmação não altera o estoque (a baixa ocorre na finalização) e não pode ser desfeita: `Entregue` é um status final.
- Depois da confirmação, os itens podem ser avaliados (RN-010) e o produtor deixa de ver o telefone do cliente (RN-021).
- O sistema não registra quem confirmou a entrega (cliente ou produtor).
- Frontend: em "Meus pedidos" (`PedidosView.vue`), o botão "Confirmar recebimento" aparece nos pedidos `Pronto para retirada` e abre uma janela de confirmação; depois de confirmar, os botões "Avaliar" ficam disponíveis.

## Vínculo do pedido com o cliente

O dono de um pedido é identificado pelo registro `PedidoCliente` (tabela `pedidos_pedidocliente`, relação um-para-um com `Pedido`, acessível por `pedido.cliente`). A tabela `Pedido` não possui mais o campo `usuario`.

- `PedidoCliente.usuario` é uma chave estrangeira obrigatória para o usuário (`related_name='pedidos_cliente'`) e convive com o snapshot do cliente no momento da compra: nome, CPF, e-mail, data de nascimento e gênero. O telefone não faz parte do snapshot (RN-021): o produtor vê o telefone principal atual do cliente nos pedidos em aberto.
- No checkout (`POST /api/v1/pedidos/`), o `PedidoCliente` é criado logo após o `Pedido`, na mesma transação. Se qualquer etapa falhar, nada é gravado.
- "Meus pedidos", detalhe e cancelamento filtram por `cliente__usuario`; a avaliação de produto confere a titularidade do pedido pelo mesmo caminho. O produtor continua filtrado por `loja__proprietario`.
- O contrato JSON da API não mudou: nenhum payload expõe `usuario`.
- Exclusão bloqueada: `PedidoCliente.usuario` e `Pedido.loja` usam `PROTECT`. Não é possível excluir um usuário que tenha pedidos como cliente, nem uma loja que tenha pedidos; o Django lança `ProtectedError` (no Admin, a exclusão é recusada com a lista dos pedidos). Isso preserva o histórico de pedidos. Para retirar o acesso, desative o usuário ou a loja.
- Item do pedido (DB-015): `PedidoProduto.produto` é opcional e usa `SET_NULL`. Se o produto for excluído, o vínculo do item fica nulo e o snapshot (`nome_produto`, `quantidade`, `valor_unitario`, `valor_desconto`, `subtotal`) é preservado. Por isso, nos itens de `GET /api/v1/pedidos/`, `GET /api/v1/pedidos/minha-loja/` e nas respostas de `PATCH /api/v1/pedidos/{id}/status/` e `PATCH /api/v1/pedidos/{id}/cancelar/`, o campo `produto` pode vir `null`. Novas restrições no banco: `quantidade > 0` e `valor_unitario`, `valor_desconto` e `subtotal >= 0`. A API continua sem exclusão de produto (somente desativação).
- Avaliação (DB-015): `Avaliacao.produto` também é opcional e usa `SET_NULL`. A avaliação continua ligada ao item do pedido (uma por item) e visível em "Meus pedidos", mas deixa de aparecer na listagem por produto. As chaves `usuario` e `pedido_produto` de `Avaliacao` ainda usam `CASCADE`; avaliações só saem por moderação no Admin.
- `Loja.proprietario` também usa `PROTECT` e é único (`uq_loja_proprietario`): não é possível excluir um produtor que tenha loja, tenha ela pedidos ou não, e a loja nunca é apagada em cascata com o usuário.

## Banco de dados e migrations

O banco é definido por `DATABASE_URL`. Com a variável vazia, o backend usa SQLite local; com `postgresql://...`, usa PostgreSQL (Supabase em produção). O modelo lógico está em `docs/modelo-logico.sql`.

> **Alerta:** o `.env` da raiz pode conter um `DATABASE_URL` apontando para o Supabase. Rodar `migrate` com essa variável preenchida aplica as migrations **em produção**. No desenvolvimento, execute os comandos com `DATABASE_URL=` vazio (use o `.env.example` como base; ele traz a variável vazia).

### Migration de loja única por produtor (lojas 0003)

`lojas/0003_loja_proprietario_unico_protect` altera `Loja.proprietario` para `on_delete=PROTECT` e cria a restrição única `uq_loja_proprietario`. Ela tem uma guarda que **interrompe** a migration se algum produtor tiver mais de uma loja. Já está aplicada no Supabase.

No SQLite local de desenvolvimento, se o `migrate` parar nessa guarda, o banco tem produtores com duas ou mais lojas. Sane o banco deixando uma loja por produtor (por exemplo, pelo Admin ou `manage.py shell`, preservando a loja que tem pedidos) ou recrie o `db.sqlite3` (apague o arquivo e rode `migrate`), e então rode `migrate` novamente.

### Migrations do vínculo do cliente (pedidos 0003 a 0005)

Movem o usuário de `Pedido` para `PedidoCliente`, em três migrations separadas e reversíveis:

1. `0003_pedidocliente_usuario` (schema): adiciona `PedidoCliente.usuario` como campo nulo.
2. `0004_copiar_usuario_para_pedidocliente` (dados): copia o usuário de cada pedido e **interrompe** se existir pedido sem `pedido_cliente`. Tem operação reversa.
3. `0005_remover_pedido_usuario` (schema): torna `PedidoCliente.usuario` obrigatório e remove `Pedido.usuario`.

Elas ficam separadas por compatibilidade com PostgreSQL: misturar alteração de dados e de schema na mesma transação causa o erro "pending trigger events".

### Migrations dos telefones (usuarios 0006 a 0008 e pedidos 0006)

Criam `tipo_telefone` e `telefone`, copiam o antigo `Usuario.telefone` e removem os campos antigos (RN-021):

1. `usuarios` 0006 (schema): cria `tipo_telefone` e `telefone`.
2. `usuarios` 0007 (dados): popula os tipos e copia o telefone de cada usuário como principal.
3. `usuarios` 0008 (schema): remove `Usuario.telefone`.
4. `pedidos` 0006 (schema): remove `PedidoCliente.telefone`.

> **Atenção antes de aplicar no Supabase:** faça backup antes. A remoção do telefone do snapshot dos pedidos (`pedidos` 0006) é irreversível, pois os dados não são recuperáveis ao reverter. Publique o backend junto com o frontend novo, pois o frontend antigo depende de `telefone` no cadastro, no perfil e nos pedidos. Após aplicar, rode `telefones_fora_do_padrao` (ver [Telefones do usuário](#telefones-do-usuário-rn-021)). Estas migrations ainda não foram aplicadas no Supabase.

### Procedimento para aplicar no Supabase

Estado: **aplicado no Supabase até `lojas` 0003 e `usuarios` 0005**. Conferências com `showmigrations`:

- 15/10/2026: todas as migrations existentes na época aplicadas, incluindo `pedidos` 0001 a 0005 (os 7 registros de `pedidos_pedidocliente` com `usuario_id` preenchido) e `lojas` 0003.
- 16/10/2026: conferido com `node scripts/backend.mjs showmigrations`; sem migration pendente na época (inclui `usuarios` 0005).

**Pendentes de aplicação** na branch integrada (exigem autorização e backup): `usuarios` 0006 a 0008 (telefones), `pedidos` 0006 (irreversível, remove o telefone do snapshot) e `pedidos` 0007 (item do pedido com produto opcional e `SET_NULL`, DB-015), e `avaliacoes` 0002 (avaliação com produto opcional e `SET_NULL`, DB-015).

O procedimento abaixo vale como referência para essas aplicações e para as futuras.

1. Faça backup (`pg_dump` ou painel do Supabase).
2. Rode as consultas somente leitura:
   ```sql
   SELECT app, name FROM django_migrations WHERE app IN ('pedidos','lojas','usuarios','produtos') ORDER BY app, id;

   SELECT COUNT(*) FROM pedidos_pedido p
   LEFT JOIN pedidos_pedidocliente pc ON pc.pedido_id = p.pedido_id
   WHERE pc.pedido_cliente_id IS NULL;
   ```
   A segunda consulta deve retornar `0`; caso contrário, a migration 0004 será interrompida e os pedidos órfãos devem ser tratados antes.
3. Pare o backend publicado.
4. Aplique um app por vez, rodando `--plan` antes de cada um: primeiro as pendentes de `lojas`, `usuarios` e `produtos`; `pedidos` por último.
   ```powershell
   node scripts/backend.mjs migrate lojas --plan
   node scripts/backend.mjs migrate lojas
   # repita para usuarios e produtos; por fim:
   node scripts/backend.mjs migrate pedidos --plan
   node scripts/backend.mjs migrate pedidos
   ```
5. Publique o código novo junto com a migration, pois o código antigo depende de `Pedido.usuario`.

## SKU de produtos

O backend gera automaticamente o SKU de produtos novos e não aceita alteração manual. O valor tem 14 dígitos, sem separadores, na ordem `id_loja` (4 dígitos), `id_categoria` (4 dígitos) e `id_produto` (6 dígitos). Por exemplo, os identificadores `1`, `1` e `1` resultam em `00010001000001`. Produtos cadastrados antes desta regra mantêm seus SKUs atuais.

## Cadastro de clientes

### `POST /api/v1/usuarios/cadastro/`

Público. Cria uma conta de cliente e retorna `access`, `refresh` e um objeto seguro em `usuario`.

```json
{
  "nome": "Nome do cliente",
  "cpf": "52998224725",
  "email": "cliente@exemplo.com",
  "telefone": "51999990000",
  "tipo_telefone": 1,
  "data_nascimento": "2000-05-10",
  "genero": "M",
  "password": "SenhaForte123",
  "password_confirmacao": "SenhaForte123"
}
```

`tipo_telefone` é o `id` de um tipo retornado por `GET /api/v1/tipos-telefone/`. O telefone informado vira o telefone principal da conta. A resposta traz `usuario.telefones` (lista com `id`, `numero`, `tipo`, `tipo_descricao` e `e_principal`); o campo `usuario.telefone` não existe mais.

Valida CPF, unicidade de CPF/e-mail, telefone conforme o tipo (ver [Telefones do usuário](#telefones-do-usuário-rn-021)), idade mínima de 16 anos e senha de ao menos oito caracteres. Retorna `400` para dados inválidos ou duplicados, por exemplo `{"telefone": ["Celular deve ter 11 dígitos com DDD."]}` ou `{"tipo_telefone": ["Informe um tipo de telefone válido."]}`.

## Redefinição de senha (RN-020)

O usuário que esqueceu a senha pede um link por e-mail e cadastra uma nova senha. Os dois endpoints são públicos (sem JWT) e limitados por IP.

Fluxo:

1. Em `/login`, o usuário abre "Esqueci minha senha" (`/esqueci-senha`) e informa o e-mail.
2. A API responde sempre com a mesma mensagem, exista ou não conta com o e-mail. Só há envio quando existe exatamente uma conta ativa com aquele e-mail (comparação sem diferenciar maiúsculas).
3. O e-mail traz o link `FRONTEND_URL/redefinir-senha#token=<código>`. O código vai no fragmento (`#`), que o navegador não envia ao servidor. A tela `/redefinir-senha` lê o código e o remove da URL e do histórico (`router.replace`); recarregar a página depois disso exige um novo link.
4. O usuário informa a nova senha e a confirmação. A API confirma, e o frontend leva ao login com a mensagem de sucesso. Não há login automático; se existir sessão aberta no navegador, o frontend a encerra.

Regras implementadas:

- Código aleatório (`secrets.token_urlsafe`); o banco guarda apenas o hash SHA-256 (tabela `usuarios_redefinicaosenha`, migration `usuarios` 0005), nunca o código.
- Cada link vale 30 minutos e pode ser usado uma única vez (`data_utilizacao` é preenchida).
- Pedir um novo link marca como usados os links pendentes anteriores. Ao concluir a troca, os demais links pendentes também são invalidados.
- Link inexistente, expirado, usado ou de conta inativa retorna sempre a mesma mensagem de erro.
- A nova senha segue as validações do cadastro (mínimo de 8 caracteres, validadores de senha do Django, confirmação igual).
- Limite por IP (DRF `ScopedRateThrottle`): 5 solicitações por hora e 10 confirmações por hora, com `429` e a mensagem "Muitas solicitações. Tente novamente mais tarde.".
- Os JWT emitidos antes da troca continuam válidos até expirarem (decisão v1).

### Solicitar link de redefinição

- Método: POST
- URL: `/api/v1/usuarios/redefinir-senha/`
- Autenticação: pública

Payload esperado:

```json
{ "email": "cliente@exemplo.com" }
```

Resposta esperada (`200`), igual para e-mail existente, inexistente ou de conta inativa:

```json
{ "detail": "Se houver uma conta com este e-mail, enviaremos um link para redefinir a senha." }
```

Possíveis erros:
- 400 — `email` ausente ou com formato inválido (`{"email": ["..."]}`).
- 429 — limite de 5 solicitações por hora por IP: `{"detail": "Muitas solicitações. Tente novamente mais tarde."}`

### Confirmar nova senha

- Método: POST
- URL: `/api/v1/usuarios/redefinir-senha/confirmar/`
- Autenticação: pública

Payload esperado:

```json
{
  "token": "<código recebido no link>",
  "password": "NovaSenhaForte123",
  "password_confirmacao": "NovaSenhaForte123"
}
```

Resposta esperada (`200`):

```json
{ "detail": "Senha redefinida. Entre com a nova senha." }
```

Possíveis erros:
- 400 — link inválido, expirado, já usado, invalidado, inexistente ou de conta inativa: `{"detail": "Este link de redefinição é inválido ou expirou. Solicite um novo."}`
- 400 — campo ausente ou fora do formato (`token`, `password` com menos de 8 caracteres, `password_confirmacao`), no formato `{"campo": ["..."]}`.
- 400 — com link válido: confirmação diferente (`{"password_confirmacao": ["As senhas não coincidem."]}`) ou senha recusada pelos validadores (`{"password": ["..."]}`).
- 429 — limite de 10 confirmações por hora por IP: `{"detail": "Muitas solicitações. Tente novamente mais tarde."}`

### E-mail em desenvolvimento e produção

O envio usa `send_mail` do Django, configurado pelas variáveis `EMAIL_*` e `DEFAULT_FROM_EMAIL` (ver [Variáveis de ambiente](#variáveis-de-ambiente)).

- Desenvolvimento: com o backend `console` (padrão do `.env.example`), o e-mail com o link aparece no terminal do backend.
- Produção: use `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend` e informe `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` e `EMAIL_USE_TLS`. Recomenda-se uma conta própria do projeto (Gmail com senha de app, Mailtrap ou Brevo). As credenciais ficam somente no `.env` do ambiente, nunca no repositório.
- Falhas de SMTP não alteram a resposta da API (continua `200`) e são registradas no log do backend sem o endereço de e-mail nem o código.

### Limitações aceitas no v1

- O envio SMTP é síncrono, dentro da requisição. A solicitação de uma conta existente pode demorar mais que a de um e-mail inexistente (diferença de tempo de resposta), e um SMTP lento prende a requisição por até `EMAIL_TIMEOUT` segundos. O envio assíncrono está previsto como tarefa futura (SCRUM-129).
- O limite por IP usa o cache em memória do Django, por processo: com mais de um processo do backend, cada um conta separadamente, e o contador zera ao reiniciar. Atrás de proxy reverso, defina `DRF_NUM_PROXIES`.
- Sessões já abertas (JWT emitidos antes da troca) não são encerradas na redefinição.
- Não há limpeza periódica dos registros expirados ou usados, nem e-mail de aviso "senha alterada".

## Perfil do usuário

- `GET /api/v1/usuarios/me/`: retorna os dados do usuário autenticado, incluindo `foto_perfil` (URL absoluta ou `null`), `telefones` (principal primeiro; `[]` em conta legada sem telefone), `is_produtor`, `tem_loja` e `idade`.
- `PATCH /api/v1/usuarios/me/`: altera `nome`, `email`, `data_nascimento`, `genero` e `foto_perfil` (ver [Imagem da loja e foto de perfil](#imagem-da-loja-e-foto-de-perfil-rn-018)), com as mesmas validações do cadastro (e-mail único e idade mínima de 16 anos). CPF, telefone e papéis (`is_produtor`, `is_staff`) não podem ser alterados por aqui e retornam `400`. Os telefones são gerenciados em `/api/v1/usuarios/me/telefones/` (ver [Telefones do usuário](#telefones-do-usuário-rn-021)).
- Pedidos já realizados mantêm o snapshot dos dados do cliente (nome, CPF, e-mail, data de nascimento e gênero); alterar o perfil não muda o histórico. O telefone é exceção (RN-021): não é copiado para o pedido.

## Telefones do usuário (RN-021)

Cada usuário (cliente ou produtor) tem um ou mais telefones, cada um com um tipo. Tabelas `tipo_telefone` (`descricao`: Celular, Fixo, Comercial) e `telefone` (usuário 0..n, `numero` como texto só com dígitos, `e_principal`). Os campos `Usuario.telefone` e `PedidoCliente.telefone` foram removidos.

Regras implementadas:

- Validação no backend pela quantidade de dígitos, com DDD: Celular 11, Fixo 10, Comercial 10 ou 11. Ao trocar o tipo, o número é validado de novo. Não há limite de telefones nem unicidade (o mesmo número pode estar em usuários diferentes). DDD e nono dígito não são validados.
- Exatamente um telefone principal por usuário. Definir outro como principal desmarca o anterior. O último telefone não pode ser excluído; para excluir o principal, defina antes outro como principal.
- Exceção legada: contas antigas sem telefone e criadas por `createsuperuser` podem ter 0 telefones. O primeiro telefone cadastrado vira o principal automaticamente, e a falta de telefone não bloqueia login nem compra.
- Admin do Django: os telefones são editados somente como inline do usuário (mínimo de 1, exatamente 1 principal).
- Pedidos: o telefone não entra no snapshot. Para o produtor, `cliente.telefone` é o telefone principal atual do cliente nos pedidos `Pendente`, `Em preparo` e `Pronto para retirada`; nos demais, ou sem telefone, é `null`. Nas respostas de pedidos do cliente, `cliente` não traz `telefone`.

### Listar tipos de telefone

- Método: GET
- URL: `/api/v1/tipos-telefone/`
- Autenticação: pública (somente leitura)

Resposta esperada (`200`):

```json
[
  { "id": 1, "descricao": "Celular" },
  { "id": 2, "descricao": "Fixo" },
  { "id": 3, "descricao": "Comercial" }
]
```

### Listar telefones

- Método: GET
- URL: `/api/v1/usuarios/me/telefones/`
- Autenticação: JWT (qualquer usuário autenticado, apenas os próprios telefones)

Resposta esperada (`200`), principal primeiro:

```json
[
  { "id": 4, "numero": "51999990000", "tipo": 1, "tipo_descricao": "Celular", "e_principal": true },
  { "id": 5, "numero": "5133330000", "tipo": 2, "tipo_descricao": "Fixo", "e_principal": false }
]
```

Possíveis erros:
- 401 — sem autenticação.

### Adicionar telefone

- Método: POST
- URL: `/api/v1/usuarios/me/telefones/`
- Autenticação: JWT (própria conta)

Payload esperado (`e_principal` é opcional; o primeiro telefone da conta vira principal automaticamente):

```json
{ "numero": "5133330000", "tipo": 2, "e_principal": false }
```

Resposta esperada (`201`): o telefone criado, no mesmo formato da listagem.

Possíveis erros:
- 400 — número inválido para o tipo: `{"numero": ["..."]}`.
- 400 — tipo inexistente: `{"tipo": ["Informe um tipo de telefone válido."]}`.
- 401 — sem autenticação.

### Ver, editar e excluir telefone

- Método: GET | PATCH | DELETE
- URL: `/api/v1/usuarios/me/telefones/{id}/`
- Autenticação: JWT (própria conta)

Payload esperado do `PATCH` (todos opcionais): `numero`, `tipo` e `e_principal`. Enviar `e_principal: true` define o telefone como principal e desmarca os outros; trocar o `tipo` revalida o número.

```json
{ "e_principal": true }
```

Resposta esperada: `GET` e `PATCH` retornam `200` com o telefone; `DELETE` retorna `204`, sem corpo. `PUT` retorna `405`.

Possíveis erros:
- 400 — número inválido para o tipo: `{"numero": ["..."]}`.
- 400 — tipo inexistente: `{"tipo": ["Informe um tipo de telefone válido."]}`.
- 400 — tentativa de desmarcar o principal: `{"e_principal": ["Defina outro telefone como principal."]}`.
- 400 — exclusão do único telefone: `{"detail": "Você precisa manter ao menos um telefone."}`.
- 400 — exclusão do principal havendo outros: `{"detail": "Defina outro telefone como principal antes de excluir este."}`.
- 401 — sem autenticação.
- 404 — telefone inexistente ou de outro usuário.
- 405 — `PUT`.

### Telefones fora do padrão (migração)

Na migração, o antigo `Usuario.telefone` foi copiado como telefone principal: 11 dígitos viram Celular, 10 viram Fixo, e valor fora do padrão entra como Celular. Valor vazio não gera telefone. O telefone do snapshot dos pedidos não é aproveitado. Para listar os casos a corrigir (somente leitura; mostra apenas os ids, nunca o número):

```powershell
node scripts/backend.mjs telefones_fora_do_padrao
```

## Favoritos

Os favoritos são privados e exigem JWT. Cada usuário pode favoritar um produto somente uma vez; produtores também podem usar a funcionalidade.

- `GET /api/v1/favoritos/`: lista somente os favoritos do usuário autenticado, do mais recente ao mais antigo. Cada item inclui `favorito_id`, `data_criacao` e `dados_produto` com as informações completas para exibição, incluindo preço, categoria, loja, estoque, status e disponibilidade.
- `POST /api/v1/favoritos/`: adiciona um produto aos favoritos. Recebe `{"produto": <produto_id>}` e retorna o favorito criado. Retorna `400` se o produto já estiver favoritado.
- `DELETE /api/v1/favoritos/{favorito_id}/`: remove um favorito do próprio usuário e retorna `204`. Não permite remover favoritos de outra conta.

Produtos favoritos inativos, sem estoque ou com a loja desativada continuam visíveis na lista, identificados como indisponíveis e sem opção de adicionar ao carrinho.

## Avaliações (RN-010)

Somente o dono de um pedido `Entregue` avalia seus itens, uma vez por item. A avaliação não pode ser editada nem removida pela API: não há `PUT`, `PATCH` nem `DELETE` em `/api/v1/avaliacoes/`.

### Criar avaliação

- Método: POST
- URL: `/api/v1/avaliacoes/`
- Autenticação: JWT (qualquer usuário autenticado, dono do pedido)

Payload esperado (`comentario` é opcional, até 500 caracteres; `nota` é inteira de 1 a 5):

```json
{ "pedido_produto": 15, "nota": 5, "comentario": "Mel excelente." }
```

Resposta esperada (`201`): produto e usuário são vinculados pelo backend.

```json
{
  "avaliacao_id": 4,
  "pedido_produto": 15,
  "produto": 12,
  "produto_nome": "Mel de laranjeira",
  "usuario_nome": "Maria S.",
  "nota": 5,
  "comentario": "Mel excelente."
}
```

Possíveis erros (`400`, na ordem das validações do `pedido_produto`):
- "Este item não pertence ao seu pedido." (também quando o id não existe)
- "Só é possível avaliar pedidos entregues."
- "Este produto não está mais disponível para avaliação." (o produto do item foi excluído; formato `{"pedido_produto": ["Este produto não está mais disponível para avaliação."]}`)
- "Este item já foi avaliado."
- "O comentário deve ter no máximo 500 caracteres."
- 400 — nota fora de 1 a 5 ou ausente (mensagens padrão do DRF).
- 401 — sem autenticação.

### Listar avaliações

- Método: GET
- URL: `/api/v1/avaliacoes/?produto=<id>`
- Autenticação: pública

Resposta esperada (`200`): lista no mesmo formato acima. `usuario_nome` é abreviado (primeiro nome e inicial do último sobrenome, como "Maria S."); o nome completo não é exposto. Avaliações de produto ou loja inativos continuam listadas. Sem `produto`, retorna todas as avaliações. Se o produto foi excluído, `produto` vem `null` e `produto_nome` vem do nome guardado no item do pedido; essas avaliações não aparecem em `?produto=<id>`, mas seguem visíveis em "Meus pedidos".

### Campo `avaliacao` nos itens de pedido

Cada item de pedido traz o campo somente leitura `avaliacao`, que vale `null` (item ainda não avaliado) ou `{ "avaliacao_id": 4, "nota": 5, "comentario": "..." }`. Aparece nos itens de `GET /api/v1/pedidos/`, `GET /api/v1/pedidos/{id}/`, `GET /api/v1/pedidos/minha-loja/` e nas respostas de `PATCH /api/v1/pedidos/{id}/status/`, `PATCH /api/v1/pedidos/{id}/cancelar/` e `POST /api/v1/pedidos/` (checkout).

### Moderação e exclusões no Admin do Django

- Pedidos (e seus itens, cliente e status) ficam somente para consulta: sem incluir, editar ou excluir, inclusive o status. A troca de status é feita pela API (RN-019).
- Avaliações são moderadas apenas por exclusão (não há inclusão nem edição). Após a exclusão, o item de pedido pode ser avaliado de novo.
- Usuário ou loja com pedidos não podem ser excluídos; usa-se a desativação.
- Produtor com loja não pode ser excluído, mesmo sem pedidos (RN-013); o Admin exibe os objetos protegidos. Encerre pela desativação da loja e pela inativação do usuário.

## Idioma e notificações

- O backend usa português do Brasil (`pt-br`) para mensagens nativas de validação do Django.
- O frontend possui notificações globais de `success`, `info`, `warning` e `danger`; sem tempo informado, permanecem até fechamento manual ou atualização da página.
