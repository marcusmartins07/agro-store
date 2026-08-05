# Agro Store

Monorepo com API Django e aplicação web Vue.

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
- `POST /api/v1/produtos/` e `PATCH /api/v1/produtos/{id}/`: cadastra ou altera produtos da própria loja.
- `POST /api/v1/produtos/precos/`: registra um novo preço vigente, encerrando automaticamente o preço anterior. Recebe `produto`, `preco_venda` e, opcionalmente, `porcentagem_desconto` entre 0 e 100.
- `GET /api/v1/pedidos/minha-loja/`: lista pedidos da loja com itens, valores e somente nome/telefone do cliente.
- `GET /api/v1/pedidos/status-disponiveis/` e `PATCH /api/v1/pedidos/{id}/status/`: consulta e atualiza o status pelo fluxo `Pendente → Em preparo → Pronto para retirada → Entregue`, com cancelamento permitido antes da retirada.
- `PATCH /api/v1/lojas/me/`: altera apenas `descricao` e `ativa`. Uma loja inativa preserva o histórico e não aceita novas compras.

Cada produtor pode cadastrar somente uma loja. Imagem de loja e alertas configuráveis de estoque permanecem como evoluções futuras.

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

## Idioma e notificações

- O backend usa português do Brasil (`pt-br`) para mensagens nativas de validação do Django.
- O frontend possui notificações globais de `success`, `info`, `warning` e `danger`; sem tempo informado, permanecem até fechamento manual ou atualização da página.
