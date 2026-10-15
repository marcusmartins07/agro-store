INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA SUL-RIO-GRANDENSE

CAMPUS CAMAQUÃ

TECNÓLOGO EM ANÁLISE E DESENVOLVIMENTO DE SISTEMAS

Marcus Vinícius da Silva Martins

**Agro Store: Plataforma Digital de Comercialização B2C para Produtores Rurais**

Camaquã, RS

2026

Marcus Vinícius da Silva Martins

**[Agro Store - Plataforma Digital de Comercialização B2C para Produtores Rurais]{.smallcaps}**

> Trabalho de Conclusão de Curso apresentado como requisito parcial à obtenção do título de Tecnólogo do Curso Análise e Desenvolvimento de Sistemas do Instituto Federal Sul-rio-grandense -- Camaquã.
>
> Orientador(a): Prof. Marcelo Gonçalves de Souza

Camaquã

2026

Marcus Vinícius da Silva Martins

**AGRO STORE -** Plataforma Digital de Comercialização B2C para Produtores Rurais

> Trabalho de Conclusão de Curso apresentado como requisito parcial à obtenção do título de Tecnólogo em Análise e Desenvolvimento de Sistemas, do Instituto Federal Sul-rio-grandense -- Câmpus Camaquã.
>
> Orientador(a): Prof. Marcelo Gonçalves de Souza

**Banca Examinadora**

Prof. Marcelo Gonçalves de Souza

Orientador

Instituto Federal Sul-rio-grandense -- Câmpus Camaquã

Prof. Diego Pereira

Avaliador

Instituto Federal Sul-rio-grandense -- Câmpus Camaquã

Prof. Geraldo Barbosa

Avaliador

Instituto Federal Sul-rio-grandense -- Câmpus Camaquã

**RESUMO**

Este trabalho apresenta o desenvolvimento do Agro Store, uma plataforma digital de comercialização voltada aos produtores rurais participantes da Feira do Produtor Rural Willi Dummer, no município de Camaquã/RS. A proposta surgiu da observação da dinâmica presencial da feira, realizada apenas nas manhãs de sábado, o que limita o alcance comercial dos produtores e dificulta a organização antecipada dos pedidos. A pesquisa caracteriza-se como aplicada, de natureza qualitativa e com abordagem de desenvolvimento de software, sendo conduzida por meio do levantamento de requisitos, da modelagem do sistema e da implementação da solução. A modelagem contempla o Diagrama Entidade-Relacionamento, o modelo lógico do banco de dados e diagramas UML representando os principais fluxos da aplicação. A solução utiliza arquitetura desacoplada, com API REST desenvolvida em Python com Django REST Framework, frontend em Vue.js, banco de dados PostgreSQL e autenticação por tokens JWT, contemplando perfis distintos para cliente, produtor e administrador. Espera-se que o sistema contribua para ampliar a visibilidade dos produtos rurais, facilitar a gestão de pedidos e fortalecer a economia local.

**Palavras-chave:** Agro Store; agricultura familiar; produtores rurais; desenvolvimento web; comercialização digital.

**ABSTRACT**

This work presents the development of Agro Store, a digital commercialization platform aimed at rural producers participating in the Willi Dummer Rural Producer Fair, in the municipality of Camaquã/RS. The proposal arose from the observation of the fair's in-person dynamics, held only on Saturday mornings, which limits the producers' commercial reach and makes it difficult to organize orders in advance. The research is characterized as applied, qualitative in nature, and based on a software development approach, being conducted through requirements gathering, system modeling, and solution implementation. The modeling includes the Entity-Relationship Diagram, the logical database model, and UML diagrams representing the main application flows. The solution uses a decoupled architecture, with a REST API developed in Python using Django REST Framework, a Vue.js frontend, a PostgreSQL database, and JWT token-based authentication, including distinct profiles for customer, producer, and administrator. It is expected that the system will contribute to increasing the visibility of rural products, facilitating order management, and strengthening the local economy.

**Keywords:** Agro Store; family farming; rural producers; web development; digital commercialization.

# 

# 

# 

# 

# 

# 

# 

# 

**LISTA DE FIGURAS**

[Figura 1 - Modelo Conceitual do Diagrama Entidade-Relacionamento 24](#figura-1---modelo-conceitual-do-diagrama-entidade-relacionamento)

[Figura 2 - Modelo Lógico do Diagrama Entidade-Relacionamento 26](#figura-2---modelo-lógico-do-diagrama-entidade-relacionamento)

[Figura 3 - Diagrama de Casos de Uso 30](#figura-3---diagrama-de-casos-de-uso)

[Figura 4 - Diagrama de Sequência I - Cadastro de Usuário 32](#figura-4---diagrama-de-sequência-i---cadastro-de-usuário)

[Figura 5 - Diagrama de Sequência I - Acesso ao Sistema 34](#figura-5---diagrama-de-sequência-ii---acesso-ao-sistema)

[Figura 6 - Diagrama de Sequência III - Cadastro de Loja pelo Produtor 36](#figura-6---diagrama-de-sequência-iii---cadastro-de-loja-pelo-produtor)

[Figura 7 - Diagrama de Sequência IV - Cadastro de Produto e Definição de Preço 38](#figura-7---diagrama-de-sequência-iv---cadastro-de-produto-e-definição-de-preço)

[Figura 8 - Diagrama de Sequência V - Consulta de Catálogo de Produtos 39](#figura-8---diagrama-de-sequência-v---consulta-de-catálogo-de-produtos)

[Figura 9 - Diagrama de Atividades I - Geração de Pedido pelo Cliente 42](#figura-9---diagrama-de-atividades-i---geração-de-pedido-pelo-cliente)

**LISTA DE QUADROS**

Quadro 1 - Cronograma de atividades 43

**LISTA DE ABREVIATURAS E SIGLAS**

API Application Programming Interface

CNPJ Cadastro Nacional da Pessoa Jurídica

CPF Cadastro de Pessoas Físicas

DER Diagrama Entidade-Relacionamento

DOM Document Object Model

DRF Django REST Framework

HTTP Hypertext Transfer Protocol

IBGE Instituto Brasileiro de Geografia e Estatística

JSON JavaScript Object Notation

JWT JSON Web Token

MTV Model-Template-View

MVC Model-View-Controller

ORM Object-Relational Mapping

REST Representational State Transfer

SKU Stock Keeping Unit

SQL Structured Query Language

UML Unified Modeling Language

**SUMÁRIO**

[**1 INTRODUÇÃO 11**](#introdução)

> [**1.1 Objetivos** 11](#objetivos)
>
> [1.1.1 Objetivo Geral 11](#objetivo-geral)
>
> [1.1.2 Objetivos Específicos 11](#objetivos-específicos)
>
> [**1.2 Justificativa** 12](#justificativa)

[**2 FUNDAMENTAÇÃO TEÓRICA 12**](#fundamentação-teórica)

> [**2.1 Agricultura Familiar e Feiras de Produtores Rurais** 13](#agricultura-familiar-e-feiras-de-produtores-rurais)
>
> [**2.2 Plataformas Digitais de Comercialização** 13](#plataformas-digitais-de-comercialização)
>
> [**2.3 Modelo B2C** 14](#modelo-b2c)
>
> [**2.4 Ferramentas e Tecnologias Utilizadas** 14](#ferramentas-e-tecnologias-utilizadas)
>
> [2.4.1 Aplicação Web 14](#aplicação-web)
>
> [2.4.2 API e REST 15](#api-e-rest)
>
> [2.4.3 Python 15](#python)
>
> [2.4.4 Django e Django REST Framework 15](#django-e-django-rest-framework)
>
> [2.4.5 Vue.js 16](#vue.js)
>
> [2.4.6 PostgreSQL 16](#postgresql)
>
> [2.4.7 MVC e MTV 16](#mvc-e-mtv)
>
> [2.4.8 JSON 17](#json)
>
> [2.4.9 JWT 17](#jwt)

[**3 METODOLOGIA 17**](#metodologia)

> [**3.1 Requisitos** 17](#requisitos)
>
> [3.1.1 Requisitos Funcionais 17](#requisitos-funcionais)
>
> [3.1.2 Requisitos não funcionais 18](#requisitos-não-funcionais)
>
> [**3.2 Modelagem** 19](#modelagem)
>
> [3.2.1 Confecção de Diagramas 19](#confecção-de-diagramas)
>
> [3.2.2 Modelagem do Banco de Dados 19](#modelagem-do-banco-de-dados)
>
> [3.2.3 Diagrama Entidade-Relacionamento (DER) 20](#diagrama-entidade-relacionamento-der)
>
> [3.2.4 Modelo Lógico 25](#modelo-lógico)
>
> [3.2.5 Diagramas UML 27](#diagramas-uml)
>
> [3.2.5.1 Diagrama de Casos de Uso 27](#diagrama-de-casos-de-uso)
>
> [3.2.5.2 Diagramas de Sequência 31](#diagramas-de-sequência)
>
> [3.2.5.2.1 Diagrama de Sequência I - Cadastro de Usuário 31](#diagrama-de-sequência-i---cadastro-de-usuário)
>
> [3.2.5.2.2 Diagrama de Sequência II - Acesso ao Sistema 32](#diagrama-de-sequência-ii---acesso-ao-sistema)
>
> [3.2.5.2.3 Diagrama de Sequência III - Cadastro de Loja pelo Produtor 34](#diagrama-de-sequência-iii---cadastro-de-loja-pelo-produtor)
>
> [3.2.5.2.4 Diagrama de Sequência IV - Cadastro de Produto e Definição de Preço 36](#diagrama-de-sequência-iv---cadastro-de-produto-e-definição-de-preço)
>
> [3.2.5.2.5 Diagrama de Sequência V - Consulta de Catálogo de Produtos 38](#diagrama-de-sequência-v---consulta-de-catálogo-de-produtos)
>
> [3.2.5.3 Diagrama de Atividades 39](#diagrama-de-atividades)
>
> [3.2.5.3.1 Diagrama de Atividades I - Geração de Pedido pelo Cliente 40](#diagrama-de-atividades-i---geração-de-pedido-pelo-cliente)

[**4 CRONOGRAMA 43**](#cronograma)

# [1 INTRODUÇÃO]{.smallcaps} {#introdução}

O presente trabalho propõe o desenvolvimento do Agro Store, uma plataforma digital voltada à intermediação de pedidos entre consumidores e produtores rurais participantes da Feira do Agricultor do município de Camaquã/RS. A iniciativa surgiu da observação direta do evento, realizado semanalmente às manhãs de sábado, onde foi possível constatar a ausência de ferramentas digitais nos processos de divulgação e comercialização dos produtos ofertados pelos agricultores locais.

A feira do agricultor representa uma importante fonte de renda para pequenos produtores da região, mas sua dinâmica presencial e o horário restrito limitam significativamente o alcance das vendas. Sem um canal digital, os produtores perdem oportunidades de negócio fora do período do evento e enfrentam dificuldades para organizar seus pedidos com antecedência. Essa lacuna motivou a proposta de um sistema que permitisse gerenciar os quatro pilares essenciais da cadeia comercial: o produtor rural, o produto, o cliente e a venda.

## 1.1 Objetivos {#objetivos}

Nas seções abaixo estão descritos o objetivo geral e os objetivos específicos desta pesquisa.

### 1.1.1 Objetivo Geral {#objetivo-geral}

Desenvolver uma plataforma digital para intermediar pedidos entre consumidores e produtores rurais da Feira do Agricultor de Camaquã/RS, permitindo o cadastro de produtos, a realização de pedidos e o acompanhamento do status de cada venda, com perfis distintos para produtor, cliente e administrador, utilizando Django REST Framework no backend e Vue.js no frontend, com retirada dos pedidos na própria feira.

### 1.1.2 Objetivos Específicos {#objetivos-específicos}

Para alcançar o objetivo geral, foram definidos os seguintes objetivos específicos:

- Realizar pesquisa bibliográfica sobre agricultura familiar, feiras de produtores rurais, plataformas digitais B2C e tecnologias de desenvolvimento web;

- Realizar o levantamento dos requisitos funcionais e não funcionais do sistema, com base na observação da dinâmica da feira do agricultor de Camaquã/RS;

- Modelar o banco de dados do sistema, elaborando os diagramas entidade-relacionamento conceitual e lógico;

- Confeccionar os diagramas UML do sistema, incluindo diagrama de casos de uso, diagramas de sequência e diagramas de atividades;

- Desenvolver a API REST utilizando Python com Django REST Framework, implementando os endpoints para cada funcionalidade do sistema;

- Desenvolver o frontend da aplicação utilizando Vue.js, com as interfaces para os usuários.

## 1.2 Justificativa {#justificativa}

A Feira do Produtor Rural Willi Dummer, em Camaquã, é uma importante fonte de renda para pequenos produtores da região, porém fica limitada ao formato presencial e ao horário restrito de funcionamento, das 6h às 12h de sábado (SILVA, 2025). Sem uma plataforma digital, esses produtores perdem vendas e têm dificuldade de organizar seus pedidos fora do evento. O sistema proposto pode contribuir para o aumento da renda desses produtores e para a movimentação da economia local, ampliando o alcance dos produtos além do dia de feira.

Do ponto de vista acadêmico, o trabalho envolve conceitos fundamentais do curso de Tecnólogo em Análise e Desenvolvimento de Sistemas, como modelagem de banco de dados relacional, desenvolvimento de APIs REST, controle de acesso por perfis de usuário e construção de interfaces web. A integração entre um backend construído em Django REST Framework e um frontend em Vue.js demonstra na prática a arquitetura de sistemas desacoplados, amplamente utilizada no mercado de desenvolvimento de software.

# 

# 

# 

# [2 FUNDAMENTAÇÃO TEÓRICA]{.smallcaps} {#fundamentação-teórica}

O desenvolvimento do Agro Store apoia-se em um conjunto de conceitos e tecnologias que, articulados, sustentam tanto as decisões de projeto quanto as escolhas técnicas adotadas ao longo do trabalho. Este capítulo percorre esse embasamento em três eixos: o papel da agricultura familiar e das feiras de produtores rurais no Brasil como contexto que motivou a solução; o modelo de marketplace e plataforma digital B2C como referência para a arquitetura de comercialização proposta; e as principais ferramentas e tecnologias empregadas na construção do sistema.

## 2.1 Agricultura Familiar e Feiras de Produtores Rurais {#agricultura-familiar-e-feiras-de-produtores-rurais}

A agricultura familiar é definida pela Lei n.º 11.326/2006 como a atividade agropecuária praticada em estabelecimento rural de até quatro módulos fiscais, sob gestão direta da família, com mão de obra predominantemente familiar (BRASIL, 2006). Os dados do Censo Agropecuário de 2017 evidenciam o peso desse segmento na estrutura agrária brasileira: a agricultura familiar representa 77% dos estabelecimentos rurais do país e responde por 67% da produção nacional de feijão, 70% da produção de mandioca e 34% do leite produzido no Brasil (IBGE, 2019).

No município de Camaquã/RS, a Feira do Produtor Rural Willi Dummer acontece semanalmente, reunindo produtores locais que comercializam hortifrutigranjeiros, produtos artesanais e derivados da agricultura familiar, com funcionamento das 6h às 12h de sábado (SILVA, 2025).

Ainda que economicamente relevantes, essas feiras operam sem suporte digital. Sem canais de venda online, o alcance dos produtores fica restrito ao público presente no local e ao horário do evento, o que representa uma lacuna concreta que o uso de tecnologias da informação pode contribuir para suprir.

## 

## 2.2 Plataformas Digitais de Comercialização {#plataformas-digitais-de-comercialização}

As plataformas digitais de comercialização podem ser compreendidas como sistemas web que possibilitam a divulgação, organização e realização de processos comerciais por meio da internet, conectando ofertantes e consumidores em um mesmo ambiente virtual. Essas plataformas contribuem para ampliar o alcance dos produtos, facilitar o acesso às informações e otimizar etapas relacionadas à compra, venda e gestão de pedidos.

Entre os modelos de plataforma digital de comercialização, destaca-se o marketplace, caracterizado por reunir diferentes vendedores e compradores em um único ambiente online, permitindo a oferta de produtos ou serviços de múltiplos fornecedores. O que diferencia esse modelo de uma loja virtual comum é a presença de diversos vendedores, possibilitando que o consumidor consulte produtos, compare ofertas e realize pedidos de forma centralizada (SEBRAE RS, 2024).

No contexto da agricultura familiar, plataformas digitais e iniciativas de comercialização direta podem ampliar o alcance da produção local, conectando produtores rurais a consumidores além dos limites físicos e horários das feiras presenciais. O Agro Store adapta esse conceito à realidade dos produtores participantes da Feira do Produtor Rural Willi Dummer, em Camaquã/RS, permitindo a divulgação digital de produtos, a realização antecipada de pedidos e a organização da demanda pelos produtores, mantendo a retirada dos pedidos na feira física.

## 2.3 Modelo B2C {#modelo-b2c}

O modelo B2C, sigla para Business to Consumer, representa uma forma de transação comercial em que empresas vendem produtos ou serviços diretamente ao consumidor final. Esse modelo é comum em setores como varejo, comércio eletrônico e serviços, tendo como foco o atendimento das necessidades de consumidores individuais. Diferencia-se do modelo B2B, no qual as transações ocorrem entre empresas, e do modelo C2C, no qual a negociação ocorre entre consumidores (STRONG BUSINESS SCHOOL, 2026).

No contexto do Agro Store, o modelo B2C é utilizado como referência conceitual, uma vez que os produtores rurais participantes da plataforma precisam possuir CNPJ para atuar na feira física. Dessa forma, os produtores cadastrados são tratados no sistema como fornecedores formalizados, que disponibilizam seus produtos diretamente aos consumidores finais. Embora a entrega dos pedidos ocorra presencialmente na feira, o processo de divulgação, seleção de produtos e geração de pedidos é realizado por meio da plataforma digital, aproximando a solução do modelo de comercialização direta entre fornecedor e consumidor.

## 2.4 Ferramentas e Tecnologias Utilizadas {#ferramentas-e-tecnologias-utilizadas}

### 2.4.1 Aplicação Web {#aplicação-web}

Uma aplicação web é um programa armazenado em um servidor remoto e acessado pelo usuário por meio de um navegador, sem necessidade de instalação local no dispositivo. Diferentemente de aplicações desktop tradicionais, pode ser utilizada em qualquer dispositivo com acesso à internet, sejam computadores, tablets ou smartphones (YASAR, 2024).

### 2.4.2 API e REST {#api-e-rest}

API (Application Programming Interface) é um conjunto de definições e protocolos que viabiliza a comunicação entre sistemas distintos (ANTUNES, 2019). O estilo arquitetural REST (Representational State Transfer) estrutura a comunicação entre sistemas por meio de requisições HTTP, utilizando verbos como GET, POST, PUT, PATCH e DELETE para definir as operações realizadas sobre os recursos. As respostas são habitualmente retornadas no formato JSON, compatível com a grande maioria das linguagens de programação modernas. Esse modelo é amplamente adotado no desenvolvimento de APIs por favorecer a separação entre o backend e o frontend da aplicação, permitindo que diferentes clientes consumam os mesmos endpoints de forma padronizada (RAMOS, 2024).

### 2.4.3 Python {#python}

Criada em 1991 por Guido van Rossum, Python é uma linguagem de programação de alto nível, interpretada e de código aberto. Sua sintaxe clara e sua extensa biblioteca padrão contribuem para que seja adotada em áreas tão distintas quanto desenvolvimento web, ciência de dados e automação. O índice TIOBE a posiciona consistentemente entre as linguagens mais utilizadas no mundo (PYTHON SOFTWARE FOUNDATION, 2024).

### 2.4.4 Django e Django REST Framework {#django-e-django-rest-framework}

Django é um framework web desenvolvido em Python com foco em produtividade e segurança. Segue o padrão arquitetural MTV (Model-Template-View), variação do MVC, e oferece recursos prontos como autenticação de usuários, ORM para mapeamento objeto-relacional e painel administrativo gerado automaticamente, além de proteções nativas contra vulnerabilidades recorrentes em aplicações web (DJANGO SOFTWARE FOUNDATION, 2024).

O Django REST Framework (DRF) complementa o Django com ferramentas voltadas especificamente à construção de APIs REST, incluindo serialização de dados, controle de permissões e documentação automática de endpoints. É a biblioteca mais adotada para esse fim no ecossistema Python (CHRISTIE, 2024).

### 2.4.5 Vue.js {#vue.js}

Vue.js é um framework JavaScript de código aberto para construção de interfaces de usuário, criado por Evan You em 2014. Organiza a aplicação em componentes reutilizáveis e conta com um sistema de reatividade que reflete alterações de estado diretamente na interface, sem a necessidade de manipulação manual do DOM. Sua curva de aprendizado acessível e a facilidade de integração com projetos já existentes contribuem para sua ampla adoção (VUE.JS, 2024).

### 2.4.6 PostgreSQL {#postgresql}

PostgreSQL é um sistema gerenciador de banco de dados relacional de código aberto com desenvolvimento ativo desde 1994. Destaca-se pela conformidade com o padrão SQL, pelo suporte a tipos de dados avançados e pela robustez em ambientes com múltiplos acessos simultâneos, características que o tornam uma escolha consolidada em aplicações web de produção (THE POSTGRESQL GLOBAL DEVELOPMENT GROUP, 2024).

### 2.4.7 MVC e MTV {#mvc-e-mtv}

O padrão arquitetural MVC, formulado por Reenskaug em 1978, organiza uma aplicação em três camadas com responsabilidades distintas: o Model, responsável pelos dados e pela lógica de negócio da aplicação; a View, encarregada da apresentação das informações ao usuário; e o Controller, que define como a interface responde às interações recebidas. Essa separação de responsabilidades torna o sistema mais organizado e facilita a manutenção do projeto por diferentes desenvolvedores ao longo do tempo (GAMMA et al., 2000). O Django adota uma variação desse padrão denominada MTV, na qual o Template corresponde à View do MVC e a View do Django exerce o papel do Controller, preservando os mesmos princípios de separação de responsabilidades.

### 2.4.8 JSON {#json}

JSON (JavaScript Object Notation) é um formato textual de troca de dados baseado na sintaxe de objetos do JavaScript, criado por Douglas Crockford nos anos 1990. Por ser leve, legível e amplamente suportado, tornou-se o formato predominante na comunicação entre APIs REST e clientes web (SÁ, 2023).

### 2.4.9 JWT {#jwt}

JWT (JSON Web Token) é um padrão aberto definido pela RFC 7519 que representa de forma segura informações entre duas partes por meio de um objeto JSON, geralmente assinado digitalmente. Sua aplicação mais comum é a autenticação: após o login do usuário, um token é gerado e retornado ao cliente, que o envia nas requisições seguintes para acessar recursos protegidos. O token é composto por três partes, cabeçalho, carga útil e assinatura. Pode ser verificado diretamente pelo servidor sem necessidade de consultar o banco de dados a cada requisição (IBM, 2024).

# [3 METODOLOGIA]{.smallcaps} {#metodologia}

## 3.1 Requisitos {#requisitos}

Este capítulo descreve o conjunto de métodos e técnicas que foram adotados para o desenvolvimento do Agro Store. A pesquisa se classifica como aplicada, de natureza qualitativa, com abordagem de desenvolvimento de software. O trabalho foi conduzido em etapas sequenciais: levantamento de requisitos, modelagem do sistema e planejamento do desenvolvimento.

### 3.1.1 Requisitos Funcionais {#requisitos-funcionais}

- Permitir o cadastro de usuários consumidores e produtores rurais, utilizando o CPF como identificador único.

- Autenticar os usuários por meio de CPF e senha, retornando tokens de acesso e de renovação no padrão JWT (JSON Web Token), os quais serão utilizados nas requisições subsequentes para validação da identidade e das permissões do usuário.

- Permitir que usuários com perfil de produtor rural criem e gerenciem sua loja na plataforma, incluindo o cadastro de nome, descrição, CNPJ, imagem de perfil e cadastro de produtos sendo o vínculo entre o usuário e a loja estabelecido automaticamente pelo sistema.

- Disponibilizar um catálogo público de produtos, organizado por categorias, com informações de nome, descrição e preço, acessível a visitantes não autenticados.

- Registrar o histórico de preços de cada produto com controle de vigência, de forma que o sistema encerre automaticamente o preço anterior ao cadastrar um novo registro de preço, preservando o histórico de variações.

- Permitir que usuários autenticados adicionem, atualizem e removam produtos de seu carrinho de compras, com soma automática de quantidade para itens já presentes.

- Converter os itens selecionados do carrinho em pedidos, agrupando-os por loja e gerando, para cada pedido, um registro dos dados do cliente e dos produtos no momento da compra, removendo os itens processados do carrinho ao final da operação.

- Acompanhamento e a atualização do status dos pedidos, que percorrem os seguintes estados: Pendente, Em Preparo, Pronto para Entrega, Entregue e Cancelado, possibilitando que o produtor gerencie o andamento de cada pedido recebido.

- Usuários autenticados favoritam e desfavoritam produtos, garantindo a unicidade do vínculo entre usuário e produto para impedir registros duplicados.

- Usuários autenticados avaliem produtos pertencentes a pedidos com status Entregue, atribuindo uma nota de um a cinco e um comentário opcional, sendo permitida apenas uma avaliação por item de pedido.

- Produtor rural terá uma interface de gerenciamento de sua loja, permitindo a visualização dos pedidos recebidos e a atualização de seus respectivos status.

<!-- orientador: revisar -->
- Controlar a disponibilidade dos produtos a partir do estoque, retirando da listagem e da busca do catálogo os produtos com estoque zerado, sem inativá-los, e sinalizando ao produtor os produtos com estoque baixo, definido como até cinco unidades.

<!-- orientador: revisar -->
- Limitar a quantidade de cada item do carrinho ao estoque disponível do produto, ajustando automaticamente os carrinhos afetados quando o estoque diminuir e impedindo a finalização de itens sem estoque.

### 3.1.2 Requisitos não funcionais {#requisitos-não-funcionais}

- O sistema deve expor seus recursos por meio de uma API REST com retorno de dados no formato JSON, seguindo os princípios arquiteturais REST.

- A autenticação deve ser implementada por meio de tokens JWT, com token de acesso de validade de cento e vinte minutos e token de renovação de validade de um dia, protegendo os endpoints que exigem identificação do usuário.

- O *frontend* e o backend serão projetos independentes que se comunicam exclusivamente via HTTP, possibilitando suportar o uso de múltiplos usuários na mesma API sem alterações no servidor.

- A interface do usuário deve ser acessível por meio de navegador web, sem necessidade de instalação de software adicional, sendo responsivo.

- Os dados dos usuários devem ser armazenados de forma segura, com senhas protegidas pelo algoritmo de hash PBKDF2.

- O banco de dados deve garantir a integridade referencial dos dados por meio de restrições de unicidade e chaves estrangeiras, assegurando, entre outros, a unicidade de CPF, e-mail, CNPJ e SKU no sistema.

- A arquitetura modular do backend, organizada em aplicações de domínio independentes, deve possibilitar a adição de novos módulos e funcionalidades sem impacto sobre os módulos existentes, favorecendo a escalabilidade do sistema.

<!-- orientador: revisar -->
- O sistema deve impedir a venda de quantidade superior ao estoque disponível, inclusive quando houver pedidos simultâneos para o mesmo produto, por meio de controle de concorrência no banco de dados.

## 3.2 Modelagem {#modelagem}

### 3.2.1 Confecção de Diagramas {#confecção-de-diagramas}

A modelagem de um sistema de software envolve a construção de representações abstratas que permitem compreender, comunicar e validar suas estruturas e comportamentos antes mesmo de sua implementação.

Nesta seção, a organização dos dados do sistema é abordada por meio do Diagrama Entidade-Relacionamento (DER) e do Modelo Lógico do banco de dados, que descrevem as entidades, seus atributos e os vínculos estabelecidos entre elas. Complementarmente, são apresentados diagramas UML (Unified Modeling Language), que documentam o comportamento do sistema sob diferentes perspectivas: o diagrama de casos de uso mapeia as funcionalidades disponíveis e os atores que delas fazem uso; o diagrama de sequência ilustra a troca de mensagens entre os componentes ao longo do tempo; e o diagrama de atividades detalha os fluxos de decisão internos da aplicação.

### 3.2.2 Modelagem do Banco de Dados {#modelagem-do-banco-de-dados}

Nesta seção são apresentados o Diagrama Entidade-Relacionamento (DER) e o Modelo Lógico do banco de dados da aplicação desenvolvida. Tais diagramas buscam descrever, de maneira gráfica e estruturada, a organização dos dados do sistema, destacando as entidades do sistema, com seus atributos e relacionamentos.

## 

### 3.2.3 Diagrama Entidade-Relacionamento (DER) {#diagrama-entidade-relacionamento-der}

O diagrama confeccionado para este trabalho apresenta as seguintes entidades, com suas respectivas relações.

**Cliente**: representa os usuários cadastrados no sistema, armazenando os dados necessários para identificação, autenticação e controle de acesso, como nome, CPF, e-mail, data de nascimento, senha, último login, além de indicadores como e_produtor, esta_ativo e e_superusuario. Relaciona-se com a entidade Loja, permitindo que usuários com perfil de produtor estejam vinculados a uma loja cadastrada na plataforma. Também se relaciona com as entidades Favorito, Avaliação, Carrinho, Pedido e Pedido_Cliente, uma vez que um cliente pode favoritar produtos, avaliar produtos adquiridos, possuir carrinhos de compra, realizar pedidos e ter seus dados preservados no momento da compra.

**Loja**: representa as lojas cadastradas pelos produtores rurais na plataforma, armazenando informações como nome, descrição, CNPJ, imagem de perfil e situação de atividade. Relaciona-se com a entidade Cliente, pois uma loja pertence a um usuário produtor, e com a entidade Pedido, visto que uma loja pode receber diversos pedidos. Também se relaciona com a entidade Carrinho, permitindo que os itens adicionados pelos clientes sejam organizados conforme a loja responsável pelos produtos.

**Produto**: representa os produtos disponibilizados para comercialização na plataforma, armazenando informações como nome, descrição, código de barras, estoque, SKU, situação de atividade, data de criação e data de atualização. Relaciona-se com a entidade Preço, que armazena os valores associados ao produto; com a entidade Categoria, responsável pela classificação dos produtos; com a entidade Imagem, já que um produto pode possuir uma ou mais imagens; com a entidade Favorito, pois pode ser favoritado por diferentes clientes; com a entidade Avaliação, uma vez que pode receber avaliações; com a entidade Pedido_Produto, representando sua participação em pedidos; e com a entidade Carrinho_Produto, representando sua inclusão nos carrinhos de compra.

**Preço**: armazena os dados referentes à precificação dos produtos, incluindo valor de venda, valor de custo, valor de desconto, porcentagem de desconto, vigência inicial, vigência final, data de criação e data de atualização. Relaciona-se com a entidade Produto, permitindo que os valores praticados sejam associados aos produtos comercializados na plataforma.

**Categoria**: armazena os dados referentes às categorias dos produtos, como nome, status, data de criação e data de atualização. Relaciona-se com a entidade Produto na cardinalidade 1:N, pois uma categoria pode estar associada a diversos produtos, enquanto cada produto pertence a uma categoria.

**Imagem**: armazena os dados das imagens vinculadas aos produtos, como caminho da imagem, ordem de exibição, indicador de imagem principal, data de criação e data de atualização. Relaciona-se com a entidade Produto na cardinalidade N:1, pois um produto pode possuir diversas imagens cadastradas.

**Carrinho**: representa o agrupamento dos produtos selecionados por um cliente antes da geração do pedido, armazenando valores como valor líquido, valor bruto, valor de desconto, data de criação e data de atualização. Relaciona-se com a entidade Cliente, indicando o usuário proprietário do carrinho, e com a entidade Loja, permitindo que os carrinhos sejam organizados de acordo com a loja responsável pelos produtos. Os produtos inseridos no carrinho são representados pela entidade Carrinho_Produto.

**Carrinho_Produto**: entidade associativa que representa os itens adicionados ao carrinho de compras. Armazena dados como quantidade, data de criação e data de atualização, além de estabelecer o vínculo entre Carrinho e Produto. Essa entidade permite que um carrinho possua múltiplos produtos e que um mesmo produto possa aparecer em diferentes carrinhos de clientes distintos.

**Pedidos**: representa os pedidos gerados a partir dos itens selecionados no carrinho, armazenando informações financeiras como valor líquido, valor bruto e valor de desconto, além de data de criação e data de atualização. Relaciona-se com a entidade Loja, pois cada pedido está associado à loja responsável pelos produtos; com a entidade Status_Pedido, que indica a situação atual do pedido; com a entidade Pedido_Produto, que armazena os itens do pedido; e com a entidade Pedido_Cliente, que preserva os dados do cliente no momento da compra.

**Pedido_Produto**: entidade associativa que representa os produtos pertencentes a um pedido, armazenando informações como nome do produto, quantidade, valor unitário, valor de desconto, subtotal, data de criação e data de atualização. Relaciona-se com as entidades Pedido e Produto, refletindo a relação entre os pedidos realizados e os produtos adquiridos. Essa estrutura também permite preservar informações do produto no momento da compra, mesmo que seus dados sejam alterados posteriormente no cadastro original.

**Pedido_Cliente**: armazena os dados do cliente no momento da geração do pedido, como nome, CPF, e-mail, data de nascimento e gênero. Relaciona-se com as entidades Pedido e Cliente, permitindo manter um registro histórico das informações utilizadas no momento da compra. Essa entidade é importante para preservar os dados do pedido mesmo que o cliente altere posteriormente suas informações cadastrais.

**Status_Pedido**: armazena os possíveis status que um pedido pode assumir durante seu ciclo de vida, como Pendente, Em Preparo, Pronto para Entrega, Entregue e Cancelado. Relaciona-se com a entidade Pedido na cardinalidade 1:N, pois um mesmo status pode estar associado a diversos pedidos.

**Favorito**: entidade associativa que representa o vínculo entre clientes e produtos favoritados, armazenando data de criação e data de atualização. Relaciona-se com as entidades Cliente e Produto, refletindo uma relação N:N, na qual um cliente pode favoritar diversos produtos e um produto pode ser favoritado por diferentes clientes.

**Avaliação**: armazena os registros de avaliações realizadas pelos clientes sobre os produtos adquiridos, contendo dados como nota, comentário, data de criação e data de atualização. Relaciona-se com as entidades Cliente, Produto e Pedido, permitindo identificar qual cliente realizou a avaliação, qual produto foi avaliado e a qual pedido a avaliação está vinculada.

**Gênero**: armazena os dados referentes aos gêneros disponíveis para classificação dos clientes cadastrados no sistema, por meio do atributo gênero. Relaciona-se com a entidade Cliente, permitindo associar os usuários ao respectivo gênero informado no cadastro.

Abaixo, apresenta-se a Figura 1, referente ao Diagrama Entidade-Relacionamento, confeccionado na etapa de modelagem do sistema.

###### 

###### Figura 1 - Modelo Conceitual do Diagrama Entidade-Relacionamento

![](media/image1.png){width="8.810859580052494in" height="5.338041338582677in"}

**Fonte:** Confeccionado pelo autor (2026).

### 3.2.4 Modelo Lógico {#modelo-lógico}

A partir do modelo conceitual, foi elaborado o modelo lógico do banco de dados, apresentado na Figura 2. Nessa representação, as entidades são convertidas em tabelas, com a definição dos tipos de dados de cada coluna, das chaves primárias e das chaves estrangeiras responsáveis por materializar os relacionamentos entre os dados. Os relacionamentos N:N identificados no DER, como o vínculo entre pedidos e produtos, entre clientes e produtos favoritados e entre carrinhos e produtos, dão origem às tabelas associativas pedido_produto, favorito e carrinho_produto. Além disso, as restrições de unicidade, como as aplicadas a cpf, email, sku, codigo_barras e status, contribuem para assegurar a integridade dos dados prevista nos requisitos não funcionais do sistema.

###### Figura 2 - Modelo Lógico do Diagrama Entidade-Relacionamento

![](media/image2.png){width="5.94627624671916in" height="5.914646762904637in"}

**Fonte:** Confeccionado pelo autor (2026).

### 3.2.5 Diagramas UML {#diagramas-uml}

Nesta seção são apresentados os diagramas UML elaborados durante a modelagem do sistema proposto. Os diagramas têm como objetivo representar de forma visual e estruturada o funcionamento da aplicação e a interação entre seus componentes, contemplando diagramas de casos de uso, de sequência e de atividade, que auxiliam na compreensão de fluxos e comportamentos do sistema.

#### 3.2.5.1 Diagrama de Casos de Uso {#diagrama-de-casos-de-uso}

Conforme detalhado nos requisitos do sistema, a distinção entre os perfis de usuários exige a especificação das ações permitidas a cada um, caracterizando-os como atores do sistema. Dessa forma, a Figura 3 apresenta o Diagrama de Casos de Uso do Agro Store, que ilustra as interações entre esses atores e as funcionalidades disponíveis na plataforma.

- **Atores:**

<!-- -->

- **Cliente:** representa o usuário consumidor da plataforma, responsável por acessar o catálogo de produtos, adicionar itens ao carrinho, realizar pedidos, acompanhar o andamento das compras, favoritar produtos e avaliar produtos adquiridos. Esse ator utiliza o sistema com o objetivo de consultar os produtos disponibilizados pelos produtores rurais e realizar pedidos para posterior retirada na feira física.

- **Produtor Rural:** representa o usuário responsável pela comercialização dos produtos na plataforma. Além das funcionalidades básicas de cadastro e autenticação, o produtor pode solicitar a criação de sua loja, gerenciar os dados da loja, cadastrar e manter produtos, acompanhar os pedidos recebidos e atualizar o status dos pedidos conforme o andamento da preparação e entrega. Esse ator é fundamental para a manutenção do catálogo de produtos e para o atendimento das solicitações realizadas pelos clientes.

- **Administrador:** representa o usuário responsável pela gestão e validação de informações dentro da plataforma. Possui atribuições voltadas ao controle do sistema, como aprovar solicitações de criação de lojas e categorias, garantindo que os registros disponibilizados na aplicação estejam adequados às regras de funcionamento da plataforma.

<!-- -->

- **Casos de Uso:**

<!-- -->

- **Cadastrar-se:** caso de uso disponível para clientes e produtores rurais. Permite a criação de uma conta na plataforma por meio do preenchimento dos dados pessoais necessários para identificação e acesso ao sistema.

- **Efetuar login:** caso de uso base para todos os atores. Realiza a autenticação do usuário na plataforma, permitindo o acesso às funcionalidades de acordo com o perfil identificado.

- **Visualizar catálogo de produtos:** permite ao cliente consultar os produtos disponíveis na plataforma, visualizando informações como nome, descrição, preço, imagens, categoria e loja responsável pela oferta.

- **Gerenciar carrinho:** permite ao cliente adicionar produtos ao carrinho, alterar quantidades, remover itens e consultar os valores relacionados aos produtos selecionados antes da geração do pedido.

- **Realizar pedido:** possibilita ao cliente confirmar a compra dos itens selecionados no carrinho. A partir dessa ação, o sistema gera o pedido, registra os produtos adquiridos, calcula os valores correspondentes e preserva os dados do cliente no momento da compra.

- **Acompanhar pedido:** permite ao cliente consultar o andamento dos pedidos realizados, verificando o status atual de cada solicitação, como Pendente, Em Preparo, Pronto para Entrega, Entregue ou Cancelado.

- **Favoritar produto:** permite ao cliente marcar produtos de interesse para facilitar consultas futuras. Essa funcionalidade cria um vínculo entre o cliente e o produto favoritado.

- **Avaliar produto:** possibilita ao cliente registrar uma avaliação sobre produtos adquiridos, informando uma nota e, opcionalmente, um comentário. Essa ação está vinculada a pedidos concluídos, garantindo que apenas produtos comprados possam ser avaliados.

- **Solicitar criação de loja:** funcionalidade atribuída ao produtor rural. Permite que o usuário com perfil de produtor solicite a criação de uma loja na plataforma, informando dados como nome, descrição, CNPJ e imagem de perfil.

- **Gerenciar loja:** permite ao produtor rural consultar e atualizar as informações de sua loja, mantendo os dados de apresentação disponíveis aos clientes da plataforma.

- **Gerenciar produtos:** permite ao produtor rural cadastrar, consultar, atualizar e desativar produtos vinculados à sua loja, incluindo informações como nome, descrição, categoria, estoque, código de barras, SKU, imagens e preços.

- **Atualizar status do pedido:** funcionalidade atribuída ao produtor rural. Permite alterar o andamento dos pedidos recebidos, indicando as etapas de preparação e entrega dos produtos solicitados pelos clientes.

- **Solicitar criação de categoria:** permite ao produtor rural solicitar o cadastro de uma nova categoria de produtos quando as categorias existentes não forem suficientes para classificar adequadamente seus itens.

- **Aprovar criação de loja:** funcionalidade atribuída ao administrador. Permite validar as solicitações de criação de lojas realizadas pelos produtores rurais, garantindo maior controle sobre os fornecedores cadastrados na plataforma.

- **Aprovar criação de categoria:** funcionalidade atribuída ao administrador. Permite avaliar e aprovar novas categorias solicitadas pelos produtores, mantendo a organização e padronização do catálogo de produtos.

Na Figura 3, encontra-se o Diagrama de Casos de Uso, que apresenta graficamente a relação entre os atores do sistema e as funcionalidades disponíveis na plataforma.

###### Figura 3 - Diagrama de Casos de Uso

![](media/image7.png){width="6.449106517935258in" height="5.34049978127734in"}

#### 

#### 3.2.5.2 Diagramas de Sequência {#diagramas-de-sequência}

Os diagramas de sequência apresentados nesta seção representam os principais fluxos de interação entre os atores do sistema e os componentes da arquitetura da aplicação. Cada diagrama descreve a ordem das mensagens trocadas entre o usuário, a interface web, a API/Backend e o banco de dados, permitindo compreender o comportamento dinâmico do sistema em funcionalidades essenciais do Agro Store.

##### 3.2.5.2.1 Diagrama de Sequência I - Cadastro de Usuário {#diagrama-de-sequência-i---cadastro-de-usuário}

O Diagrama de Sequência I busca representar visualmente a lógica por trás do processo de cadastro de um novo usuário na plataforma. Possui a seguinte estrutura:

- **Atores:**

  - **Cliente:** usuário que deseja realizar seu cadastro na plataforma para acessar as funcionalidades do sistema.

  - **Frontend:** interface visual da aplicação, responsável por coletar os dados informados pelo usuário.

  - **API/Backend:** componente responsável por receber os dados, realizar validações, proteger a senha e solicitar a gravação das informações.

  - **Banco de dados:** componente responsável pela persistência dos dados do novo usuário.

<!-- -->

- **Fluxo de Eventos:**

  - **Preenche dados de cadastro:** o fluxo inicia-se quando o cliente informa seus dados pessoais na interface, como nome, CPF, e-mail, data de nascimento, gênero, tipo de usuário e senha.

  - **Envia dados de cadastro:** o *frontend* encaminha as informações preenchidas para a API/Backend.

  - **Valida os dados informados:** a API/Backend verifica se os campos obrigatórios foram preenchidos corretamente e se os dados informados já não estão cadastrados.

  - **Protege a senha do usuário:** caso os dados sejam válidos, a senha é protegida por meio de algoritmo de hash antes de ser armazenada.

  - **Salva novo usuário:** a API/Backend solicita ao banco de dados a criação do registro do usuário.

  - **Confirma cadastro:** o banco de dados confirma a persistência das informações.

  - **Retorna usuário cadastrado:** a API/Backend retorna ao *frontend* a confirmação do cadastro.

  - **Exibe confirmação de cadastro:** o *frontend* apresenta ao cliente a mensagem de sucesso. Caso os dados sejam inválidos ou já existentes, a API/Backend retorna uma mensagem de erro e o *frontend* solicita a correção das informações.

Abaixo, a Figura 4 apresenta o Diagrama de Sequência I, que detalha o processo de cadastro de usuário.

###### Figura 4 - Diagrama de Sequência I - Cadastro de Usuário

![](media/image3.png){width="6.299212598425197in" height="3.9305555555555554in"}

**Fonte:** Confeccionado pelo autor (2026).

##### 3.2.5.2.2 Diagrama de Sequência II - Acesso ao Sistema {#diagrama-de-sequência-ii---acesso-ao-sistema}

O Diagrama de Sequência II busca representar visualmente o fluxo de autenticação do usuário na plataforma. Possui a seguinte estrutura:

- **Atores:**

  - **Usuário:** representa o cliente, produtor rural ou administrador que deseja acessar a área autenticada do sistema.

  - **Frontend:** interface visual responsável por receber CPF e senha.

  - **API/Backend:** componente responsável por validar as credenciais e gerar as credenciais de acesso.

  - **Banco de dados:** componente onde são consultadas as informações do usuário cadastrado.

<!-- -->

- **Fluxo de Eventos:**

  - **Informa CPF e senha:** o fluxo inicia-se quando o usuário informa suas credenciais de acesso na tela de login.

  - **Envia credenciais:** o *frontend* encaminha CPF e senha para a API/Backend.

  - **Procura usuário pelo CPF:** a API/Backend consulta o banco de dados para localizar o usuário correspondente ao CPF informado.

  - **Retorna dados do usuário:** o banco de dados retorna as informações encontradas.

  - **Confere a senha:** a API/Backend compara a senha informada com a senha protegida armazenada.

  - **Gera credenciais de acesso:** caso as credenciais estejam corretas, a API/Backend gera as credenciais necessárias para autenticação do usuário.

  - **Retorna acesso autorizado:** a API/Backend envia ao *frontend* a confirmação de autenticação.

  - **Libera área autenticada:** o *frontend* permite que o usuário acesse as funcionalidades disponíveis ao seu perfil. Caso as credenciais estejam incorretas, é retornado um erro de autenticação e o usuário é informado de que o CPF ou a senha são inválidos.

Abaixo, a Figura 5 apresenta o Diagrama de Sequência II, que detalha o processo de acesso ao sistema.

###### Figura 5 - Diagrama de Sequência II - Acesso ao Sistema

![](media/image8.png){width="6.299212598425197in" height="4.777777777777778in"}

**Fonte:** Confeccionado pelo autor (2026).

##### 3.2.5.2.3 Diagrama de Sequência III - Cadastro de Loja pelo Produtor {#diagrama-de-sequência-iii---cadastro-de-loja-pelo-produtor}

O Diagrama de Sequência III busca representar visualmente o processo de cadastro de uma loja por um usuário com perfil de produtor rural. Possui a seguinte estrutura:

- **Atores:**

  - **Produtor:** usuário responsável por cadastrar e gerenciar uma loja na plataforma.

  - **Frontend:** interface visual utilizada pelo produtor para informar os dados da loja.

  - **API/Backend:** componente responsável por verificar a autenticação, validar o perfil do usuário e solicitar a criação da loja.

  - **Banco de dados:** componente responsável por armazenar os dados da loja cadastrada.

<!-- -->

- **Fluxo de Eventos:**

  - **Informa dados da loja:** o fluxo inicia-se quando o produtor preenche os dados necessários para criação da loja, como nome, descrição, CNPJ e imagem.

  - **Envia dados da loja:** o *frontend* encaminha as informações para a API/Backend.

  - **Verifica autenticação:** a API/Backend valida se o usuário está autenticado no sistema.

  - **Confirma se o usuário é produtor:** a API/Backend verifica se o usuário possui permissão para cadastrar uma loja.

  - **Salva loja vinculada ao produtor:** caso o usuário seja produtor, a API/Backend solicita ao banco de dados a criação da loja, vinculando-a ao usuário responsável.

  - **Confirma criação da loja:** o banco de dados confirma o armazenamento das informações.

  - **Retorna dados da loja:** a API/Backend devolve ao *frontend* os dados cadastrados.

  - **Exibe loja cadastrada:** o *frontend* apresenta ao produtor a confirmação do cadastro. Caso o usuário não possua perfil de produtor, a API/Backend retorna erro de permissão e o processo é interrompido.

Abaixo, a Figura 6 apresenta o Diagrama de Sequência III, que detalha o processo de cadastro de loja pelo produtor.

###### Figura 6 - Diagrama de Sequência III - Cadastro de Loja pelo Produtor

![](media/image4.png){width="6.299212598425197in" height="3.8472222222222223in"}

**Fonte:** Confeccionado pelo autor (2026).

##### 3.2.5.2.4 Diagrama de Sequência IV - Cadastro de Produto e Definição de Preço {#diagrama-de-sequência-iv---cadastro-de-produto-e-definição-de-preço}

O Diagrama de Sequência IV busca representar visualmente o processo de cadastro de produtos e definição de seus respectivos preços. Possui a seguinte estrutura:

- **Atores:**

  - **Produtor:** usuário responsável por cadastrar produtos vinculados à sua loja.

  - **Frontend:** interface visual utilizada para informar os dados do produto e seu preço.

  - **API/Backend:** componente responsável por validar a autenticação, registrar o produto e associar as informações de preço.

  - **Banco de dados:** componente responsável pela persistência dos dados de produto e preço.

<!-- -->

- **Fluxo de Eventos:**

  - **Preenche dados do produto:** o fluxo inicia-se quando o produtor informa os dados do produto, como nome, descrição, loja, categoria, estoque e identificadores.

  - **Envia produto:** o *frontend* encaminha os dados do produto para a API/Backend.

  - **Verifica autenticação:** a API/Backend confirma se o produtor está autenticado e autorizado.

  - **Salva produto:** a API/Backend solicita ao banco de dados a gravação do novo produto.

  - **Confirma produto cadastrado:** o banco de dados confirma a criação do registro.

  - **Retorna produto criado:** a API/Backend devolve ao *frontend* as informações do produto cadastrado.

  - **Define preço de venda e desconto:** em seguida, o produtor informa os dados de preço do produto, como valor de venda, valor de custo e desconto.

  - **Envia preço do produto:** o *frontend* encaminha as informações de preço para a API/Backend.

  - **Calcula desconto quando informado:** a API/Backend realiza os cálculos necessários quando houver desconto aplicado.

  - **Salva preço vigente:** a API/Backend solicita ao banco de dados o armazenamento do preço associado ao produto.

  - **Confirma preço cadastrado:** o banco de dados confirma a gravação das informações.

  - **Exibe produto com preço atual:** o *frontend* apresenta ao produtor o produto cadastrado com seu respectivo preço.

Abaixo, a Figura 7 apresenta o Diagrama de Sequência IV, que detalha o processo de cadastro de produto e definição de preço.

###### Figura 7 - Diagrama de Sequência IV - Cadastro de Produto e Definição de Preço

![](media/image6.png){width="6.299212598425197in" height="4.430555555555555in"}

**Fonte:** Confeccionado pelo autor (2026).

##### 3.2.5.2.5 Diagrama de Sequência V - Consulta de Catálogo de Produtos {#diagrama-de-sequência-v---consulta-de-catálogo-de-produtos}

O Diagrama de Sequência V busca representar visualmente o processo de consulta pública dos produtos disponíveis na plataforma. Possui a seguinte estrutura:

- **Atores:**

  - **Cliente:** usuário que acessa a plataforma para consultar os produtos disponíveis.

  - **Frontend:** interface visual responsável por apresentar o catálogo ao usuário.

  - **API/Backend:** componente responsável por buscar e organizar os dados dos produtos.

  - **Banco de dados:** componente onde são consultadas as informações de produtos, lojas, categorias e preços.

<!-- -->

- **Fluxo de Eventos:**

  - **Abre o catálogo de produtos:** o fluxo inicia-se quando o cliente acessa a área de catálogo da plataforma.

  - **Solicita lista de produtos:** o *frontend* envia à API/Backend uma solicitação para recuperar os produtos disponíveis.

  - **Busca produtos, lojas, categorias e preços vigentes:** a API/Backend consulta o banco de dados para obter as informações necessárias.

  - **Retorna produtos encontrados:** o banco de dados devolve os registros localizados.

  - **Monta catálogo formatado:** a API/Backend organiza as informações, incluindo preço atual, preço original e desconto, quando houver.

  - **Envia catálogo formatado:** a API/Backend retorna ao *frontend* a lista de produtos preparada para exibição.

    <!-- orientador: revisar -->

  - **Exibe produtos disponíveis:** o *frontend* apresenta ao cliente os produtos disponíveis na plataforma, isto é, os produtos ativos, pertencentes a lojas ativas e com estoque maior que zero. Por se tratar de um recurso público, esse fluxo não exige autenticação.

Abaixo, a Figura 8 apresenta o Diagrama de Sequência V, que detalha o processo de consulta do catálogo de produtos.

<!-- autor: atualizar figura conforme texto (RN-017) -->

###### Figura 8 - Diagrama de Sequência V - Consulta de Catálogo de Produtos

![](media/image5.png){width="6.299212598425197in" height="2.8333333333333335in"}

**Fonte:** Confeccionado pelo autor (2026).

#### 3.2.5.3 Diagrama de Atividades {#diagrama-de-atividades}

Finalizando a apresentação dos diagramas de modelagem UML, encontram-se os diagramas de atividades, responsáveis por representar o fluxo de execução das ações realizadas dentro de processos específicos do sistema. Esses diagramas permitem visualizar a sequência das atividades, os pontos de decisão e os possíveis caminhos alternativos existentes durante a utilização da plataforma.

##### 3.2.5.3.1 Diagrama de Atividades I - Geração de Pedido pelo Cliente {#diagrama-de-atividades-i---geração-de-pedido-pelo-cliente}

O Diagrama de Atividades I busca modelar o fluxo realizado pelo cliente desde o acesso ao catálogo de produtos até a geração do pedido. Esse processo representa uma das principais funcionalidades do Agro Store, pois descreve o caminho percorrido pelo consumidor para selecionar produtos disponíveis na plataforma, adicioná-los ao carrinho e confirmar a compra. O fluxo possui a seguinte estrutura:

  <!-- orientador: revisar -->

- **Acessar catálogo de produtos:** descreve a ação inicial do cliente ao acessar a listagem de produtos disponíveis na plataforma. A partir dessa ação, o sistema busca os produtos disponíveis, isto é, os produtos ativos, pertencentes a lojas ativas e com estoque maior que zero, com suas respectivas lojas, categorias e preços vigentes, retornando o catálogo formatado para exibição ao usuário.

- **Selecionar produto:** representa a escolha de um item pelo cliente dentro do catálogo. Após a seleção, o sistema busca as informações detalhadas do produto, incluindo dados da loja, descrição, preço vigente e demais informações necessárias para que o cliente decida pela inclusão no carrinho.

- **Adicionar produto ao carrinho:** ocorre quando o cliente informa a quantidade desejada e solicita a inclusão do produto no carrinho. Essa ação gera um nó de decisão responsável por verificar se o cliente está autenticado. Caso não esteja autenticado \[Não\], o sistema informa a necessidade de realizar login e encerra o fluxo. Caso esteja autenticado \[Sim\], o processo continua.

  <!-- orientador: revisar -->

- **Verificar existência do produto no carrinho:** após a autenticação, o sistema verifica se o produto selecionado já está presente no carrinho do cliente. Caso o produto já exista \[Sim\], a quantidade informada é somada à quantidade já registrada. Caso o produto ainda não esteja no carrinho \[Não\], um novo item é criado. Em ambos os casos, a quantidade resultante fica limitada ao estoque disponível do produto: se a ultrapassar, a inclusão é recusada e o cliente é informado de que não há estoque suficiente. Quando a inclusão é aceita, o sistema consulta o preço vigente do produto e atualiza os valores do carrinho.

- **Exibir produto no carrinho:** representa o retorno visual ao cliente após a inclusão ou atualização do item. O sistema apresenta o carrinho atualizado, contendo os produtos selecionados, suas quantidades e os subtotais calculados.

- **Abrir carrinho:** descreve a ação do cliente ao acessar o resumo da compra. Nesse momento, o sistema busca os itens vinculados ao carrinho do usuário autenticado, retornando os produtos, lojas, quantidades e preços para exibição.

- **Alterar carrinho:** representa uma ação opcional do cliente antes da confirmação da compra. Caso deseje alterar o carrinho \[Sim\], o cliente pode modificar a quantidade de um item ou removê-lo. O sistema atualiza os dados e exibe novamente o resumo da compra. Caso não deseje realizar alterações \[Não\], o fluxo segue para a confirmação da compra.

- **Confirmar compra:** ocorre quando o cliente decide gerar o pedido a partir dos itens selecionados no carrinho. O sistema recebe a lista de itens e verifica novamente a credencial de acesso do cliente antes de buscar os itens pertencentes ao seu carrinho.

  <!-- orientador: revisar -->

- **Verificar itens válidos:** esse nó de decisão valida se todos os itens enviados estão aptos para a geração do pedido. Um item é considerado inválido quando não pertence ao carrinho do cliente, quando o produto ou a loja estão inativos, quando sua quantidade é zero (item "Sem estoque"), quando o estoque é insuficiente para a quantidade solicitada ou quando o produto não possui preço vigente. Caso algum item seja inválido \[Não\], a finalização é recusada por inteiro: nenhum pedido é gerado e o cliente é informado do motivo, com a indicação do produto envolvido. Caso todos os itens sejam válidos \[Sim\], o sistema segue para o processamento da compra.

- **Agrupar itens por loja:** os itens selecionados são organizados de acordo com a loja responsável por cada produto. Essa etapa é necessária porque um mesmo carrinho pode conter produtos de diferentes produtores, exigindo a geração de pedidos separados para cada loja envolvida.

- **Calcular valores do pedido:** para cada loja envolvida, o sistema consulta os preços vigentes dos produtos, calcula o valor bruto, os descontos aplicáveis e o valor líquido do pedido.

- **Criar pedido:** após o cálculo dos valores, o sistema cria o pedido com status inicial Pendente, registra os produtos vinculados ao pedido e copia os dados do cliente para preservar as informações existentes no momento da compra.

- **Remover itens comprados do carrinho:** depois que os pedidos são criados, os itens processados são removidos do carrinho, evitando que permaneçam disponíveis para nova compra duplicada.

  <!-- orientador: revisar -->

- **Baixar o estoque e ajustar os carrinhos afetados:** na criação dos pedidos, o sistema subtrai do estoque de cada produto a quantidade vendida. Em seguida, nos carrinhos de outros clientes que contêm esses produtos, as quantidades que ultrapassam o novo estoque são reduzidas a esse valor, podendo chegar a zero, caso em que o item permanece no carrinho com a indicação "Sem estoque". Essas operações ocorrem na mesma transação da geração do pedido, conforme descrito na seção 3.3.

- **Exibir confirmação da compra:** ao final do processo, o sistema apresenta ao cliente a confirmação da compra realizada e informa que o pedido foi criado com status Pendente, encerrando o fluxo no nó final.

A seguir, apresenta-se a Figura 9, referente ao Diagrama de Atividades I, que descreve o processo de seleção de produto, inclusão no carrinho e geração de pedido pelo cliente.

<!-- autor: atualizar figura conforme texto (RN-017) -->

###### Figura 9 - Diagrama de Atividades I - Geração de Pedido pelo Cliente

![](media/image9.png){width="9.724409448818898in" height="3.4305555555555554in"}

> **Fonte:** Confeccionado pelo autor (2026).

<!-- orientador: revisar -->
## 3.3 Regras de Negócio de Estoque {#regras-de-negócio-de-estoque}

Durante o desenvolvimento, identificou-se a necessidade de regras específicas para o tratamento do estoque dos produtos, aspecto que não havia sido detalhado na versão inicial dos requisitos. Esta seção descreve as regras implementadas, as decisões técnicas adotadas para garantir sua consistência, a forma como foram validadas e as limitações que permanecem como trabalhos futuros.

<!-- orientador: revisar -->
### 3.3.1 Disponibilidade dos Produtos por Estoque {#disponibilidade-dos-produtos-por-estoque}

Na versão inicial do sistema, não havia tratamento específico para produtos com estoque zerado ou reduzido, de modo que itens esgotados permaneciam listados no catálogo e podiam induzir o cliente a tentar uma compra impossível de ser atendida. Para corrigir essa situação, foi definida e implementada uma regra de disponibilidade baseada na quantidade em estoque. O produto cujo estoque atinge zero deixa de ser exibido na listagem pública do catálogo, sem que seu cadastro seja inativado. Como a busca do catálogo é realizada no *frontend* sobre o resultado dessa listagem fornecida pela API, o produto também deixa de ser encontrado pela busca. A página de detalhe permanece acessível por meio do endereço direto e informa a condição "Sem estoque", com a compra bloqueada. Quando o produtor repõe o estoque, o produto volta a ser exibido no catálogo automaticamente, sem nenhuma ação adicional. Essa decisão separa dois conceitos distintos: a inativação, que representa a decisão do produtor de retirar o produto de venda, e a indisponibilidade temporária, que decorre apenas da falta de unidades.

Para apoiar o produtor no acompanhamento do estoque, o sistema adota um limite único e global de cinco unidades para caracterizar o estoque baixo. Na área do produtor, os produtos com estoque entre uma e cinco unidades recebem o indicador "Estoque baixo", e os produtos com estoque zerado recebem o indicador "Sem estoque — fora do catálogo". Um aviso resumido informa a quantidade de produtos ativos em cada situação. Trata-se de uma sinalização apenas visual, exibida quando o produtor acessa a plataforma. Além disso, a API recusa, com mensagem explicativa, qualquer tentativa de registrar estoque negativo.

<!-- orientador: revisar -->
### 3.3.2 Coerência entre Carrinho e Estoque {#coerência-entre-carrinho-e-estoque}

Como o carrinho é persistido no servidor, a quantidade escolhida pelo cliente pode deixar de corresponder ao estoque real entre o momento da inclusão e o da finalização. Para manter a coerência, o sistema limita a quantidade de cada item ao estoque disponível do produto. Sempre que o estoque diminui, seja pela venda a outro cliente, seja por ajuste feito pelo produtor, as quantidades de todos os carrinhos que ultrapassam o novo estoque são reduzidas a esse valor e gravadas no banco de dados. Essa redução pode chegar a zero. Nesse caso, o item permanece no carrinho com a indicação "Sem estoque" e não pode ser finalizado. Se o cliente tentar finalizar um conjunto de itens que inclua um item nessa condição, a finalização é recusada por inteiro e nenhum pedido é gerado, seguindo o mesmo critério adotado para estoque insuficiente ou produto inativo. Por decisão de projeto, a reposição posterior do estoque não restaura a quantidade que o cliente havia escolhido, pois essa informação não é mantida após o ajuste.

Essas regras complementam o fluxo apresentado no Diagrama de Atividades I (Figura 9): a inclusão e a alteração de itens no carrinho passam a respeitar o estoque disponível, e a geração do pedido, ao baixar o estoque dos produtos vendidos, ajusta também os carrinhos de outros clientes que contenham esses produtos.

<!-- orientador: revisar -->
### 3.3.3 Tratamento de Concorrência na Baixa de Estoque {#tratamento-de-concorrência-na-baixa-de-estoque}

Em um sistema com vários usuários simultâneos, duas compras do mesmo produto podem ser processadas ao mesmo tempo. Cada uma pode ler o mesmo estoque antes que a outra o atualize e, assim, vender mais unidades do que as disponíveis. Esse fenômeno é conhecido como condição de corrida (*race condition*) [CITAÇÃO NECESSÁRIA]. Para evitá-lo, a finalização do pedido e a edição do estoque pelo produtor são executadas dentro de uma transação, isto é, um conjunto de operações tratado pelo banco de dados como uma unidade indivisível. Nessa transação, as linhas dos produtos envolvidos recebem um bloqueio pessimista, obtido pela instrução SQL `SELECT ... FOR UPDATE` [CITAÇÃO NECESSÁRIA]. Enquanto uma operação mantém o bloqueio, as demais que precisam do mesmo produto aguardam sua conclusão e então leem o estoque já atualizado, o que impede a venda acima do disponível. Na finalização, os produtos são bloqueados sempre na mesma ordem, o que reduz o risco de impasse (*deadlock*) entre transações concorrentes.

Esse bloqueio por linha é efetivo no PostgreSQL, banco de dados adotado para a versão final do sistema. Durante o desenvolvimento, utiliza-se o SQLite, sistema gerenciador de banco de dados que armazena todos os dados em um único arquivo e dispensa a instalação de um servidor. O SQLite não oferece bloqueio por linha. Nesse ambiente, a proteção decorre do próprio SQLite, que serializa as operações de escrita no banco de dados [CITAÇÃO NECESSÁRIA]. Por essa razão, o comportamento de referência para o controle de concorrência é o do PostgreSQL.

<!-- orientador: revisar -->
### 3.3.4 Validação das Regras de Estoque {#validação-das-regras-de-estoque}

As regras descritas nesta seção foram verificadas por meio de testes automatizados do backend, que simulam as requisições à API e conferem as respostas e os dados gravados. Na data de redação desta seção, a suíte de testes do backend reunia 111 testes automatizados, todos executados com sucesso, entre eles os que verificam a retirada do produto sem estoque do catálogo, os limites do indicador de estoque baixo, a recusa de estoque negativo e o ajuste dos carrinhos. Complementarmente, as telas afetadas foram inspecionadas visualmente nas larguras de 375 e 1280 pixels, representativas de *smartphones* e de computadores de mesa, respectivamente, em atenção ao requisito não funcional de responsividade da interface.

<!-- orientador: revisar -->
### 3.3.5 Limitações e Trabalhos Futuros do Controle de Estoque {#limitações-e-trabalhos-futuros-do-controle-de-estoque}

O controle de estoque implementado atende às necessidades do MVP (Produto Mínimo Viável, do inglês *Minimum Viable Product*), mas apresenta limitações que podem orientar trabalhos futuros, no âmbito de um controle de estoque mais avançado. A sinalização de estoque baixo é apenas visual e depende do acesso do produtor à plataforma. Uma evolução possível é a notificação ativa, por e-mail ou por notificação *push*. O limite de cinco unidades é único para todos os produtos e poderia passar a ser configurável por produto, considerando as diferentes unidades de venda e o giro de cada item. Quando a quantidade de um item do carrinho é reduzida sem chegar a zero, o cliente não recebe um aviso específico. Esse aviso exigiria armazenar a quantidade escolhida originalmente. Por fim, a proibição de estoque negativo é hoje garantida apenas pela validação da API. A restrição equivalente no banco de dados, que reforçaria a integridade independentemente da aplicação, está planejada e ainda não foi implementada.

# [4 CRONOGRAMA]{.smallcaps} {#cronograma}

Abaixo segue o cronograma de atividades:

1.  Construção da Proposta de TCC;

2.  Pesquisa Bibliográfica para levantamento de sistemas semelhantes, bem como construção do referencial teórico;

3.  Levantamento dos requisitos funcionais e não-funcionais;

4.  Construção dos diagramas;

5.  Modelagem do banco de dados;

6.  Seminário de andamento;

7.  Desenvolvimento dos códigos;

8.  Análise dos Resultados e Conclusão;

9.  Entrega e Defesa do TCC

###### Quadro 1 - Cronograma de atividades

<table style="width:95%;">
<colgroup>
<col style="width: 8%" />
<col style="width: 6%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
</colgroup>
<tbody>
<tr>
<td>Atividades</td>
<td colspan="11" style="text-align: center;">Mês / 2026</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">FEV</td>
<td style="text-align: center;">MAR</td>
<td style="text-align: center;">ABR</td>
<td style="text-align: center;">MAI</td>
<td style="text-align: center;">JUN</td>
<td style="text-align: center;">JUL</td>
<td style="text-align: center;">AGO</td>
<td style="text-align: center;">SET</td>
<td style="text-align: center;">OUT</td>
<td style="text-align: center;">NOV</td>
<td style="text-align: center;">DEZ</td>
</tr>
<tr>
<td style="text-align: center;">1</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;">2</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;">3</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;">4</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;">5</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;">6</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">X</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;">7</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;">8</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;">9</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">X</td>
<td style="text-align: center;">X</td>
</tr>
</tbody>
</table>

**Fonte:** Confeccionado pelo autor (2026)

**REFERÊNCIAS**

ABRAMOVAY, Ricardo. Muito além da economia verde. São Paulo: Editora Abril, 2012.

ANTUNES, M. API RESTful: conceito, princípios e como criar. 2019. Disponível em: https://www.hostgator.com.br/blog/api-restful. Acesso em: 11 abr. 2026.

BRASIL. Lei nº 11.326, de 24 de julho de 2006. Estabelece as diretrizes para a formulação da Política Nacional da Agricultura Familiar e Empreendimentos Familiares Rurais. Diário Oficial da União, Brasília, DF, 25 jul. 2006. Disponível em: https://www.planalto.gov.br/ccivil_03/\_ato2004-2006/2006/lei/l11326.htm. Acesso em: 06 abr. 2026.

CHRISTIE, T. Django REST Framework documentation. 2024. Disponível em: https://www.django-rest-framework.org/. Acesso em: 11 abr. 2026.

DJANGO SOFTWARE FOUNDATION. Django documentation. 2024. Disponível em: https://docs.djangoproject.com/. Acesso em: 11 abr. 2026.

GAMMA, E. et al. Padrões de projeto: soluções reutilizáveis de software orientado a objetos. Porto Alegre: Bookman, 2000.

IBM. JSON Web Token (JWT). IBM Documentation, 2024. Disponível em: https://www.ibm.com/docs/pt-br/cics-ts/6.x?topic=cics-json-web-token-jwt. Acesso em: 12 abr. 2026.

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). Censo Agropecuário 2017: resultados definitivos. Rio de Janeiro: IBGE, 2019. Disponível em: https://www.ibge.gov.br/estatisticas/economicas/agricultura-e-pecuaria/21814-2017-censo-agropecuario.html. Acesso em: 06 abr. 2026.

PYTHON SOFTWARE FOUNDATION. Python documentation. 2024. Disponível em: https://docs.python.org/. Acesso em: 11 abr. 2026.

RAMOS, Vinícius. O que é o Django REST Framework (DRF)? Python Academy, 27 ago. 2024. Disponível em: https://pythonacademy.com.br/blog/o-que-e-o-django-rest-framework. Acesso em: 11 abr. 2026.

SÁ, L. JSON: guia completo. 2023. Disponível em: https://www.hostgator.com.br/blog/json-guia-completo. Acesso em: 12 abr. 2026.

SEBRAE RS. Marketplace: o que é e como funciona. Porto Alegre, 27 ago. 2024. Disponível em: https://digital.sebraers.com.br/blog/marketing-e-vendas/marketplace-o-que-e-e-como-funciona/. Acesso em: 06 abr. 2026.

SILVA, Kathrein. Feira do Produtor Rural Willi Dummer acontece neste sábado (20). Clic Camaquã, Camaquã, 17 set. 2025. Disponível em: https://www.cliccamaqua.com.br/noticias/feira-do-produtor-rural-willi-dummer-acontece-neste-sabado-20/. Acesso em: 06 abr. 2026.

STRONG BUSINESS SCHOOL. O que é B2C (Business to Consumer)? Disponível em: https://strong.com.br/glossario/o-que-e-b2c-business-to-consumer/. Acesso em: 13 jun. 2026.

THE POSTGRESQL GLOBAL DEVELOPMENT GROUP. PostgreSQL documentation. 2024. Disponível em: https://www.postgresql.org/docs/. Acesso em: 11 abr. 2026.

VUE.JS. Vue.js documentation. 2024. Disponível em: https://vuejs.org/. Acesso em: 11 abr. 2026.

YASAR, Kinza. What is web application (web apps) and its benefits? TechTarget, 25 nov. 2024. Disponível em: https://www.techtarget.com/searchsoftwarequality/definition/Web-application-Web-app. Acesso em: 11 abr. 2026.

> 
