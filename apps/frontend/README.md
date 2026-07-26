# 🌿 Agro Store — TCC

Marketplace para produtores rurais desenvolvido com **Vue 3 + Vite + Pinia + Vue Router**.

---

## 🚀 Como rodar o projeto

### 1. Instalar dependências
```bash
npm install
```

### 2. Rodar em desenvolvimento
```bash
npm run dev
```
Acesse: http://localhost:5173

### 3. Gerar build de produção
```bash
npm run build
```

---

## 📁 Estrutura do projeto

```
src/
├── assets/
│   └── main.css          # Variáveis CSS globais (cores, fontes)
├── components/
│   └── ProductCard.vue   # Card de produto reutilizável
├── data/
│   └── mock.js           # Dados fake (produtos, fornecedores, categorias)
├── router/
│   └── index.js          # Rotas (vue-router)
├── stores/
│   └── index.js          # Estado global: carrinho e favoritos (Pinia)
├── views/
│   ├── ProdutosView.vue  # ✅ Catálogo com filtros e grid
│   ├── CarrinhoView.vue  # 🔜 Em desenvolvimento
│   ├── FavoritosView.vue # 🔜 Em desenvolvimento
│   ├── PedidosView.vue   # 🔜 Em desenvolvimento
│   ├── LojaView.vue      # 🔜 Em desenvolvimento
│   ├── AvaliacoesView.vue# 🔜 Em desenvolvimento
│   ├── ClienteView.vue   # 🔜 Em desenvolvimento
│   ├── EmpRuralView.vue  # 🔜 Em desenvolvimento
│   └── LoginView.vue     # 🔜 Em desenvolvimento
└── App.vue               # Layout raiz com topbar
```

---

## 🎨 Cores do projeto

| Variável         | Valor     | Uso                          |
|------------------|-----------|------------------------------|
| `--green`        | `#2E8B57` | Botões, links, destaques     |
| `--green-dark`   | `#1e6b40` | Hover dos botões             |
| `--green-light`  | `#E8F5E9` | Background geral             |
| `--green-text`   | `#1b5e35` | Textos principais            |
| `--border`       | `#d1e7d8` | Bordas dos cards             |

---

## 🗃️ Stores (Pinia)

### `useCarrinhoStore`
| Método / Getter     | Descrição                              |
|---------------------|----------------------------------------|
| `adicionar(produto)`| Adiciona ou incrementa item            |
| `remover(id)`       | Remove item do carrinho                |
| `alterarQuantidade` | Incrementa/decrementa quantidade       |
| `total`             | Valor total (computed)                 |
| `porFornecedor`     | Itens agrupados por fornecedor         |
| `totalItens`        | Contagem total de itens                |

### `useFavoritosStore`
| Método / Getter     | Descrição                              |
|---------------------|----------------------------------------|
| `alternar(produto)` | Adiciona ou remove dos favoritos       |
| `isFavorito(id)`    | Retorna true/false                     |
| `ordenados`         | Lista ordenada por data (mais recente) |