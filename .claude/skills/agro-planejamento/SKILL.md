---
name: agro-planejamento
description: "Planejamento do Agro Store: princípios, áreas, modelo de tarefa TASK, regras de criação, priorização, critério de pronto e controle no Jira (projeto SCRUM em agrostore.atlassian.net, rótulos por área, status e vínculos Blocks) com registro em .ai/todo/. Use ao planejar, quebrar ou documentar tarefas."
---

> Origem: `skills/planning.md`. Referências a `.ai/skills/*.md` correspondem às skills `agro-*` desta pasta.

# Skill: Planejamento

## Objetivo

Orientar o planejamento do desenvolvimento do Agro Store.

Esta skill deve ser usada para organizar o que será desenvolvido, definir prioridades, quebrar funcionalidades em tarefas e manter clareza sobre o andamento do projeto.

## Escopo

O planejamento deve considerar que o Agro Store é um MVP para TCC.

Portanto, a prioridade deve ser entregar as funcionalidades essenciais para demonstrar o funcionamento do sistema.

## Princípios

- Priorizar funcionalidades essenciais.
- Evitar tarefas grandes demais.
- Dividir desenvolvimento em etapas pequenas.
- Separar tarefas por área quando necessário.
- Evitar funcionalidades fora do escopo do MVP.
- Sempre considerar impacto no TCC.
- Manter rastreabilidade do que foi planejado, feito e ajustado.

## Áreas de planejamento

As tarefas podem ser organizadas por área:

- Backend.
- Frontend.
- Banco de dados.
- Regras de negócio.
- Testes.
- Documentação.
- TCC.

## Modelo recomendado de tarefa

```md
## TASK-000 — Título da tarefa

Status: Backlog | Em andamento | Concluído

Área:
Backend | Frontend | Banco | Regras de negócio | Testes | Documentação | TCC

Objetivo:
Descrever o objetivo da tarefa.

Descrição:
Detalhar o que precisa ser feito.

Arquivos previstos:
- caminho/do/arquivo

Critérios de aceite:
- [ ] Critério 1
- [ ] Critério 2
- [ ] Critério 3

Observações:
- Informações adicionais.
```

## Regras para criação de tarefas

- Toda tarefa deve ter objetivo claro.
- Toda tarefa deve ter critérios de aceite.
- Toda tarefa deve informar a área principal.
- Tarefas grandes devem ser divididas.
- Não criar tarefas desnecessariamente pequenas.
- Priorizar o que destrava o MVP.
- Registrar dúvidas de regra de negócio antes da implementação.

## Priorização recomendada

Ordem geral sugerida:

1. Revisar estrutura atual.
2. Revisar autenticação.
3. Revisar produtos.
4. Revisar carrinho.
5. Revisar pedidos.
6. Revisar permissões.
7. Revisar telas principais.
8. Revisar testes mínimos.
9. Atualizar documentação.
10. Preparar apresentação e texto do TCC.

## Critério para considerar tarefa pronta

Uma tarefa só deve ser considerada pronta quando:

- A implementação foi feita.
- O comportamento esperado foi validado.
- Não há erro evidente.
- O impacto no restante do projeto foi avaliado.
- A documentação foi atualizada, se necessário.

## Controle de tarefas

O controle principal das tarefas fica no Jira: projeto Agro Store (`SCRUM`) em `https://agrostore.atlassian.net`.

- Toda tarefa é do tipo `Tarefa` e o resumo mantém o ID por área: `BE-016 — Título da tarefa`.
- A área vai em rótulo, com o nome do arquivo em `.ai/todo/`: `backend`, `banco-de-dados`, `documentacao-tcc`, `frontend`, `regras-de-negocio` ou `testes`.
- Status: `A fazer` (pendente), `Em andamento`, `Em análise` e `Concluído`.
- Critérios de aceite ficam como lista de verificação na descrição.
- Uma linha "Dependência:" vira vínculo `Blocks` no Jira (a tarefa da qual se depende bloqueia a outra).
- Os arquivos de `.ai/todo/` continuam como registro: cada tarefa tem a linha `Jira: SCRUM-XX`. Ao criar uma tarefa no Jira, registrar também no arquivo da área com o mesmo ID e a chave.
