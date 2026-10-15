---
name: agro-regras-de-negocio
description: "Regras de negócio centrais do Agro Store: usuários e cadastro, produtor e loja, produtos, SKU e imagens, preços, carrinho, finalização com split por loja, pedidos e status, retirada na feira, favoritos, avaliações e regras pendentes. Use sempre que uma tarefa tocar ou questionar uma regra de negócio."
---

> Origem: `skills/business-rules.md`. Referências a `.ai/skills/*.md` correspondem às skills `agro-*` desta pasta.

# Skill: Regras de Negócio

## Objetivo

Centralizar e orientar as regras de negócio do Agro Store.

Esta skill substitui a ideia inicial de `cart-and-orders.md`, pois o projeto deve concentrar regras de negócio em um local único e expansível.

Sempre que uma nova regra de negócio for identificada, ela deve ser adicionada ou refletida neste arquivo.

## Princípios gerais

- O Agro Store é um MVP para TCC.
- O sistema deve priorizar funcionalidades essenciais.
- Não implementar funcionalidades fora do escopo sem validação.
- Regras críticas devem ser validadas no backend.
- O frontend pode exibir cálculos e melhorar a experiência do usuário, mas não deve ser a única camada de validação.
- Sempre questionar quando houver dúvida sobre regra de negócio.

## Usuários e autenticação

- O login é feito por usuário.
- O papel do usuário é definido por permissões e propriedades do perfil.
- O usuário pode atuar como cliente, produtor/agricultor ou administrador.
- O cliente precisa criar conta para comprar, favoritar produtos e usar o carrinho.
- O produtor/agricultor precisa estar autenticado para cadastrar produtos.
- Usuários não autenticados podem visualizar áreas públicas, quando liberadas.
- O cadastro público cria somente contas de cliente e deve retornar tokens JWT para iniciar a sessão automaticamente.
- O cadastro exige nome, CPF válido e único, e-mail único, celular brasileiro com 11 dígitos, data de nascimento,
  gênero e senha com no mínimo 8 caracteres. O cliente deve ter pelo menos 16 anos.
- CPF e telefone são persistidos somente com dígitos. CPF, e-mail, idade e telefone são validados no backend.
- O cadastro não aceita campos de privilégios, incluindo `is_produtor`, `is_staff` ou permissões.
- O cadastro de cliente não cria loja nem inicia solicitação para perfil de produtor.
- Cadastro, aprovação de produtor, ativação de loja e notificações administrativas serão definidos em tarefa futura.
- No perfil, o usuário pode alterar nome, e-mail, celular, data de nascimento, gênero e foto de perfil, com as mesmas validações do cadastro.
  CPF e papéis (`is_produtor`, `is_staff`) não podem ser alterados pelo próprio usuário.
- Foto de perfil (RN-018): todo usuário (cliente ou produtor) pode ter uma única foto de perfil, opcional, enviada, trocada ou removida
  (sem precisar enviar outra) somente pelo próprio usuário na tela de perfil. Sem foto, o sistema exibe as iniciais do nome.
  A foto é exibida apenas ao próprio usuário (perfil e menu da conta); não aparece em avaliações, pedidos ou na área do produtor.
  As regras comuns de arquivo estão em "Imagem da loja e foto de perfil" na seção do produtor e da loja.
- Alterar o perfil não muda pedidos já realizados: eles mantêm o snapshot dos dados do cliente.
- O usuário que não é produtor vê apenas uma orientação para procurar a organização da feira; o frontend não oferece criação de loja para ele.

## Produtor, agricultor e loja

- O produtor/agricultor representa quem vende produtos na plataforma.
- A entidade `loja` pode representar o espaço comercial do produtor/agricultor.
- Um produtor/agricultor pode cadastrar e administrar seus próprios produtos.
- Um produtor/agricultor não deve administrar produtos de outro produtor.
- O produtor/agricultor deve visualizar apenas pedidos relacionados à sua própria loja/produtor.
- Uma loja por produtor (RN-013): decisão v1: cada produtor pode possuir somente uma loja.
  A regra é validada na API, que recusa a criação de uma segunda loja com mensagem clara, e também garantida no banco,
  que impede duas lojas com o mesmo proprietário mesmo em pedidos simultâneos.
  Múltiplas lojas por produtor ficam para o futuro e dependem de nova decisão.
- Produtor com loja não pode ser excluído (RN-013): enquanto possuir loja, o produtor não pode ser excluído, tenha ou não pedidos;
  a exclusão é recusada e a loja e os produtos são preservados. A loja nunca é apagada em cascata junto com o usuário.
  O encerramento da atividade do produtor é feito pela desativação da loja e, se for o caso, pela inativação do usuário pelo administrador,
  preservando o histórico.
- O produtor pode alterar o nome, a descrição e a imagem e desativar sua própria loja. CNPJ e proprietário não são alterados por essa área.
  A desativação preserva o histórico e impede novas compras.
- Imagem da loja (RN-018): cada loja pode ter uma única imagem, opcional, que pode ser escolhida já na criação da loja ou enviada depois
  na área do produtor. Se a imagem enviada na criação for inválida, a loja não é criada e o produtor corrige o arquivo.
  Somente o proprietário da loja envia, troca ou remove a imagem; a remoção é permitida sem enviar outra.
  Sem imagem, o sistema exibe um marcador neutro com a inicial do nome da loja.
  A imagem aparece na página pública da loja, no detalhe do produto (junto ao nome da loja) e na área do produtor;
  os cards do catálogo continuam mostrando a imagem principal do produto. A desativação da loja não apaga a imagem.
- Imagem da loja e foto de perfil, regras comuns (RN-018): o backend aceita apenas JPG, PNG ou WEBP de até 5 MB, conferindo
  extensão e conteúdo, e renomeia o arquivo com nome aleatório (mesmas validações da RN-016). Mensagens de recusa:
  "Envie uma imagem JPG, PNG ou WEBP válida." e "A imagem deve ter no máximo 5 MB."; quando o envio é recusado, a imagem atual é mantida.
  Diferente da imagem do produto, enviar uma nova imagem substitui a anterior. O arquivo anterior é removido do storage ao trocar
  ou remover, mas só é removido se não for usado por outra loja.
  Os arquivos ficam no disco local em desenvolvimento e no Supabase Storage em produção.
  A imagem da loja e a foto do usuário não fazem parte do snapshot do pedido; trocá-las ou removê-las não altera pedidos já realizados.
  Os valores já existentes em `Loja.imagem_perfil` são preservados na mudança do campo; um valor que não aponta para arquivo válido
  é exibido como "sem imagem", sem apagar o dado.
  Nenhuma permissão administrativa nova é criada para essas imagens; a moderação pelo administrador é trabalho futuro.

## Produtos

- Somente produtor/agricultor cadastra produtos.
- Produtos pertencem a uma loja/produtor.
- Todo produto deve possuir exatamente uma categoria.
- Subcategorias não fazem parte do modelo atual do MVP.
- Categorias ativas podem ser usadas em novos cadastros e na troca de categoria de um produto.
- Produto já vinculado a uma categoria inativa continua visível e pode ter seus demais dados editados.
- Categoria inativa não deve ocultar produto do catálogo nem impedir sua compra por si só.
- Categorias não podem ser excluídas; devem ser inativadas quando não puderem receber novos produtos.
- Produtor pode sugerir uma categoria, que deve nascer inativa e ficar visível publicamente.
- Somente administrador pode criar categoria já ativa, renomear, ativar ou inativar categorias.
- Produto inativo não deve aparecer como disponível para compra.
- Produtos não são excluídos: o produtor os desativa (e pode reativá-los). A exclusão apagaria itens de pedidos já realizados.
- Produto sem estoque suficiente não deve ser comprado.
- Estoque zerado no catálogo (RN-017): produto com estoque 0 não aparece na listagem nem na busca do catálogo público.
  O detalhe pelo link direto continua acessível, com "Sem estoque" e a compra bloqueada. O campo `ativo` não é alterado.
- Estoque baixo (RN-017): limite único e global de 5 unidades. Produto com estoque de 1 a 5 é sinalizado ao produtor na área do produtor.
  É só um indicador visual; a notificação ativa (e-mail/push) continua como trabalho futuro.
- Estoque não negativo (RN-017): o estoque do produto não pode ser negativo. A API recusa valor negativo com mensagem clara.
  A trava equivalente no banco ainda está pendente e será feita em tarefa própria de banco.
- SKU, código de barras, CPF e CNPJ devem ser tratados como texto.
- O SKU de cada produto novo é gerado automaticamente e não pode ser alterado. O formato possui 14 dígitos, sem separadores: `id_loja` com 4 dígitos, `id_categoria` com 4 dígitos e `id_produto` com 6 dígitos. Exemplo: loja 1, categoria 1 e produto 1 geram `00010001000001`.
- Produtos existentes preservam o SKU que já possuem.
- Imagens do produto (RN-016): cada produto pode ter de 0 a 5 imagens, opcionais, com uma ordem de exibição definida pelo produtor.
  Quando houver imagem, exatamente uma é a principal: a primeira enviada vira principal automaticamente, definir outra principal desmarca a anterior
  e, ao excluir a principal, a próxima pela ordem é promovida. O banco impede duas imagens principais no mesmo produto.
  A imagem principal é usada no catálogo, nos cards e na lista do produtor; o detalhe do produto exibe todas, começando pela principal.
  Somente o produtor dono do produto (ou administrador) envia, ordena, define a principal ou exclui imagens; a leitura segue a visibilidade do produto.
  O backend aceita apenas JPG, PNG ou WEBP de até 5 MB, conferindo extensão e conteúdo, e renomeia o arquivo com nome aleatório.
  Uma imagem enviada não é substituída: para trocá-la, o produtor exclui a imagem e envia outra. O arquivo excluído é removido do storage.
  Os arquivos ficam no disco local em desenvolvimento e no Supabase Storage em produção.
  O campo legado `Produto.imagem` foi migrado para a imagem principal e não é mais usado pela API; sua remoção depende de autorização.
- Valores financeiros devem usar Decimal no backend.

## Preços

- Produtos podem possuir histórico de preços.
- O preço vigente deve ser considerado no momento da compra.
- O backend deve validar o preço final no fechamento do pedido.
- O frontend pode apenas exibir totais para facilitar a experiência do usuário.

## Carrinho

- O carrinho deve ser salvo no backend.
- O cliente precisa estar autenticado para usar o carrinho.
- Produto repetido no carrinho deve somar quantidade, não criar item duplicado.
- Quantidade e estoque (RN-017): o cliente escolhe uma quantidade de 1 até o estoque do produto.
  Quando o estoque diminui (pedido de outro cliente ou edição do produtor), o sistema reduz para o estoque atual a quantidade
  de todos os carrinhos que passaram dele, podendo chegar a 0. Esse ajuste é gravado no banco.
  Item com quantidade 0 permanece no carrinho como "Sem estoque" e não pode ser finalizado.
  A reposição do estoque não restaura a quantidade anterior.
- O carrinho pode conter produtos de diferentes produtores/lojas.
- O frontend pode calcular totais para exibição.
- A validação final dos valores deve ocorrer no backend.
- Decisão v1: a implementação atual mantém um carrinho por cliente e por loja no backend, e o frontend agrega esses carrinhos para exibição.
- Decisão v1: a padronização completa para um carrinho único por cliente, como sugerido nos diagramas, fica para uma task futura com migration aprovada.

## Finalização do carrinho

Ao finalizar o carrinho, o backend deve:

1. Buscar itens do usuário autenticado.
2. Validar se o carrinho possui itens.
3. Validar se os produtos estão ativos.
4. Validar estoque disponível.
5. Buscar preço vigente.
6. Agrupar itens por loja/produtor.
7. Criar um pedido separado para cada loja/produtor.
8. Criar os itens de cada pedido.
9. Criar snapshot dos dados do cliente.
10. Criar snapshot dos dados dos produtos.
11. Baixar estoque ao gerar o pedido.
12. Ajustar os carrinhos de outros clientes afetados pela baixa de estoque (RN-017).
13. Remover do carrinho os itens finalizados.
14. Retornar os pedidos criados.
- Decisão v1: a finalização recebe os itens selecionados do carrinho e finaliza apenas esses itens.
- RN-017: item do carrinho com quantidade 0 ("Sem estoque") não pode ser finalizado. Se os itens enviados incluírem um item com
  quantidade 0, a finalização inteira é recusada, informando o produto, e nenhum pedido é criado
  (mesmo comportamento usado para estoque insuficiente ou produto inativo).

## Pedidos

- Ao finalizar o carrinho, o sistema deve separar os itens por produtor/loja.
- Deve ser criado um pedido separado para cada produtor/loja.
- O pedido deve preservar snapshot dos dados do cliente.
- O pedido deve preservar snapshot dos dados do produto.
- O cliente deve visualizar apenas seus próprios pedidos.
- O produtor/agricultor deve visualizar apenas pedidos relacionados aos seus produtos ou loja.
- O pedido representa uma solicitação para retirada presencial na feira.
- Preservação do histórico (RN-019): usuário ou loja que tenha pedidos não pode ser excluído, para preservar o histórico de pedidos.
  Todo pedido fica vinculado ao cliente que o fez e à loja que o recebeu, e esses vínculos impedem a exclusão.
  O bloqueio vale para o cliente com pedidos e para o produtor cuja loja tenha pedidos: ao excluir esse usuário pelo admin do Django,
  a exclusão é recusada e os pedidos que a impedem são exibidos.
  A loja não tem exclusão própria, nem no admin nem na API, e não é excluída junto com o produtor dono:
  produtor com loja não pode ser excluído, mesmo sem pedidos (RN-013). A API também não oferece exclusão de usuário.
  Usuário com pedidos nunca é excluído: para encerrar seu acesso, o administrador o desativa e a conta é mantida.
  Pedidos não são excluídos nem editados (snapshot, itens e valores) pela área administrativa, que os mantém apenas para consulta;
  para encerrar um pedido, usa-se o status `Cancelado`.
  Para encerrar a atividade de uma loja, o caminho é a desativação, que preserva o histórico e impede novas compras.

## Exemplo de split de pedidos

```text
Carrinho:
- Produto A — Produtor 1
- Produto B — Produtor 1
- Produto C — Produtor 2

Resultado:
- Pedido 1 para Produtor 1
- Pedido 2 para Produtor 2
```

## Pagamento

Não existe pagamento online no MVP.

Não implementar sem autorização:

- Pix.
- Cartão.
- Gateway de pagamento.
- Confirmação automática de pagamento.
- Integração financeira.

## Retirada

- A retirada é presencial na feira.
- Não implementar entrega em domicílio no MVP.
- Não implementar cálculo de frete no MVP.
- Não implementar endereço de entrega no MVP, salvo se for aprovado como informação complementar do cadastro.
- Decisão v1 (RN-008): a feira ocorre todos os sábados, das 6h às 12h, na Rua Major Lúcio Meireles, nº 61, Centro, Camaquã (junto ao prédio nos fundos da Igreja Imaculada / escritório da Emater).
- O dia e o horário da feira são uma configuração única e global da plataforma, não variam por loja/produtor.
- A informação é apenas exibida ao cliente (catálogo/carrinho/pedidos); o backend não valida nem bloqueia a criação de pedidos fora desse dia/horário no MVP.

## Status do pedido

Status esperados:

- Pendente.
- Em preparo.
- Pronto para retirada.
- Entregue.
- Cancelado.

Fluxo sugerido:

```text
Pendente -> Em preparo -> Pronto para retirada -> Entregue
Pendente -> Cancelado
Em preparo -> Cancelado
```

Decisão v1: o produtor deve respeitar estritamente esse fluxo ao atualizar pedidos da sua própria loja.
Na área do produtor, o quadro de pedidos só permite avançar para o próximo status ou cancelar quando o fluxo permite; não há retorno de status.
Para organizar a retirada, o produtor pode consultar somente nome e telefone do cliente no pedido.

- O cliente pode cancelar somente pedidos próprios com status `Pendente`.
- O cancelamento é imediato, preserva o pedido no histórico como `Cancelado` e não exige motivo no MVP.
- Todo cancelamento autorizado, feito pelo cliente ou produtor, restaura uma única vez o estoque de cada item do pedido.

## Favoritos

- Qualquer usuário autenticado, incluindo produtor, pode favoritar produtos.
- Um mesmo produto não deve ser favoritado mais de uma vez pelo mesmo usuário.
- Favoritos devem ser vinculados ao usuário autenticado.
- Produtos favoritos inativos, sem estoque ou com loja inativa permanecem visíveis, mas não podem ser adicionados ao carrinho.

## Avaliações

- Avaliação de produto comprado (RN-010): somente o usuário autenticado dono do pedido pode avaliar um item desse pedido,
  e somente quando o pedido estiver com status `Entregue`. Vale para qualquer usuário que compre, incluindo o produtor.
  A avaliação é feita por item de pedido; o backend vincula automaticamente o produto do item e o usuário autenticado.
- Cada item de pedido pode ser avaliado uma única vez (o banco também impede duplicidade). Se o mesmo produto foi comprado
  em pedidos diferentes, cada item entregue pode receber sua própria avaliação.
- A avaliação possui nota inteira de 1 a 5 e comentário opcional, com até 500 caracteres. Mensagens de recusa: "Este item não pertence ao seu pedido.",
  "Só é possível avaliar pedidos entregues.", "Este item já foi avaliado." e "O comentário deve ter no máximo 500 caracteres.".
- As avaliações são públicas: qualquer visitante vê, no detalhe do produto, a lista de avaliações e a média das notas.
  A API já retorna o nome do avaliador abreviado (primeiro nome e inicial do sobrenome); o nome completo não é exposto.
  As avaliações continuam visíveis mesmo que o produto ou a loja sejam desativados.
- Decisão v1: a média é calculada apenas para exibição, no detalhe do produto; não há média armazenada nem exibida no catálogo.
- Decisão v1: depois de enviada, a avaliação não pode ser editada nem removida pelo autor; não existe edição de avaliação.
  Somente o administrador pode remover uma avaliação, como moderação, pela área administrativa.
  Depois de removida pelo administrador, uma nova avaliação pode ser enviada para o mesmo item de pedido.

## Administração

- Administradores podem ter permissões mais amplas.
- Regras administrativas devem ser tratadas com cuidado para não liberar ações indevidas.
- Não criar permissões administrativas novas sem validar necessidade.

## Cuidados ao alterar regras de negócio

Antes de alterar uma regra, avaliar impacto em:

- Models.
- Serializers.
- Views/ViewSets.
- Permissions.
- Rotas.
- Services do frontend.
- Stores do frontend.
- Telas afetadas.
- Testes.
- Documentação técnica.
- Texto do TCC.

## Regras futuras

Adicionar novas regras abaixo conforme o projeto evoluir.

### Indicadores da área do produtor

- Vendas do mês, pedidos no mês, ticket médio, vendas dos últimos 7 dias e produtos mais vendidos consideram somente pedidos
  não cancelados, agrupados pela data de criação do pedido.
- Os indicadores são calculados no frontend apenas para acompanhamento e não substituem relatórios ou validações do backend.

### Loja e imagens (fora da RN-018)

- Cidade e contato da loja serão definidos em tarefa própria (DB-013); não fazem parte da RN-018.
- Moderação de imagens de loja e de usuário pelo administrador.
- Logo e capa separadas da loja (no MVP, cada loja tem uma única imagem).
- Imagem da loja nos cards do catálogo.

### Dados pessoais (fora do MVP)

- Anonimização dos dados pessoais de usuário com pedidos que peça a exclusão da conta (LGPD), preservando o histórico de pedidos.

### Regras pendentes de definição
- Se o produtor poderá recusar pedido.
- Como o cliente solicitará a habilitação de produtor rural.
