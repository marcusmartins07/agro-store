# Agro Store

Monorepo com API Django e aplicação web Vue.

## Funcionalidades principais

- Catálogo público de produtos com filtro por categoria e imagens por produto (até 5, com uma principal).
- Controle de disponibilidade por estoque: produto com estoque 0 sai da listagem do catálogo (o detalhe continua acessível, com a compra bloqueada) e volta quando o estoque é reposto. Detalhes em [Disponibilidade por estoque](#disponibilidade-por-estoque-rn-017).
- Indicador de estoque baixo (1 a 5 unidades) na área do produtor.
- Carrinho salvo no backend, com ajuste automático da quantidade quando o estoque diminui.
- Finalização do carrinho com um pedido por loja, baixa de estoque e snapshot de cliente e produtos.
- Cancelamento de pedidos pendentes pelo cliente, com restauração do estoque.
- Avaliação de produtos comprados: na tela "Meus pedidos" (`/pedidos`), o cliente avalia cada item de pedido entregue (nota de 1 a 5 e comentário opcional). A rota antiga `/avaliacoes/:id` redireciona para `/pedidos`. Detalhes em [Avaliações](#avaliações-rn-010).
- Favoritos, perfil do usuário e cadastro de clientes.
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
python apps/backend/manage.py migrate
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
- `POST /api/v1/produtos/precos/`: registra um novo preço vigente, encerrando automaticamente o preço anterior. Recebe `produto`, `preco_venda` e, opcionalmente, `porcentagem_desconto` entre 0 e 100.
- `GET /api/v1/pedidos/minha-loja/`: lista pedidos da loja com itens, valores, data de criação (`data_criacao`) e somente nome/telefone do cliente.
- `GET /api/v1/pedidos/status-disponiveis/` e `PATCH /api/v1/pedidos/{id}/status/`: consulta e atualiza o status pelo fluxo `Pendente → Em preparo → Pronto para retirada → Entregue`, com cancelamento permitido antes da retirada.
- `PATCH /api/v1/lojas/me/`: altera apenas `nome`, `descricao` e `ativa`; outros campos (como `cnpj`) retornam `400`. Uma loja inativa preserva o histórico e não aceita novas compras.

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

Cada produtor pode cadastrar somente uma loja. Imagem de loja e alertas configuráveis de estoque permanecem como evoluções futuras.

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

## Vínculo do pedido com o cliente

O dono de um pedido é identificado pelo registro `PedidoCliente` (tabela `pedidos_pedidocliente`, relação um-para-um com `Pedido`, acessível por `pedido.cliente`). A tabela `Pedido` não possui mais o campo `usuario`.

- `PedidoCliente.usuario` é uma chave estrangeira obrigatória para o usuário (`related_name='pedidos_cliente'`) e convive com o snapshot do cliente no momento da compra: nome, CPF, e-mail, telefone, data de nascimento e gênero.
- No checkout (`POST /api/v1/pedidos/`), o `PedidoCliente` é criado logo após o `Pedido`, na mesma transação. Se qualquer etapa falhar, nada é gravado.
- "Meus pedidos", detalhe e cancelamento filtram por `cliente__usuario`; a avaliação de produto confere a titularidade do pedido pelo mesmo caminho. O produtor continua filtrado por `loja__proprietario`.
- O contrato JSON da API não mudou: nenhum payload expõe `usuario`.
- Exclusão bloqueada: `PedidoCliente.usuario` e `Pedido.loja` usam `PROTECT`. Não é possível excluir um usuário que tenha pedidos como cliente, nem uma loja que tenha pedidos; o Django lança `ProtectedError` (no Admin, a exclusão é recusada com a lista dos pedidos). Isso preserva o histórico de pedidos. Para retirar o acesso, desative o usuário ou a loja.
- `Loja.proprietario` também usa `PROTECT` e é único (`uq_loja_proprietario`): não é possível excluir um produtor que tenha loja, tenha ela pedidos ou não, e a loja nunca é apagada em cascata com o usuário.
- As demais chaves estrangeiras não protegem: `PedidoProduto.produto` e as chaves de `Avaliacao` (`usuario`, `produto` e `pedido_produto`) usam `CASCADE`. Por isso produtos não são excluídos (são desativados) e avaliações só saem por moderação no Admin.

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

### Procedimento para aplicar no Supabase

Estado: **aplicado em produção (Supabase)**. Em 15/10/2026, `showmigrations` confirmou todas as migrations aplicadas, incluindo `pedidos` 0001 a 0005 (os 7 registros de `pedidos_pedidocliente` com `usuario_id` preenchido) e `lojas` 0003. O procedimento abaixo fica como registro histórico e como referência para novas aplicações, que exigem autorização.

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
   python apps/backend/manage.py migrate lojas --plan
   python apps/backend/manage.py migrate lojas
   # repita para usuarios e produtos; por fim:
   python apps/backend/manage.py migrate pedidos --plan
   python apps/backend/manage.py migrate pedidos
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
  "data_nascimento": "2000-05-10",
  "genero": "M",
  "password": "SenhaForte123",
  "password_confirmacao": "SenhaForte123"
}
```

Valida CPF, unicidade de CPF/e-mail, celular com 11 dígitos, idade mínima de 16 anos e senha de ao menos oito caracteres. Retorna `400` para dados inválidos ou duplicados.

## Perfil do usuário

- `GET /api/v1/usuarios/me/`: retorna os dados do usuário autenticado, incluindo `is_produtor`, `tem_loja` e `idade`.
- `PATCH /api/v1/usuarios/me/`: altera `nome`, `email`, `telefone`, `data_nascimento` e `genero`, com as mesmas validações do cadastro (e-mail único, celular com 11 dígitos e idade mínima de 16 anos). CPF e papéis (`is_produtor`, `is_staff`) não podem ser alterados e retornam `400`.
- Pedidos já realizados mantêm o snapshot dos dados do cliente; alterar o perfil não muda o histórico.

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
- "Este item já foi avaliado."
- "O comentário deve ter no máximo 500 caracteres."
- 400 — nota fora de 1 a 5 ou ausente (mensagens padrão do DRF).
- 401 — sem autenticação.

### Listar avaliações

- Método: GET
- URL: `/api/v1/avaliacoes/?produto=<id>`
- Autenticação: pública

Resposta esperada (`200`): lista no mesmo formato acima. `usuario_nome` é abreviado (primeiro nome e inicial do último sobrenome, como "Maria S."); o nome completo não é exposto. Avaliações de produto ou loja inativos continuam listadas. Sem `produto`, retorna todas as avaliações.

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
