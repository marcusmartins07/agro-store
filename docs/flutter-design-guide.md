# Guia de Telas Flutter — Agro Store

Este guia descreve como recriar as principais telas do app em **Flutter**, mantendo as mesmas cores, espaçamentos e padrões visuais usados no frontend web (Vue + Bootstrap).

---

## 1. Paleta de cores

Extraída de `apps/frontend/src/assets/main.css`. Crie um arquivo `lib/theme/app_colors.dart`:

```dart
import 'package:flutter/material.dart';

class AppColors {
  static const green       = Color(0xFF2E8B57); // cor primária (botões, links, destaques)
  static const greenDark   = Color(0xFF1E6B40); // hover/pressed, headers escuros
  static const greenLight  = Color(0xFFE8F5E9); // fundos suaves (imagens de produto, chips)
  static const greenMid    = Color(0xFFC8E6C9); // avatares, ícones circulares
  static const greenText   = Color(0xFF1B5E35); // texto sobre fundo claro (títulos)
  static const tagBg       = Color(0xFFA5D6A7); // badges de desconto
  static const tagText     = Color(0xFF1B5E35);
  static const white       = Color(0xFFFFFFFF);
  static const gray        = Color(0xFF6B7280); // texto secundário
  static const grayLight   = Color(0xFFF3F4F6); // fundo de campos "somente leitura"
  static const border      = Color(0xFFD1E7D8); // bordas de cards
  static const star        = Color(0xFFF59E0B); // avaliações
  static const danger      = Color(0xFFDC2626); // erros, remover, favoritos ativos
  static const warningBg   = Color(0xFFFFFDE7); // card "Ofertas do dia"
  static const warningBorder = Color(0xFFFDE68A);
  static const warningText = Color(0xFF856404);
}
```

**Regra geral:** fundo padrão do app é `greenLight` (`#E8F5E9`), texto padrão é `greenText` (`#1B5E35`), botão primário é `green` (`#2E8B57`) com hover/pressed `greenDark` (`#1E6B40`).

---

## 2. Tema global (ThemeData)

Crie `lib/theme/app_theme.dart`:

```dart
import 'package:flutter/material.dart';
import 'app_colors.dart';

final appTheme = ThemeData(
  useMaterial3: true,
  scaffoldBackgroundColor: AppColors.greenLight,
  fontFamily: 'Segoe UI', // ou a fonte padrão do sistema
  colorScheme: ColorScheme.fromSeed(
    seedColor: AppColors.green,
    primary: AppColors.green,
    error: AppColors.danger,
  ),
  appBarTheme: const AppBarTheme(
    backgroundColor: AppColors.white,
    foregroundColor: AppColors.greenText,
    elevation: 1,
  ),
  cardTheme: CardTheme(
    color: AppColors.white,
    elevation: 0,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(14), // cards de produto/telas usam 14px
      side: const BorderSide(color: AppColors.border),
    ),
  ),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: AppColors.green,
      foregroundColor: AppColors.white,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)), // pill
      padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 20),
      textStyle: const TextStyle(fontWeight: FontWeight.bold),
    ),
  ),
  inputDecorationTheme: InputDecorationTheme(
    filled: true,
    fillColor: AppColors.white,
    border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
  ),
);
```

**Padrões visuais recorrentes:**
- Cards: `border-radius: 14px`, borda `#D1E7D8`, fundo branco.
- Botões primários: fundo verde, texto branco, `border-radius` arredondado (pill quando é ação de destaque como "Login" ou "Finalizar Pedido").
- Títulos de seção: `fontWeight: bold`, cor `greenText`.
- Texto secundário: cinza (`gray`).
- Ícones/emojis são usados no lugar de imagens (🌿 🛒 👤 🔍 🥦 🍎 etc.) — mantenha os mesmos emojis para consistência.

---

## 3. Estrutura de navegação

O app web tem uma navbar fixa com: logo, busca, catálogo, carrinho (com badge de contagem) e menu de conta. No Flutter, use:

- `Scaffold` com `AppBar` (logo + ação de busca) e `BottomNavigationBar` ou `Drawer` para: Catálogo, Carrinho, Pedidos, Favoritos, Perfil.
- Badge de contagem no ícone do carrinho: use `Badge` do Material 3 (`Badge(label: Text('$totalItens'), child: Icon(Icons.shopping_cart))`).

Rotas principais (equivalente às views Vue em `router/index.js`):

| Tela Flutter | Equivale à view Vue | Rota |
|---|---|---|
| `ProdutosScreen` | `ProdutosView.vue` | `/` |
| `CarrinhoScreen` | `CarrinhoView.vue` | `/carrinho` |
| `FavoritosScreen` | `FavoritosView.vue` | `/favoritos` |
| `PedidosScreen` | `PedidosView.vue` | `/pedidos` |
| `ClienteScreen` (perfil) | `ClienteView.vue` | `/cliente` |
| `LoginScreen` | `LoginView.vue` | `/login` |
| `LojaScreen` | `LojaView.vue` | `/loja/:id` |

---

## 4. Telas principais

### 4.1 Tela de Produtos (Catálogo) — `ProdutosScreen`

Equivalente a `ProdutosView.vue`. Estrutura:

1. **Cabeçalho**: título "Nosso Mercado" (bold, `greenText`) + subtítulo cinza + campo de busca.
2. **Filtros** (em mobile, pode virar um `BottomSheet` ou `ExpansionTile` em vez da sidebar lateral):
   - Categorias: lista de botões — ativo com fundo verde/texto branco, inativo com fundo cinza claro.
   - Ordenação: mesma lógica (Relevância, Menor preço, Maior preço, Com desconto).
   - Card "Ofertas do Dia": fundo amarelo claro (`warningBg`), borda (`warningBorder`), texto (`warningText`).
3. **Grid de produtos**: `GridView` com 2 colunas em mobile (equivalente ao `row-cols-2` do Bootstrap), usando o `ProductCard` (ver 5.1).
4. **Estado vazio**: emoji 🌾 grande, texto "Nenhum produto encontrado", botão "Limpar filtros".
5. **Loading**: shimmer/skeleton nos cards.

### 4.2 Tela de Carrinho — `CarrinhoScreen`

Equivalente a `CarrinhoView.vue`.

- Título "Meu Carrinho" (bold, `greenText`).
- **Não logado / vazio**: card centralizado com ícone circular verde-claro (`greenMid`), texto explicativo e botão pill verde ("Fazer login" / "Voltar ao Mercado").
- **Itens agrupados por loja/fornecedor**: label em maiúsculas cinza com emoji 🏪, seguido de cards por item contendo:
  - checkbox de seleção
  - miniatura com emoji (fundo `greenLight`, `border-radius: 10`)
  - nome do produto + preço (verde)
  - stepper de quantidade (botões `−` / `+`)
  - subtotal
  - botão remover (✕, vermelho)
- **Resumo do pedido** (card lateral, ou seção fixa no fim em mobile): subtotal por fornecedor, total selecionado, local de retirada, botão "Finalizar Pedido" (verde, full-width) e "Continuar comprando" (outline).

### 4.3 Tela de Login/Cadastro — `LoginScreen`

Equivalente a `LoginView.vue`.

- Card centralizado, largura máxima ~400-500dp.
- **Cabeçalho do card**: fundo `greenDark`, texto branco — "Agro Store" + subtítulo.
- **Toggle Entrar/Cadastrar**: dois botões lado a lado dentro de um container com fundo `greenLight` e `border-radius: 10`; o ativo tem fundo `greenDark` e texto branco (como um `SegmentedButton`).
- **Form de login**: campo CPF (com máscara `000.000.000-00`), campo senha (com botão mostrar/ocultar), botão "Acessar marketplace" (verde escuro, full-width).
- **Form de cadastro**: nome, CPF, celular (com máscara), e-mail, data de nascimento, gênero (dropdown), senha + confirmação.

### 4.4 Tela de Perfil — `ClienteScreen`

Equivalente a `ClienteView.vue`.

- Card 1 (topo/lateral): avatar circular com iniciais (fundo `greenMid`, texto `greenText`), nome, e-mail, badge de tipo de conta ("Produtor rural" verde / "Cliente" cinza).
- Card 2: lista de informações pessoais em grid 2 colunas — cada campo com label pequeno cinza + valor em um "box" com fundo `grayLight`, borda `border`, `border-radius: 8`.

### 4.5 Tela vazia/placeholder padrão

Usada em telas ainda não implementadas (`LojaView.vue`, `AvaliacoesView.vue`): card centralizado, `border-radius: 14`, título "Em breve" (bold, `greenText`) e texto cinza explicativo.

---

## 5. Componentes reutilizáveis

### 5.1 `ProductCard`

Equivalente a `ProductCard.vue`. Estrutura de cima para baixo:

- Área de imagem: altura fixa (~160dp), fundo `greenLight`, emoji grande centralizado (56px) representando a categoria.
  - Badge de desconto no canto superior esquerdo: fundo `tagBg`, texto `tagText`, ex: "-20%".
  - Botão de favorito (círculo) no canto superior direito: fundo branco/coração vazio (♡) quando não favoritado, fundo vermelho/coração cheio (♥) quando favoritado.
- Corpo do card:
  - Linha: categoria (badge de texto verde, maiúsculo, pequeno) + nome da loja (cinza, com emoji 🏪).
  - Nome do produto (bold).
  - Descrição (cinza, pequena, opcional).
  - Preço (verde, bold, grande) + preço original riscado (se houver desconto).
  - Botão "🛒 Adicionar" (verde, full-width). Se indisponível, mostra mensagem e desabilita.

Mapa de emojis por categoria (mantenha os mesmos):

```dart
const categoriaEmojis = {
  'Vegetais': '🥦',
  'Verduras': '🥬',
  'Frutas': '🍎',
  'Doces': '🍯',
  'Laticínios': '🧀',
  'Grãos': '🌾',
  'Artesanato': '🧺',
  'Pães': '🍞',
  'Carnes': '🥩',
  'Ovos': '🥚',
};
// padrão: '🌱'
```

### 5.2 Botões

- **Primário**: fundo `green`, texto branco, `border-radius` pill (24+) para ações de destaque (login, finalizar pedido) ou 8px para ações normais (adicionar ao carrinho).
- **Outline**: borda `greenDark`/cinza, texto da mesma cor, fundo transparente.
- **Ativo/selecionado** (filtros, toggle): fundo verde sólido, texto branco. Inativo: fundo cinza claro, texto cinza escuro.

### 5.3 Badges

- Badge de categoria: texto verde, negrito, maiúsculo, tamanho pequeno.
- Badge de tipo de conta: pill, fundo verde (produtor) ou cinza (cliente), texto branco.
- Badge de contagem (carrinho): círculo vermelho pequeno sobre o ícone.

---

## 6. Convenções gerais

- **Espaçamento**: usar múltiplos de 4/8dp, similar ao `gap-2`/`gap-3` do Bootstrap (8px/12px).
- **Bordas arredondadas**: 8px em inputs, 12-14px em cards, pill (999px) em botões de destaque e badges.
- **Tipografia**: títulos em negrito com a cor `greenText`; texto de apoio em cinza (`gray`).
- **Feedback ao usuário**: usar `SnackBar` para mensagens de sucesso/erro, seguindo o mesmo padrão do sistema de notificações do frontend web (`stores/notificacoes.js`) — cores: verde para sucesso, vermelho para erro.
- **Emojis no lugar de ícones customizados**: o app web usa emojis nativos extensivamente em vez de ícones SVG. Para manter a identidade visual, prefira usar os mesmos emojis como `Text` ao invés de trocar por `Icon` do Material, exceto onde um ícone padrão (ex: carrinho, busca) for mais legível no Flutter.

---

## 7. Checklist de implementação

- [ ] Criar `AppColors` e `appTheme`.
- [ ] Implementar `Scaffold` base com navegação (AppBar + BottomNavigationBar/Drawer).
- [ ] Tela de Login/Cadastro.
- [ ] Tela de Produtos (catálogo) com filtros e grid.
- [ ] Componente `ProductCard`.
- [ ] Tela de Carrinho.
- [ ] Tela de Perfil.
- [ ] Tela de Pedidos.
- [ ] Tela de Favoritos.
- [ ] Tela de Loja/Vitrine do produtor.
