---
name: agro-backend
description: "Padrões do backend do Agro Store (Django, DRF, Simple JWT): PEP 8 pragmático com 150 colunas, responsabilidades de models/serializers/views, segurança e variáveis de ambiente, permissões, categorias e checklist de alterações. Use ao criar, alterar, revisar ou auditar código em apps/backend/."
---

> Origem: `skills/backend.md`. Referências a `.ai/skills/*.md` correspondem às skills `agro-*` desta pasta.

# Skill: Backend

## Objetivo

Orientar alterações no backend do Agro Store, desenvolvido em Django e Django REST Framework.

## Localização

```text
apps/backend/
```

## Tecnologias

- Python.
- Django.
- Django REST Framework.
- Simple JWT.
- SQLite em desenvolvimento.
- PostgreSQL como objetivo final.

## Regras obrigatórias

- Seguir a estrutura existente do projeto.
- Não instalar bibliotecas externas sem autorização.
- Aplicar PEP 8 pragmático e manter o máximo de 150 caracteres por linha.
- Usar `flake8` como verificação recomendada quando estiver disponível no ambiente.
- Usar `# noqa` somente quando necessário, com o código da regra e uma justificativa no comentário.
- Preferir código simples, legível e sem abstrações desnecessárias.
- Manter compatibilidade com SQLite e PostgreSQL.
- Não alterar models sem avaliar impactos.
- Criar migrations automaticamente quando models forem alterados após aprovação.
- Não expor dados sensíveis nem criar endpoints públicos sem necessidade.
- Não incluir segredos, tokens, senhas ou dados pessoais em logs, respostas de erro, fixtures ou arquivos versionados.

## Padrão de código

### PEP 8 pragmático

- Usar 4 espaços para indentação, sem tabs, e separar elementos de alto nível por duas linhas em branco.
- Usar `snake_case` para funções, métodos, variáveis e módulos; `PascalCase` para classes; e `UPPER_CASE` para constantes.
- Usar nomes descritivos e específicos do domínio. Evitar abreviações obscuras e nomes genéricos
  como `data`, `item` ou `result` quando um nome mais claro for possível.
- Manter linhas com até 150 caracteres. Quebrar chamadas, coleções e expressões longas de forma legível antes de ultrapassar esse limite.
- Organizar imports em blocos: biblioteca padrão, dependências de terceiros e módulos do projeto; separar os blocos por uma linha em branco.
- Evitar imports curinga, imports não utilizados e múltiplos imports sem relação na mesma linha.
- Usar aspas e estilo já predominantes no arquivo alterado; não reformatar arquivos inteiros sem necessidade.

### Responsabilidades e legibilidade

- Manter funções e métodos focados em uma responsabilidade. Extrair passos repetidos ou complexos para funções nomeadas.
- Models representam persistência e regras diretamente ligadas à entidade. Serializers validam e transformam dados de entrada e saída.
- Views e ViewSets devem concentrar autenticação, permissões, queryset e orquestração da requisição, sem acumular regras críticas extensas.
- Quando um fluxo de negócio crítico envolver múltiplas entidades ou passos, centralizá-lo em uma
  função ou serviço explícito e usar transação quando necessário.
- Não duplicar regra de negócio em múltiplos serializers, views ou no frontend.
- Remover código morto, `print`, comentários temporários, `TODO` sem tarefa associada e dados de teste antes de finalizar uma alteração.

### Exceções, logs e respostas

- Capturar somente exceções esperadas e tratá-las no nível adequado; não usar `except:` vazio nem silenciar falhas.
- Retornar respostas de erro claras e consistentes, com status HTTP apropriado, sem revelar detalhes internos da aplicação.
- Usar logs para diagnóstico quando necessário, mas nunca registrar senhas, JWTs, chaves, CPF, e-mail completo ou outros dados sensíveis.

## Segurança e variáveis de ambiente

- Usar `os.getenv` para configurações de ambiente e converter valores para o tipo esperado de forma explícita.
- O arquivo `.env` é local, não pode ser versionado e deve partir do modelo `.env.example`, que
  contém apenas valores seguros de desenvolvimento e placeholders.
- Não armazenar segredos em código Python, arquivos de configuração versionados, comandos, documentação, prints ou logs.
- Para produção, a configuração deve falhar de forma segura:
  `DJANGO_SECRET_KEY` deve existir e ser segura; `DJANGO_DEBUG` deve ser `false`; e
  `DJANGO_ALLOWED_HOSTS` e `CORS_ALLOWED_ORIGINS` devem estar definidos explicitamente.
- Não usar chave secreta padrão, `DEBUG=true`, hosts curingas ou CORS permissivo em produção.
- A configuração local do VS Code deve permanecer em `.vscode/launch.json`, ignorada pelo Git,
  e usar `envFile` com `${workspaceFolder}/.env`. O arquivo `launch.json` não pode conter
  valores secretos.

### Achado atual para auditorias

`apps/backend/agrostore/settings.py` ainda possui fallback para `SECRET_KEY` e assume `DEBUG=true`
quando variáveis não são fornecidas. Esse comportamento é aceitável apenas durante o desenvolvimento
local e deve ser sinalizado em qualquer auditoria ou preparação de produção. A sua correção exige
uma tarefa específica, pois altera o comportamento de inicialização do backend.

## Qualidade e auditoria

- `flake8` é a ferramenta recomendada para verificar estilo e erros estáticos. Ela ainda não está
  instalada nem configurada no projeto; não instalá-la sem autorização.
- Quando disponível, executar `python -m flake8 apps/backend` e corrigir os achados relevantes,
  respeitando o limite de 150 caracteres definido nesta skill.
- Antes de uma alteração relevante, revisar permissões, exposição de dados, validações no backend,
  transações, migrations, compatibilidade SQLite/PostgreSQL, testes e impacto no frontend.
- Ao alterar configurações, revisar `.env.example`, `.gitignore`, `settings.py`, `ALLOWED_HOSTS`,
  CORS, `DEBUG` e o risco de expor valores em logs ou no controle de versão.
- Ao alterar regra de negócio, seguir também `.ai/skills/business-rules.md` e avaliar impacto em
  backend, frontend, banco, testes, documentação técnica e TCC.

## Apps esperados

O backend pode conter apps como:

- usuarios.
- lojas.
- produtos.
- carrinhos.
- pedidos.
- favoritos.
- avaliacoes.
- main.

Antes de criar um novo app, verificar se a funcionalidade pode ficar em um app existente.

## Autenticação

- Manter JWT.
- Access token e refresh token devem continuar sendo usados.
- Endpoints privados devem exigir autenticação.
- Endpoints públicos devem ser liberados apenas quando fizer sentido.

Exemplos de endpoints públicos possíveis:

- Listagem de produtos.
- Detalhe de produto.
- Listagem de lojas.
- Detalhe de loja.
- Listagem de categorias.
- Login.

## Permissões

O sistema trabalha com usuários que podem ter diferentes papéis por permissões e propriedades do perfil.

Perfis principais:

- Cliente.
- Produtor/agricultor.
- Administrador.

Regras gerais:

- Cliente pode comprar, favoritar e avaliar.
- Produtor pode cadastrar produtos e gerenciar seus pedidos.
- Administrador pode ter permissões mais amplas.
- Cliente comum não deve cadastrar produto.
- Produtor não deve editar produto de outro produtor.

## Categorias de produto

- A leitura de categorias é pública; categorias inativas também são visíveis como sugestões pendentes.
- O filtro `?ativo=true` deve retornar somente categorias ativas para seleção e filtros do catálogo.
- Somente produtor autenticado pode criar sugestão de categoria, que deve ser persistida como inativa.
- Administrador (`is_staff`) pode criar categorias ativas, renomear, ativar e inativar categorias.
- Categorias não possuem exclusão por API.
- Criação de produto exige categoria ativa. Em edição, uma categoria inativa só é aceita quando já é o vínculo
  existente e o campo `categoria` não é alterado.
- A listagem de produtos aceita `?categoria=<categoria_id>` para filtrar pela categoria única do produto.

## Padrão para alterações

Ao alterar backend:

1. Identificar app afetado.
2. Verificar models.
3. Verificar serializers.
4. Verificar views/viewsets.
5. Verificar urls.
6. Verificar permissions.
7. Verificar admin, se aplicável.
8. Verificar testes.
9. Verificar impacto no frontend.
10. Criar migration se necessário.

## Boas práticas

- Manter regras críticas no backend.
- Retornar mensagens de erro claras.
- Evitar funções grandes.
- Usar transações em operações críticas, como criação de pedidos.
