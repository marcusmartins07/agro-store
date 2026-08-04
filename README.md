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
