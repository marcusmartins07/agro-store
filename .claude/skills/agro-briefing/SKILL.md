---
name: agro-briefing
description: "Modelo de briefing que o CTO usa para delegar tarefas do Agro Store aos agentes da Raiz Digital: skills a ler, tarefa, objetivo, regras, fase (Análise ou Implementação) e formato do relatório. Use ao montar ou receber uma delegação de tarefa."
---

> Origem: `skills/modelo.md`. Referências a `.ai/skills/*.md` correspondem às skills `agro-*` desta pasta.

# Skill: Briefing de tarefa

## Objetivo

Padronizar como uma tarefa é passada a um agente da Raiz Digital, para que todos recebam o mesmo
nível de contexto e sigam o mesmo fluxo: primeiro analisar e informar, depois implementar apenas
os ajustes necessários.

## Modelo de briefing

```md
Para: <agente> (<nome e cargo>)
Jira: SCRUM-XX (ou "sem tarefa no Jira")
Fase: Análise | Implementação
Aprovação do usuário: <citação literal do OK do usuário, quando a fase ou ação exigir>

Skills:
- agro-<skill> (já pré-carregadas no agente; listar só as que forem extras)

Tarefa:
<o que deve ser feito, em uma frase>

Objetivo:
<resultado esperado para o usuário ou para o sistema>

Regras:
- <regras de negócio que se aplicam, citando a skill agro-regras-de-negocio>
- <o que está fora do escopo do MVP e não deve ser feito>

Contexto:
- <arquivos, telas, endpoints ou decisões já conhecidas>
- <resultado de agentes anteriores (análise, especificação de UX, parecer do Tech Lead)>

Antes de alterar código (Fase Análise):
- Analise a implementação atual.
- Informe o que já está correto.
- Informe o que precisa ser ajustado.
- Liste os arquivos que pretende alterar.
- Não altere nenhum arquivo nesta fase.

Depois (Fase Implementação):
- Implemente apenas os ajustes aprovados na análise.
- Não amplie o escopo; registre oportunidades fora do escopo como pendência.

Relatório esperado:
- Resumo do que foi feito ou encontrado.
- Arquivos alterados (ou que pretende alterar).
- Regras de negócio impactadas.
- Testes executados e resultado.
- Pendências e dúvidas para o CTO.
- Impacto em documentação técnica e no texto do TCC.
```

## Regras do briefing

- Todo briefing informa a fase. Sem fase explícita, o agente trata como **Análise**.
- A Fase Implementação só é enviada depois que o usuário aprovou a análise.
- Ações externas (criar, mover ou comentar no Jira) exigem a citação literal da aprovação do usuário.
- Dúvidas de regra de negócio não são resolvidas por suposição: o agente as devolve ao CTO.
- Um mesmo conjunto de arquivos tem apenas um agente escrevendo por vez.

## Exemplo: revisão do carrinho

Briefing original que deu origem a este modelo:

```md
Leia o AGENTS.md e as skills:
- .ai/skills/backend.md
- .ai/skills/frontend.md
- .ai/skills/business-rules.md
- .ai/skills/database.md

Tarefa:
Revisar o carrinho do Agro Store.

Objetivo:
O carrinho deve ficar salvo no backend, mas o frontend pode calcular os totais para exibição.

Regras:
- Produto repetido no carrinho deve somar quantidade.
- Cliente precisa estar logado para usar carrinho.
- Produto inativo não pode ser adicionado.
- Produto sem estoque suficiente não pode ser adicionado.
- A finalização do carrinho deve criar pedidos separados por produtor/loja.
- Não implementar pagamento online.
- Retirada será presencial na feira.

Antes de alterar código:
- Analise a implementação atual.
- Informe o que já está correto.
- Informe o que precisa ser ajustado.
- Liste os arquivos que pretende alterar.

Depois implemente apenas os ajustes necessários.
```
