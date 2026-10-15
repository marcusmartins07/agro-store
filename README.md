# Agro Store

Monorepo com API Django e aplicação web Vue.

## Funcionalidades principais

- Catálogo público de produtos com filtro por categoria e imagens por produto (até 5, com uma principal).
- Controle de disponibilidade por estoque: produto com estoque 0 sai da listagem do catálogo (o detalhe continua acessível, com a compra bloqueada) e volta quando o estoque é reposto. Detalhes em [Disponibilidade por estoque](#disponibilidade-por-estoque-rn-017).
- Indicador de estoque baixo (1 a 5 unidades) na área do produtor.
- Carrinho salvo no backend, com ajuste automático da quantidade quando o estoque diminui.
- Finalização do carrinho com um pedido por loja, baixa de estoque e snapshot de cliente e produtos.
- Cancelamento de pedidos pendentes pelo cliente, com restauração do estoque.
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

### SKU de produtos

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

## Idioma e notificações

- O backend usa português do Brasil (`pt-br`) para mensagens nativas de validação do Django.
- O frontend possui notificações globais de `success`, `info`, `warning` e `danger`; sem tempo informado, permanecem até fechamento manual ou atualização da página.
