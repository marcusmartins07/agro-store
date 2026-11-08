---
name: agro-banco-de-dados
description: "Modelo de dados do Agro Store: fonte de verdade em docs/modelo-logico.sql, convenções de nomes em português, compatibilidade Django/SQLite/PostgreSQL, relações e histórico, migrations e restrições. Use ao propor, alterar ou revisar models, migrations, constraints ou o modelo lógico."
---

> Origem: `skills/database.md`. Referências a `.ai/skills/*.md` correspondem às skills `agro-*` desta pasta.

# Skill: Banco de Dados

## Objetivo e fonte de verdade

Orientar alterações no modelo de dados do Agro Store. O modelo lógico canônico
está em [`docs/modelo-logico.sql`](../../docs/modelo-logico.sql); ele é uma
referência PostgreSQL. O schema executável é gerado pelas migrations Django
(SQLite em desenvolvimento, PostgreSQL no Docker local e em produção).

Uma mudança no SQL canônico não autoriza, por si só, mudança em models,
migrations ou API. Antes de alinhar a implementação, avaliar o impacto e obter
aprovação conforme `AGENTS.md`.

## Convenções

- Usar português do Brasil e `snake_case` em tabelas, colunas, constraints e
  chaves físicas: `id_pedido`, `data_criacao`, `esta_ativa`.
- Usar `id_<entidade>` para chaves primárias e estrangeiras no modelo lógico;
  não usar prefixos como `fk_`.
- Manter `produtor` para a pessoa vendedora e `loja` para seu espaço comercial.
- CPF, CNPJ, SKU, código de barras e telefone são texto, preservando zeros à
  esquerda. Valores monetários usam `Decimal`/`DECIMAL`, nunca `float`.
- Datas de auditoria usam `data_criacao` e `data_atualizacao`; vigências usam
  `vigencia_inicio` e `vigencia_fim`.
- `status` é uma exceção de domínio consolidada; no modelo lógico de pedido, a
  relação é identificada por `id_status_pedido`.

## Django e compatibilidade

- O contrato de autenticação do Django exige atributos como `password`,
  `last_login`, `is_active`, `is_staff` e `is_superuser`.
- Esses atributos Python são preservados, e suas colunas físicas são mapeadas
  em português com `db_column` (`senha`, `ultimo_login`, `esta_ativo`,
  `e_equipe`, `e_superusuario`).
- Não alterar campos JSON, serializers, rotas ou frontend apenas para refletir
  a nomenclatura física do banco. Qualquer mudança de API precisa de aprovação
  específica.

## Relações e histórico

- Produto possui uma única categoria obrigatória. A exclusão é protegida;
  categorias devem ser inativadas, não removidas.
- Loja pertence a um produtor: `loja.proprietario` é PROTECT e único
  (`uq_loja_proprietario`), produtor (1,1) — (0,1) loja.
  Produtor com loja não é excluído; a loja é desativada. A relação continua
  `ForeignKey` (`usuario.lojas`), não `OneToOneField`.
- Produto pertence a uma loja; preços pertencem a produto e mantêm vigência.
- Imagens pertencem a produto (`ImagemProduto`, cascata com o produto): produto
  (1,1) — (0,n) imagem, com `ordem` e `e_principal`. A restrição única
  condicional `imagem_principal_unica_por_produto` impede duas principais; o
  limite de 5 imagens é validado na API. O antigo campo `Produto.imagem` foi
  copiado para a imagem principal e removido; não existe mais no model nem no banco.
- Loja e usuário têm uma imagem única cada (`Loja.imagem_perfil` e `Usuario.foto_perfil`, `FileField` de 255,
  `''` quando vazio), substituída na troca. `imagem_perfil` era texto e virou arquivo sem mudar a coluna,
  preservando os caminhos legados. Extensões e nome aleatório ficam em `main/imagens.py`.
- Telefones pertencem ao usuário (`Telefone`, cascata com o usuário; RN-021): usuário (1,1) — (0,n) telefone,
  com tipo obrigatório (`TipoTelefone.descricao`, PROTECT; tipos fixos Celular, Fixo e Comercial carregados pela
  migration `usuarios/0002_dados_iniciais`), `numero` texto de até 11 dígitos (somente dígitos, com DDD, sem unicidade) e
  `e_principal`. A restrição única condicional `telefone_principal_unico_por_usuario` impede dois principais; o
  mínimo de 1 telefone e os dígitos por tipo (`TipoTelefone.DIGITOS_POR_TIPO`) são validados na API e no admin.
  Exceção legada: contas sem telefone antes da DB-018 e contas criadas por `createsuperuser` podem ter 0 telefones.
  O antigo `Usuario.telefone` foi copiado como principal e removido (DB-018).
- Carrinho pertence a um usuário e uma loja. `carrinho_produto` é o item do
  carrinho e é único por carrinho e produto.
- Pedido pertence à loja e ao status; `pedido.loja` é PROTECT. O cliente fica em
  `pedido_cliente.usuario` (obrigatório, PROTECT/RESTRICT), junto com o snapshot.
  Pedidos e suas referências centrais não podem ser apagados em cascata.
- `pedido_cliente` é o snapshot um-para-um do cliente, exceto o telefone (RN-021): o telefone não é
  copiado para o pedido (`PedidoCliente.telefone` foi removido na DB-018) e é consultado no telefone
  principal atual do cliente. `pedido_produto` mantém
  nome, quantidade e valores do momento da compra; sua referência ao produto é
  opcional e deve usar `SET NULL` se o produto for removido.
- Favoritos são únicos por usuário e produto. Avaliações possuem nota de 1 a 5
  e são vinculadas ao item de pedido avaliado.

## Migrations e checklist

Histórico consolidado (DB-022): cada app (`usuarios`, `lojas`, `produtos`, `carrinhos`, `pedidos`, `favoritos`,
`avaliacoes`) tem uma única `0001_initial`, gerada a partir dos models, e `usuarios/0002_dados_iniciais` carrega os
dados fixos: gêneros M, F e I e tipos de telefone Celular, Fixo e Comercial. `status_pedido` não tem seed e é criado
sob demanda. O seed de gênero cria M, F e I somente se não existirem e troca I de "Indefinido" para "Prefiro não
informar" somente quando ainda for "Indefinido", sem desfazer nomes trocados pelo administrador (RN-024). Números de
migration anteriores à DB-022 (por exemplo `lojas/0003` ou `usuarios/0007`) não existem mais. Comandos locais
chamam o Python do venv com `DATABASE_URL` explícito, porque o `.env` da raiz aponta para o Supabase.

Após uma alteração de model aprovada:

1. Atualizar o model e gerar a migration; para renomeações, preferir operações
   de rename/mapeamento que preservem os dados em vez de recriar tabelas.
2. Revisar compatibilidade SQLite/PostgreSQL, constraints, `on_delete` e dados
   existentes antes de aplicar a migration.
3. Verificar serializers, admin, views, permissões, serviços/stores/telas do
   frontend, testes, documentação técnica e texto do TCC.
4. Validar que pedidos, itens e snapshots históricos permanecem consultáveis.

## Restrições

Não fazer automaticamente sem autorização:

- Renomear tabelas ou colunas físicas existentes.
- Remover campos, relacionamentos ou dados.
- Alterar cardinalidade, estratégia de carrinho/pedidos ou contrato da API.
- Criar migrations sem uma alteração de model aprovada.

Trava temporária (DB-022, Tech Lead): até a DB-023 ser executada, não criar migrations novas nos apps `usuarios`,
`lojas`, `produtos`, `carrinhos`, `pedidos`, `favoritos` e `avaliacoes`, mesmo com alteração de model aprovada, e
não rodar `migrate` no Supabase.
