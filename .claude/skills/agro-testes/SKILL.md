---
name: agro-testes
description: "Prioridades e casos mínimos de testes do Agro Store (login, permissões, produtos, carrinho, split de pedidos, status, favoritos, avaliações, preço vigente e estoque). Use ao criar, manter ou executar testes e ao validar critérios de aceite."
---

> Origem: `skills/tests.md`. Referências a `.ai/skills/*.md` correspondem às skills `agro-*` desta pasta.

# Skill: Testes

## Objetivo

Orientar criação e manutenção de testes do Agro Store.

## Prioridades

Priorizar testes para regras de negócio críticas:

1. Login.
2. Permissões.
3. Cadastro de produto.
4. Carrinho.
5. Split de pedidos por produtor/loja.
6. Status de pedido.
7. Favoritos.
8. Avaliações.
9. Preço vigente.
10. Estoque.

## Backend

Testar preferencialmente:

- Models.
- Serializers.
- ViewSets.
- Permissões.
- Endpoints principais.
- Regras de criação de pedido.
- Regras de carrinho.

## Frontend

Testes frontend podem ser mais simples no MVP.

Priorizar validações manuais documentadas quando testes automatizados forem desnecessários para o prazo do TCC.

## Regras

- Não instalar biblioteca de teste sem autorização.
- Usar o padrão já existente no projeto.
- Se não houver testes estruturados, sugerir antes de implementar.
- Criar testes objetivos.
- Evitar testes frágeis baseados apenas em layout.

## Casos mínimos recomendados

### Carrinho

- Adicionar produto ao carrinho.
- Somar quantidade se produto já existir.
- Remover item do carrinho.
- Impedir quantidade inválida.
- Impedir produto inativo.

### Pedidos

- Criar pedido com uma loja.
- Criar múltiplos pedidos quando houver produtos de lojas diferentes.
- Criar snapshot do cliente.
- Criar snapshot dos produtos.
- Limpar carrinho após finalizar.
- Impedir pedido com carrinho vazio.

### Permissões

- Cliente não cadastra produto.
- Produtor cadastra produto.
- Produtor visualiza pedidos da própria loja.
- Cliente visualiza apenas seus próprios pedidos.
