# Diagramas do TCC (fontes Mermaid)

Os arquivos `.mmd` desta pasta são a fonte dos diagramas do TCC. O `docs/TCC.md` é convertido para .docx/PDF,
e essa conversão não renderiza Mermaid. Por isso, cada diagrama é exportado como PNG e o texto do TCC aponta
para a imagem. Ao mudar um diagrama, edite o `.mmd` e exporte o PNG de novo.

## Como exportar para PNG (Mermaid Live Editor)

1. Abra <https://mermaid.live>.
2. Apague o conteúdo do painel **Code** e cole o conteúdo inteiro do arquivo `.mmd`.
3. Confira a pré-visualização. Se houver erro de sintaxe, ele aparece abaixo do código.
4. Em **Actions**, use **PNG** para baixar a imagem.
5. Salve nesta pasta com o mesmo nome do `.mmd`, trocando a extensão para `.png`.
   Exemplo: `fig02-modelo-logico.mmd` gera `fig02-modelo-logico.png`.

Não é preciso instalar nenhuma dependência.

## Correspondência com as figuras do TCC

| Arquivo | Figura no TCC | Tipo |
| --- | --- | --- |
| — | Figura 1 - Modelo Conceitual (DER) | Mantido em notação de Chen, fora do Mermaid (responsabilidade do autor) |
| `fig02-modelo-logico.mmd` | Figura 2 - Modelo Lógico | `erDiagram` |
| `fig03-casos-de-uso.mmd` | Figura 3 - Diagrama de Casos de Uso | `flowchart LR` (aproximação) |
| `fig04-seq-cadastro.mmd` | Figura 4 - Diagrama de Sequência I - Cadastro de Usuário | `sequenceDiagram` |
| `fig05-seq-login.mmd` | Figura 5 - Diagrama de Sequência II - Acesso ao Sistema | `sequenceDiagram` |
| `fig06-seq-cadastro-loja.mmd` | Figura 6 - Diagrama de Sequência III - Cadastro de Loja | `sequenceDiagram` |
| `fig07-seq-produto-preco.mmd` | Figura 7 - Diagrama de Sequência IV - Produto e Preço | `sequenceDiagram` |
| `fig08-seq-catalogo.mmd` | Figura 8 - Diagrama de Sequência V - Catálogo | `sequenceDiagram` |
| `fig09-atividades-pedido.mmd` | Figura 9 - Diagrama de Atividades I - Geração de Pedido | `flowchart TD` (aproximação) |
| `fig10-estados-pedido.mmd` | Figura 10 - Diagrama de Estados do Pedido (Seção 4.2) | `stateDiagram-v2` |
| `fig11-seq-imagens-produto.mmd` | Figura 11 - Diagrama de Sequência VI - Imagens do Produto (Seção 4.3) | `sequenceDiagram` |
| `fig12-seq-avaliacao.mmd` | Figura 12 - Diagrama de Sequência VII - Avaliação de Item Entregue (Seção 4.6) | `sequenceDiagram` |

No `docs/TCC.md`, as figuras apontam para `diagramas/figNN-*.png`, um caminho relativo à pasta `docs/`. Ao converter com o pandoc,
execute o comando a partir de `docs/` ou informe `--resource-path=docs`.

## Observações

- Os diagramas seguem o código implementado (models, views e serializers do backend). Os comentários `%%`
  de cada arquivo indicam onde o fluxo foi conferido e onde o `docs/modelo-logico.sql` (modelo-alvo) diverge.
- Os caminhos de endpoint nos diagramas de sequência partem de `/api/v1/`.
