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

[Figura 5 - Diagrama de Sequência II - Acesso ao Sistema 34](#figura-5---diagrama-de-sequência-ii---acesso-ao-sistema)

[Figura 6 - Diagrama de Sequência III - Cadastro de Loja pelo Produtor 36](#figura-6---diagrama-de-sequência-iii---cadastro-de-loja-pelo-produtor)

[Figura 7 - Diagrama de Sequência IV - Cadastro de Produto e Definição de Preço 38](#figura-7---diagrama-de-sequência-iv---cadastro-de-produto-e-definição-de-preço)

[Figura 8 - Diagrama de Sequência V - Consulta de Catálogo de Produtos 39](#figura-8---diagrama-de-sequência-v---consulta-de-catálogo-de-produtos)

[Figura 9 - Diagrama de Atividades I - Geração de Pedido pelo Cliente 42](#figura-9---diagrama-de-atividades-i---geração-de-pedido-pelo-cliente)

<!-- autor: atualizar a numeração de páginas das listas e do sumário após a exportação -->

[Figura 10 - Diagrama de Estados do Pedido](#figura-10---diagrama-de-estados-do-pedido)

[Figura 11 - Diagrama de Sequência VI - Imagens do Produto](#figura-11---diagrama-de-sequência-vi---imagens-do-produto)

[Figura 12 - Diagrama de Sequência VII - Avaliação de Item Entregue](#figura-12---diagrama-de-sequência-vii---avaliação-de-item-entregue)

<!-- orientador: revisar -->
[Figura 13 - Diagrama de Sequência VIII - Redefinição de Senha](#figura-13---diagrama-de-sequência-viii---redefinição-de-senha)

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

<!-- orientador: revisar -->
IP Internet Protocol

JSON JavaScript Object Notation

JWT JSON Web Token

LGPD Lei Geral de Proteção de Dados Pessoais

MTV Model-Template-View

MVC Model-View-Controller

MVP Minimum Viable Product (Produto Mínimo Viável)

ORM Object-Relational Mapping

REST Representational State Transfer

SKU Stock Keeping Unit

<!-- orientador: revisar -->
SMTP Simple Mail Transfer Protocol

SQL Structured Query Language

<!-- orientador: revisar -->
TLS Transport Layer Security

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

[**4 DESENVOLVIMENTO E RESULTADOS**](#desenvolvimento-e-resultados)

> [**4.1 Regras de Negócio de Estoque**](#regras-de-negócio-de-estoque)
>
> [4.1.1 Disponibilidade dos Produtos por Estoque](#disponibilidade-dos-produtos-por-estoque)
>
> [4.1.2 Coerência entre Carrinho e Estoque](#coerência-entre-carrinho-e-estoque)
>
> [4.1.3 Tratamento de Concorrência na Baixa de Estoque](#tratamento-de-concorrência-na-baixa-de-estoque)
>
> [**4.2 Pedidos e Ciclo de Status**](#pedidos-e-ciclo-de-status)
>
> [**4.3 Imagens dos Produtos**](#imagens-dos-produtos)
>
> [**4.4 Área do Produtor e Perfil do Usuário**](#área-do-produtor-e-perfil-do-usuário)
>
> [**4.5 Favoritos**](#favoritos)
>
> [**4.6 Avaliações de Produtos**](#avaliações-de-produtos)
>
> [**4.7 Preservação do Histórico de Pedidos**](#preservação-do-histórico-de-pedidos)
>
> <!-- orientador: revisar -->
> [**4.8 Redefinição de Senha**](#redefinição-de-senha)
>
> [**4.9 Verificação das Funcionalidades**](#verificação-das-funcionalidades)

[**5 LIMITAÇÕES E TRABALHOS FUTUROS**](#limitações-e-trabalhos-futuros)

> <!-- orientador: revisar -->
> [**5.1 Limitações das Funcionalidades Implementadas**](#limitações-das-funcionalidades-implementadas)
>
> [**5.2 Trabalhos Futuros**](#trabalhos-futuros)

[**6 CRONOGRAMA 43**](#cronograma)

# [1 INTRODUÇÃO]{.smallcaps} {#introdução}

O presente trabalho propõe o desenvolvimento do Agro Store, uma plataforma digital voltada à intermediação de pedidos entre consumidores e produtores rurais participantes da Feira do Produtor Rural Willi Dummer, no município de Camaquã/RS. A iniciativa surgiu da observação direta do evento, realizado semanalmente às manhãs de sábado, onde foi possível constatar a ausência de ferramentas digitais nos processos de divulgação e comercialização dos produtos ofertados pelos agricultores locais.

A Feira do Produtor Rural Willi Dummer representa uma importante fonte de renda para pequenos produtores da região, mas sua dinâmica presencial e o horário restrito limitam significativamente o alcance das vendas. Sem um canal digital, os produtores perdem oportunidades de negócio fora do período do evento e enfrentam dificuldades para organizar seus pedidos com antecedência. Essa lacuna motivou a proposta de um sistema que permitisse gerenciar os quatro pilares essenciais da cadeia comercial: o produtor rural, o produto, o cliente e a venda.

## 1.1 Objetivos {#objetivos}

Nas seções abaixo estão descritos o objetivo geral e os objetivos específicos desta pesquisa.

### 1.1.1 Objetivo Geral {#objetivo-geral}

Desenvolver uma plataforma digital para intermediar pedidos entre consumidores e produtores rurais da Feira do Produtor Rural Willi Dummer, em Camaquã/RS, permitindo o cadastro de produtos, a realização de pedidos e o acompanhamento do status de cada venda, com perfis distintos para produtor, cliente e administrador, utilizando Django REST Framework no backend e Vue.js no frontend, com retirada dos pedidos na própria feira.

### 1.1.2 Objetivos Específicos {#objetivos-específicos}

Para alcançar o objetivo geral, foram definidos os seguintes objetivos específicos:

- Realizar pesquisa bibliográfica sobre agricultura familiar, feiras de produtores rurais, plataformas digitais B2C e tecnologias de desenvolvimento web;

- Realizar o levantamento dos requisitos funcionais e não funcionais do sistema, com base na observação da dinâmica da Feira do Produtor Rural Willi Dummer, em Camaquã/RS;

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

No contexto do Agro Store, o modelo B2C é utilizado como referência conceitual, uma vez que os produtores rurais participantes da plataforma precisam possuir CNPJ para atuar na feira física. Dessa forma, os produtores cadastrados são tratados no sistema como fornecedores formalizados, que disponibilizam seus produtos diretamente aos consumidores finais. Embora a retirada dos pedidos ocorra presencialmente na feira, o processo de divulgação, seleção de produtos e geração de pedidos é realizado por meio da plataforma digital, aproximando a solução do modelo de comercialização direta entre fornecedor e consumidor.

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

<!-- orientador: revisar -->
- Permitir o cadastro público de usuários clientes, utilizando o CPF como identificador único e iniciando a sessão do usuário ao final do cadastro, sendo o perfil de produtor rural atribuído pela administração da plataforma.

<!-- orientador: revisar -->
- Permitir que cada usuário mantenha um ou mais telefones de contato, classificados nos tipos Celular, Fixo ou Comercial, com exatamente um deles indicado como principal, validando a quantidade de dígitos do número de acordo com o tipo informado e impedindo que o usuário fique sem telefone ou sem telefone principal ao excluir registros.

- Autenticar os usuários por meio de CPF e senha, retornando tokens de acesso e de renovação no padrão JWT (JSON Web Token), os quais serão utilizados nas requisições subsequentes para validação da identidade e das permissões do usuário.

- Permitir que usuários com perfil de produtor rural criem e gerenciem sua loja na plataforma, incluindo o cadastro de nome, descrição, CNPJ, imagem de perfil e cadastro de produtos sendo o vínculo entre o usuário e a loja estabelecido automaticamente pelo sistema.

- Disponibilizar um catálogo público de produtos, organizado por categorias, com informações de nome, descrição e preço, acessível a visitantes não autenticados.

- Registrar o histórico de preços de cada produto com controle de vigência, de forma que o sistema encerre automaticamente o preço anterior ao cadastrar um novo registro de preço, preservando o histórico de variações.

- Permitir que usuários autenticados adicionem, atualizem e removam produtos de seu carrinho de compras, com soma automática de quantidade para itens já presentes.

- Converter os itens selecionados do carrinho em pedidos, agrupando-os por loja e gerando, para cada pedido, um registro dos dados do cliente e dos produtos no momento da compra, removendo os itens processados do carrinho ao final da operação.

<!-- orientador: revisar -->
- Acompanhamento e a atualização do status dos pedidos, que percorrem os seguintes estados: Pendente, Em preparo, Pronto para retirada, Entregue e Cancelado, possibilitando que o produtor gerencie o andamento de cada pedido recebido.

- Usuários autenticados favoritam e desfavoritam produtos, garantindo a unicidade do vínculo entre usuário e produto para impedir registros duplicados.

- Usuários autenticados avaliem produtos pertencentes a pedidos com status Entregue, atribuindo uma nota de um a cinco e um comentário opcional, sendo permitida apenas uma avaliação por item de pedido.

- Produtor rural terá uma interface de gerenciamento de sua loja, permitindo a visualização dos pedidos recebidos e a atualização de seus respectivos status.

- Controlar a disponibilidade dos produtos a partir do estoque, retirando da listagem e da busca do catálogo os produtos com estoque zerado, sem inativá-los, e sinalizando ao produtor os produtos com estoque baixo, definido como até cinco unidades.

- Limitar a quantidade de cada item do carrinho ao estoque disponível do produto, ajustando automaticamente os carrinhos afetados quando o estoque diminuir e impedindo a finalização de itens sem estoque.

<!-- orientador: revisar -->
- Permitir que o usuário que esqueceu a senha solicite, informando o e-mail da conta, o envio de um *link* de redefinição com validade de trinta minutos e uso único, por meio do qual possa cadastrar uma nova senha, submetida às mesmas validações do cadastro, sem que o sistema revele se o e-mail informado pertence a uma conta e sem autenticar o usuário automaticamente ao final do processo.

### 3.1.2 Requisitos não funcionais {#requisitos-não-funcionais}

- O sistema deve expor seus recursos por meio de uma API REST com retorno de dados no formato JSON, seguindo os princípios arquiteturais REST.

- A autenticação deve ser implementada por meio de tokens JWT, com token de acesso de validade de cento e vinte minutos e token de renovação de validade de um dia, protegendo os endpoints que exigem identificação do usuário.

- O *frontend* e o backend serão projetos independentes que se comunicam exclusivamente via HTTP, possibilitando suportar o uso de múltiplos usuários na mesma API sem alterações no servidor.

- A interface do usuário deve ser acessível por meio de navegador web, sem necessidade de instalação de software adicional, sendo responsivo.

- Os dados dos usuários devem ser armazenados de forma segura, com senhas protegidas pelo algoritmo de hash PBKDF2.

- O banco de dados deve garantir a integridade referencial dos dados por meio de restrições de unicidade e chaves estrangeiras, assegurando, entre outros, a unicidade de CPF, e-mail, CNPJ e SKU no sistema.

- A arquitetura modular do backend, organizada em aplicações de domínio independentes, deve possibilitar a adição de novos módulos e funcionalidades sem impacto sobre os módulos existentes, favorecendo a escalabilidade do sistema.

- O sistema deve impedir a venda de quantidade superior ao estoque disponível, inclusive quando houver pedidos simultâneos para o mesmo produto, por meio de controle de concorrência no banco de dados.

<!-- orientador: revisar -->
- O processo de redefinição de senha deve armazenar apenas o resumo criptográfico (*hash*) do código enviado por e-mail, nunca o código em si, e limitar a quantidade de solicitações e de tentativas de confirmação por endereço de origem, reduzindo o risco de uso indevido e de tentativas sucessivas de adivinhação.

## 3.2 Modelagem {#modelagem}

### 3.2.1 Confecção de Diagramas {#confecção-de-diagramas}

A modelagem de um sistema de software envolve a construção de representações abstratas que permitem compreender, comunicar e validar suas estruturas e comportamentos antes mesmo de sua implementação.

Nesta seção, a organização dos dados do sistema é abordada por meio do Diagrama Entidade-Relacionamento (DER) e do Modelo Lógico do banco de dados, que descrevem as entidades, seus atributos e os vínculos estabelecidos entre elas. Complementarmente, são apresentados diagramas UML (Unified Modeling Language), que documentam o comportamento do sistema sob diferentes perspectivas: o diagrama de casos de uso mapeia as funcionalidades disponíveis e os atores que delas fazem uso; o diagrama de sequência ilustra a troca de mensagens entre os componentes ao longo do tempo; e o diagrama de atividades detalha os fluxos de decisão internos da aplicação.

<!-- orientador: revisar -->
Com exceção do modelo conceitual (Figura 1), elaborado na notação de Peter Chen, os diagramas deste trabalho foram produzidos com o Mermaid, ferramenta de código aberto que gera diagramas a partir de uma descrição textual [CITAÇÃO NECESSÁRIA]. Essa abordagem permite manter o código-fonte de cada diagrama versionado junto ao código do sistema e atualizá-lo sempre que uma regra de negócio é alterada, favorecendo a coerência entre a modelagem e a implementação. Como o Mermaid não oferece um tipo específico para diagramas de casos de uso nem para diagramas de atividades da UML, esses dois diagramas foram representados por fluxogramas que aproximam a notação original. Os diagramas foram exportados como imagens para inclusão no texto.

### 3.2.2 Modelagem do Banco de Dados {#modelagem-do-banco-de-dados}

Nesta seção são apresentados o Diagrama Entidade-Relacionamento (DER) e o Modelo Lógico do banco de dados da aplicação desenvolvida. Tais diagramas buscam descrever, de maneira gráfica e estruturada, a organização dos dados do sistema, destacando as entidades do sistema, com seus atributos e relacionamentos.

## 

### 3.2.3 Diagrama Entidade-Relacionamento (DER) {#diagrama-entidade-relacionamento-der}

O diagrama confeccionado para este trabalho apresenta as seguintes entidades, com suas respectivas relações.

<!-- orientador: revisar -->
**Cliente**: representa os usuários cadastrados no sistema, armazenando os dados necessários para identificação, autenticação e controle de acesso, como nome, CPF, e-mail, data de nascimento, foto de perfil (opcional), senha, último login, além de indicadores como e_produtor, esta_ativo e e_superusuario. Os números de telefone não são armazenados diretamente nessa entidade, mas na entidade Telefone, descrita adiante, o que permite ao usuário manter mais de um contato. Relaciona-se com a entidade Loja, permitindo que usuários com perfil de produtor estejam vinculados a uma loja cadastrada na plataforma. Também se relaciona com as entidades Telefone, Favorito, Avaliação, Carrinho, Pedido_Cliente e Redefinicao_Senha, uma vez que um cliente pode cadastrar seus telefones de contato, favoritar produtos, avaliar produtos adquiridos, possuir carrinhos de compra, ter seus dados preservados no momento da compra e solicitar a redefinição de sua senha. O vínculo entre o cliente e os pedidos que realiza não é registrado diretamente na entidade Pedido, mas por intermédio da entidade Pedido_Cliente, na cardinalidade (1,1) para (0,n): um cliente pode estar associado a nenhum ou a diversos registros de Pedido_Cliente, enquanto cada registro pertence a exatamente um cliente.

**Loja**: representa as lojas cadastradas pelos produtores rurais na plataforma, armazenando informações como nome, descrição, CNPJ, imagem de perfil e situação de atividade. Relaciona-se com a entidade Cliente, pois uma loja pertence a um usuário produtor, e com a entidade Pedido, visto que uma loja pode receber diversos pedidos. Também se relaciona com a entidade Carrinho, permitindo que os itens adicionados pelos clientes sejam organizados conforme a loja responsável pelos produtos.

<!-- orientador: revisar -->
O relacionamento entre Cliente e Loja ocorre na cardinalidade (0,1) para (1,1): cada loja pertence a exatamente um usuário produtor, e cada usuário possui no máximo uma loja, de modo que o usuário sem perfil de produtor não possui loja. Por decisão de projeto, a possibilidade de um mesmo produtor manter várias lojas não foi contemplada no MVP.

<!-- orientador: revisar -->
**Produto**: representa os produtos disponibilizados para comercialização na plataforma, armazenando informações como nome, descrição, código de barras, estoque, SKU, situação de atividade, data de criação e data de atualização. Relaciona-se com a entidade Preço, que armazena os valores associados ao produto; com a entidade Categoria, responsável pela classificação dos produtos; com a entidade Imagem, já que um produto pode possuir de nenhuma a cinco imagens; com a entidade Favorito, pois pode ser favoritado por diferentes clientes; com a entidade Avaliação, uma vez que pode receber avaliações; com a entidade Pedido_Produto, representando sua participação em pedidos; e com a entidade Carrinho_Produto, representando sua inclusão nos carrinhos de compra.

**Preço**: armazena os dados referentes à precificação dos produtos, incluindo valor de venda, valor de custo, valor de desconto, porcentagem de desconto, vigência inicial, vigência final, data de criação e data de atualização. Relaciona-se com a entidade Produto, permitindo que os valores praticados sejam associados aos produtos comercializados na plataforma.

**Categoria**: armazena os dados referentes às categorias dos produtos, como nome, status, data de criação e data de atualização. Relaciona-se com a entidade Produto na cardinalidade 1:N, pois uma categoria pode estar associada a diversos produtos, enquanto cada produto pertence a uma categoria.

<!-- orientador: revisar -->
**Imagem**: armazena os dados das imagens vinculadas aos produtos, como caminho da imagem, ordem de exibição, indicador de imagem principal, data de criação e data de atualização. Relaciona-se com a entidade Produto na cardinalidade (0,n) para (1,1): cada imagem pertence a exatamente um produto, enquanto um produto pode não possuir imagem ou possuir até cinco imagens, limite verificado pela aplicação. Quando há imagens cadastradas, exatamente uma delas é a principal.

**Carrinho**: representa o agrupamento dos produtos selecionados por um cliente antes da geração do pedido, armazenando valores como valor líquido, valor bruto, valor de desconto, data de criação e data de atualização. Relaciona-se com a entidade Cliente, indicando o usuário proprietário do carrinho, e com a entidade Loja, permitindo que os carrinhos sejam organizados de acordo com a loja responsável pelos produtos. Os produtos inseridos no carrinho são representados pela entidade Carrinho_Produto.

**Carrinho_Produto**: entidade associativa que representa os itens adicionados ao carrinho de compras. Armazena dados como quantidade, data de criação e data de atualização, além de estabelecer o vínculo entre Carrinho e Produto. Essa entidade permite que um carrinho possua múltiplos produtos e que um mesmo produto possa aparecer em diferentes carrinhos de clientes distintos.

**Pedidos**: representa os pedidos gerados a partir dos itens selecionados no carrinho, armazenando informações financeiras como valor líquido, valor bruto e valor de desconto, além de data de criação e data de atualização. Relaciona-se com a entidade Loja, pois cada pedido está associado à loja responsável pelos produtos; com a entidade Status_Pedido, que indica a situação atual do pedido; com a entidade Pedido_Produto, que armazena os itens do pedido; e com a entidade Pedido_Cliente, na cardinalidade (1,1) para (1,1), que identifica o cliente responsável pela compra e preserva os seus dados no momento em que o pedido foi gerado. Dessa forma, a entidade Pedido não possui referência direta ao cliente.

**Pedido_Produto**: entidade associativa que representa os produtos pertencentes a um pedido, armazenando informações como nome do produto, quantidade, valor unitário, valor de desconto, subtotal, data de criação e data de atualização. Relaciona-se com as entidades Pedido e Produto, refletindo a relação entre os pedidos realizados e os produtos adquiridos. Essa estrutura também permite preservar informações do produto no momento da compra, mesmo que seus dados sejam alterados posteriormente no cadastro original.

**Pedido_Cliente**: armazena os dados do cliente no momento da geração do pedido, como nome, CPF, e-mail, data de nascimento e gênero. Esse conjunto de dados constitui um *snapshot*, isto é, uma cópia das informações tal como se encontravam no instante da compra. Por decisão de projeto, o telefone do cliente não integra esse *snapshot*: quando necessário para a retirada, ele é consultado no cadastro atual do cliente, conforme justificado na Seção 4.7. A entidade cumpre duas funções: estabelece o vínculo entre o pedido e o cliente que o realizou e preserva o registro histórico das informações utilizadas na compra. Relaciona-se com a entidade Pedido na cardinalidade (1,1) para (1,1), pois cada pedido possui exatamente um registro de dados do cliente, e com a entidade Cliente na cardinalidade (0,n) para (1,1), pois cada registro pertence a um único cliente, que pode acumular diversos pedidos ao longo do tempo. Essa entidade é importante para preservar os dados do pedido mesmo que o cliente altere posteriormente suas informações cadastrais.

A concentração do vínculo com o cliente e do *snapshot* em uma mesma entidade, separada de Pedido, foi adotada para evitar que a mesma informação seja mantida em dois lugares e para reforçar a preservação do histórico de compras. Com essa organização, a entidade Pedido descreve apenas a transação comercial com a loja, enquanto a identificação do comprador permanece associada aos dados registrados no momento da compra, o que contribui para a integridade e a rastreabilidade das informações.

<!-- orientador: revisar -->
**Status_Pedido**: armazena os possíveis status que um pedido pode assumir durante seu ciclo de vida, como Pendente, Em preparo, Pronto para retirada, Entregue e Cancelado. Relaciona-se com a entidade Pedido na cardinalidade 1:N, pois um mesmo status pode estar associado a diversos pedidos.

**Favorito**: entidade associativa que representa o vínculo entre clientes e produtos favoritados, armazenando data de criação e data de atualização. Relaciona-se com as entidades Cliente e Produto, refletindo uma relação N:N, na qual um cliente pode favoritar diversos produtos e um produto pode ser favoritado por diferentes clientes.

**Avaliação**: armazena os registros de avaliações realizadas pelos clientes sobre os produtos adquiridos, contendo dados como nota, comentário, data de criação e data de atualização. Relaciona-se com a entidade Pedido_Produto, que representa o item do pedido, na cardinalidade (0,1) para (1,1): cada avaliação refere-se a exatamente um item de pedido, e cada item de pedido pode receber no máximo uma avaliação. Relaciona-se também com as entidades Cliente e Produto, permitindo identificar qual cliente realizou a avaliação e qual produto foi avaliado; nesses casos, um cliente pode registrar diversas avaliações e um produto pode receber diversas avaliações, enquanto cada avaliação pertence a um único cliente e a um único produto. A associação com o pedido ocorre de forma indireta, por meio do item avaliado, o que contribui para que somente produtos efetivamente comprados possam ser avaliados.

**Gênero**: armazena os dados referentes aos gêneros disponíveis para classificação dos clientes cadastrados no sistema, por meio do atributo gênero. Relaciona-se com a entidade Cliente, permitindo associar os usuários ao respectivo gênero informado no cadastro.

<!-- orientador: revisar -->
**Telefone**: armazena os telefones de contato dos clientes, contendo o número, com o DDD (Discagem Direta a Distância), um indicador de telefone principal, a data de criação e a data de atualização. Relaciona-se com a entidade Cliente na cardinalidade (1,n) para (1,1): cada telefone pertence a exatamente um cliente, e cada cliente possui ao menos um telefone, podendo possuir diversos, sem limite de quantidade, dos quais exatamente um é o principal. Essa cardinalidade mínima representa a regra de negócio adotada, segundo a qual todo usuário mantém ao menos um meio de contato. No modelo lógico (Figura 2), o mesmo relacionamento aparece com a cardinalidade (0,n), pois o banco de dados não impõe esse mínimo: ele é garantido pela aplicação, conforme a Seção 3.2.4, e o banco admite a exceção das contas anteriores a essa funcionalidade e das contas de superusuário criadas pela linha de comando, descrita na Seção 4.4. Relaciona-se também com a entidade Tipo_Telefone, que classifica cada número. Não há restrição de unicidade sobre o número, de modo que um mesmo telefone pode estar cadastrado para clientes diferentes, como pode ocorrer com um telefone compartilhado por membros de uma mesma família.

<!-- orientador: revisar -->
**Tipo_Telefone**: armazena os tipos de telefone admitidos pelo sistema, por meio do atributo descrição, cujos valores são Celular, Fixo e Comercial. Esses tipos são previamente carregados no banco de dados e não são cadastrados pelos usuários. Relaciona-se com a entidade Telefone na cardinalidade (1,1) para (0,n): cada telefone possui exatamente um tipo, e um tipo pode classificar diversos telefones.

<!-- orientador: revisar -->
**Redefinicao_Senha**: armazena as solicitações de redefinição de senha realizadas pelos clientes, contendo o resumo criptográfico (*hash*) do código enviado por e-mail, a data de expiração, a data de utilização e a data de criação. Relaciona-se com a entidade Cliente na cardinalidade (0,n) para (1,1): cada solicitação pertence a exatamente um cliente, enquanto um cliente pode não possuir nenhuma solicitação ou acumular diversas ao longo do tempo, uma vez que o histórico das solicitações é preservado. A data de utilização, quando preenchida, indica que o *link* correspondente já foi utilizado ou invalidado e não pode mais ser aceito.

Abaixo, apresenta-se a Figura 1, referente ao Diagrama Entidade-Relacionamento, confeccionado na etapa de modelagem do sistema.

###### 

###### Figura 1 - Modelo Conceitual do Diagrama Entidade-Relacionamento

<!-- autor: redesenhar a Figura 1 (versão 2.2, coerente com docs/modelo-logico.sql e a Figura 2). (1) Remover o atributo "telefone celular" da entidade Cliente. (2) Incluir a entidade Telefone, com os atributos numero (texto, somente dígitos com DDD, e não NUMERIC como na variante 2.1), e_principal, data_criacao e data_atualizacao. (3) Incluir a entidade Tipo_Telefone, com o atributo descricao (Celular, Fixo, Comercial). (4) Relacionamento Cliente (1,1) — possui — (1,n) Telefone (regra de negócio: todo usuário tem ao menos um telefone; a Figura 2 mantém (0,n), conforme explicado no texto da entidade Telefone). (5) Relacionamento Tipo_Telefone (1,1) — classifica — (0,n) Telefone. (6) Remover o atributo telefone da entidade Pedido_Cliente. Sugestão de legenda, mantida sem alteração: "Figura 1 - Modelo Conceitual do Diagrama Entidade-Relacionamento". -->
![](media/image1.png){width="8.810859580052494in" height="5.338041338582677in"}

**Fonte:** Confeccionado pelo autor (2026).

### 3.2.4 Modelo Lógico {#modelo-lógico}

<!-- orientador: revisar -->
A partir do modelo conceitual, foi elaborado o modelo lógico do banco de dados, apresentado na Figura 2. Nessa representação, as entidades são convertidas em tabelas, com a definição dos tipos de dados de cada coluna, das chaves primárias e das chaves estrangeiras responsáveis por materializar os relacionamentos entre os dados. Os relacionamentos N:N identificados no DER, como o vínculo entre pedidos e produtos, entre clientes e produtos favoritados e entre carrinhos e produtos, dão origem às tabelas associativas pedido_produto, favorito e carrinho_produto. Além disso, as restrições de unicidade, como as aplicadas a cpf, email, cnpj, sku, status e token_hash, contribuem para assegurar a integridade dos dados prevista nos requisitos não funcionais do sistema.

<!-- orientador: revisar -->
A tabela de imagens dos produtos possui, além da chave estrangeira para o produto, uma restrição de unicidade condicional, isto é, aplicada apenas às linhas que atendem a uma condição: entre as imagens de um mesmo produto, somente uma pode estar marcada como principal. Dessa forma, o próprio banco de dados impede a existência de duas imagens principais para o mesmo produto, enquanto o limite de cinco imagens por produto é verificado pela aplicação.

No modelo lógico, a tabela pedido possui chaves estrangeiras apenas para loja e status_pedido, enquanto a referência ao cliente fica na tabela pedido_cliente, por meio da coluna id_usuario, de preenchimento obrigatório. A coluna id_pedido dessa tabela é única, o que materializa a relação um-para-um com o pedido. Para preservar o histórico de pedidos, as chaves estrangeiras de pedido_cliente para o usuário e de pedido para a loja utilizam a regra de exclusão restritiva (ON DELETE RESTRICT), segundo a qual o banco de dados recusa a exclusão de um registro enquanto existirem outros registros que dependem dele. Assim, não é possível excluir um usuário ou uma loja que possua pedidos associados. Essa escolha substitui a exclusão em cascata (ON DELETE CASCADE), na qual a remoção do registro principal provocaria a remoção automática dos pedidos vinculados e, consequentemente, a perda do histórico de vendas e de compras.

<!-- orientador: revisar -->
Na tabela loja, a coluna proprietario_id, que referencia o usuário produtor, também é única, o que materializa a relação de no máximo uma loja por produtor. Essa restrição de unicidade complementa a validação realizada pela API e garante a regra mesmo quando duas requisições de criação de loja para o mesmo produtor são processadas simultaneamente: nesse caso, o banco de dados recusa a segunda inclusão, e a API responde com a mesma mensagem de validação apresentada ao usuário. A chave estrangeira dessa coluna adota igualmente a regra de exclusão restritiva, de forma que um produtor que possua loja não pode ser excluído, ainda que a loja não tenha recebido pedidos, e a loja nunca é removida em cascata junto com o seu proprietário.

<!-- orientador: revisar -->
A tabela redefinicao_senha possui chave estrangeira obrigatória para o usuário e uma restrição de unicidade sobre a coluna token_hash, que armazena o *hash* do código enviado no *link* de redefinição. O *hash* é o resultado de uma função criptográfica de mão única, que transforma um valor em uma sequência de tamanho fixo da qual não é possível recuperar o valor original [CITAÇÃO NECESSÁRIA]; no sistema, utiliza-se o algoritmo SHA-256 [CITAÇÃO NECESSÁRIA]. Assim, mesmo que o conteúdo do banco de dados seja exposto, os códigos dos *links* válidos não podem ser obtidos a partir dele. A tabela possui ainda uma restrição de verificação (CHECK), isto é, uma condição que toda linha deve satisfazer para ser gravada, que exige que a data de expiração seja posterior à data de criação. Diferentemente das tabelas ligadas aos pedidos, a chave estrangeira para o usuário utiliza a exclusão em cascata (ON DELETE CASCADE): como os registros de redefinição de senha são auxiliares ao acesso e não compõem o histórico comercial, não há razão para que impeçam a exclusão de um usuário, e são removidos junto com ele.

<!-- orientador: revisar -->
A restrição de unicidade condicional descrita para as imagens dos produtos também é empregada na tabela telefone, que possui chaves estrangeiras obrigatórias para o usuário e para o tipo de telefone: entre os telefones de um mesmo usuário, no máximo um pode estar marcado como principal. A exigência de que exista exatamente um telefone principal, e de que o usuário mantenha ao menos um telefone, é completada pela aplicação, que marca automaticamente como principal o primeiro telefone cadastrado e recusa a exclusão do último telefone e do telefone principal. Por essa razão, na Figura 2 o relacionamento entre usuario e telefone é representado com a cardinalidade (0,n), que corresponde ao que o banco de dados efetivamente impõe e acomoda as contas sem telefone descritas na Seção 4.4, enquanto o DER (Figura 1) adota (1,n), por representar a regra de negócio. A coluna numero é do tipo texto e armazena somente os dígitos, com o DDD, seguindo o mesmo critério adotado para CPF, CNPJ e SKU: trata-se de um identificador sobre o qual não se realizam operações aritméticas, e a quantidade de dígitos é relevante para a validação de acordo com o tipo. A tabela tipo_telefone possui restrição de unicidade sobre a coluna descricao. Assim como na tabela redefinicao_senha, a chave estrangeira de telefone para o usuário utiliza a exclusão em cascata, pois os telefones são dados auxiliares do cadastro e não compõem o histórico comercial; já a chave estrangeira para o tipo utiliza a exclusão restritiva, o que impede a remoção de um tipo que ainda classifique algum telefone. Com a criação dessas tabelas, as colunas de telefone das tabelas usuario e pedido_cliente foram removidas, e os telefones existentes foram transferidos para a nova estrutura, conforme descrito na Seção 4.4.

###### Figura 2 - Modelo Lógico do Diagrama Entidade-Relacionamento

![](diagramas/fig02-modelo-logico.png){width="6.3in"}

**Fonte:** Confeccionado pelo autor (2026).

### 3.2.5 Diagramas UML {#diagramas-uml}

Nesta seção são apresentados os diagramas UML elaborados durante a modelagem do sistema proposto. Os diagramas têm como objetivo representar de forma visual e estruturada o funcionamento da aplicação e a interação entre seus componentes, contemplando diagramas de casos de uso, de sequência e de atividade, que auxiliam na compreensão de fluxos e comportamentos do sistema.

#### 3.2.5.1 Diagrama de Casos de Uso {#diagrama-de-casos-de-uso}

Conforme detalhado nos requisitos do sistema, a distinção entre os perfis de usuários exige a especificação das ações permitidas a cada um, caracterizando-os como atores do sistema. Dessa forma, a Figura 3 apresenta o Diagrama de Casos de Uso do Agro Store, que ilustra as interações entre esses atores e as funcionalidades disponíveis na plataforma.

- **Atores:**

<!-- -->

<!-- orientador: revisar -->
- **Visitante:** representa a pessoa que acessa a plataforma sem estar autenticada. Pode consultar o catálogo, o detalhe dos produtos e as avaliações publicadas, além de criar sua conta de cliente e, caso já possua conta e tenha esquecido a senha, solicitar a redefinição.

<!-- orientador: revisar -->
- **Cliente:** representa o usuário consumidor da plataforma, responsável por acessar o catálogo de produtos, adicionar itens ao carrinho, realizar pedidos, acompanhar o andamento das compras, cancelar pedidos ainda pendentes, editar seus dados de perfil, favoritar produtos e avaliar os itens de pedidos entregues. Esse ator utiliza o sistema com o objetivo de consultar os produtos disponibilizados pelos produtores rurais e realizar pedidos para posterior retirada na feira física.

<!-- orientador: revisar -->
- **Produtor Rural:** representa o usuário responsável pela comercialização dos produtos na plataforma. Por também ser um usuário da plataforma, o produtor herda as funcionalidades do cliente. Além delas, pode cadastrar sua loja, limitada a uma por produtor, gerenciar os dados da loja, cadastrar e manter produtos, preços e imagens, sugerir categorias, acompanhar os pedidos recebidos, cancelar pedidos que ainda não estejam prontos para retirada e atualizar o status dos pedidos conforme o andamento da preparação e da retirada na feira. Esse ator é fundamental para a manutenção do catálogo de produtos e para o atendimento das solicitações realizadas pelos clientes.

<!-- orientador: revisar -->
- **Administrador:** representa o usuário responsável pela gestão e validação de informações dentro da plataforma. Possui atribuições voltadas ao controle do sistema, como ativar ou renomear as categorias sugeridas pelos produtores e moderar as avaliações publicadas, garantindo que os registros disponibilizados na aplicação estejam adequados às regras de funcionamento da plataforma. A aprovação formal de produtores e lojas não faz parte do MVP e é tratada como trabalho futuro (Capítulo 5).

<!-- -->

- **Casos de Uso:**

<!-- -->

<!-- orientador: revisar -->
- **Cadastrar-se como cliente:** caso de uso disponível para o visitante. Permite a criação de uma conta de cliente na plataforma por meio do preenchimento dos dados pessoais necessários para identificação e acesso ao sistema. O cadastro público não cria contas de produtor nem de administrador: o perfil de produtor é atribuído pela administração da plataforma.

- **Efetuar login:** caso de uso base para todos os atores. Realiza a autenticação do usuário na plataforma, permitindo o acesso às funcionalidades de acordo com o perfil identificado.

<!-- orientador: revisar -->
- **Redefinir senha:** caso de uso disponível a qualquer usuário cadastrado que não esteja autenticado por ter esquecido a senha. O usuário informa o e-mail da conta e recebe, por e-mail, um *link* válido por trinta minutos e de uso único, por meio do qual cadastra uma nova senha. A resposta à solicitação é sempre a mesma, exista ou não uma conta com o e-mail informado, e, após a troca, o usuário deve efetuar login com a nova senha. O fluxo é detalhado na Seção 4.8.

<!-- orientador: revisar -->
- **Visualizar catálogo de produtos:** permite ao visitante e ao cliente consultar os produtos disponíveis na plataforma, visualizando informações como nome, descrição, preço, imagens, categoria e loja responsável pela oferta.

- **Gerenciar carrinho:** permite ao cliente adicionar produtos ao carrinho, alterar quantidades, remover itens e consultar os valores relacionados aos produtos selecionados antes da geração do pedido.

- **Realizar pedido:** possibilita ao cliente confirmar a compra dos itens selecionados no carrinho. A partir dessa ação, o sistema gera o pedido, registra os produtos adquiridos, calcula os valores correspondentes e preserva os dados do cliente no momento da compra.

<!-- orientador: revisar -->
- **Acompanhar pedido:** permite ao cliente consultar o andamento dos pedidos realizados, verificando o status atual de cada solicitação, como Pendente, Em preparo, Pronto para retirada, Entregue ou Cancelado.

<!-- orientador: revisar -->
- **Cancelar pedido pendente:** permite ao cliente cancelar um pedido próprio enquanto ele estiver com o status Pendente.

<!-- orientador: revisar -->
- **Editar perfil:** permite ao usuário alterar seus dados pessoais, com exceção do CPF e do perfil de acesso, gerenciar seus telefones de contato, adicionando, editando, excluindo e definindo o telefone principal, bem como enviar, trocar ou remover sua foto de perfil, que é opcional.

<!-- orientador: revisar -->
- **Favoritar produto:** permite ao usuário autenticado, seja cliente ou produtor, marcar produtos de interesse para facilitar consultas futuras. Essa funcionalidade cria um vínculo entre o usuário e o produto favoritado.

<!-- orientador: revisar -->
- **Avaliar item entregue:** possibilita ao cliente registrar uma avaliação sobre um item de pedido com status Entregue, informando uma nota e, opcionalmente, um comentário, garantindo que apenas produtos comprados possam ser avaliados.

<!-- orientador: revisar -->
- **Consultar avaliações do produto:** permite a qualquer pessoa, autenticada ou não, consultar as avaliações publicadas na página de detalhe do produto.

<!-- orientador: revisar -->
- **Cadastrar loja:** funcionalidade atribuída ao produtor rural. Permite que o usuário com perfil de produtor cadastre sua loja na plataforma, informando nome, descrição e CNPJ e, opcionalmente, uma imagem da loja. Cada produtor pode possuir somente uma loja.

<!-- orientador: revisar -->
- **Gerenciar loja:** permite ao produtor rural consultar e atualizar o nome, a descrição e a imagem de sua loja, bem como desativá-la, mantendo os dados de apresentação disponíveis aos clientes da plataforma.

<!-- orientador: revisar -->
- **Gerenciar produtos, preços e imagens:** permite ao produtor rural cadastrar, consultar, atualizar e desativar produtos vinculados à sua loja, incluindo informações como nome, descrição, categoria, estoque, código de barras, preços e imagens. O SKU é gerado automaticamente pelo sistema.

<!-- orientador: revisar -->
- **Atualizar status do pedido:** funcionalidade atribuída ao produtor rural. Permite alterar o andamento dos pedidos recebidos, indicando as etapas de preparação dos produtos solicitados pelos clientes e de sua retirada na feira.

<!-- orientador: revisar -->
- **Cancelar pedido da loja:** permite ao produtor rural cancelar um pedido recebido enquanto ele estiver com o status Pendente ou Em preparo.

<!-- orientador: revisar -->
- **Sugerir categoria:** permite ao produtor rural sugerir uma nova categoria de produtos quando as categorias existentes não forem suficientes para classificar adequadamente seus itens. A categoria sugerida é criada inativa.

<!-- orientador: revisar -->
- **Ativar ou renomear categoria:** funcionalidade atribuída ao administrador. Permite ativar as categorias sugeridas pelos produtores, bem como renomeá-las ou inativá-las, mantendo a organização e a padronização do catálogo de produtos.

<!-- orientador: revisar -->
- **Moderar avaliações:** funcionalidade atribuída ao administrador. Permite consultar e remover avaliações pela área administrativa, sem a possibilidade de criá-las ou editá-las.

<!-- orientador: revisar -->
- **Solicitar habilitação e criação de loja** e **Aprovar produtor e loja:** casos de uso previstos na modelagem inicial, nos quais o usuário solicitaria a habilitação como produtor e o administrador aprovaria a solicitação. Esses casos de uso não foram implementados no MVP e aparecem tracejados na Figura 3. Eles são tratados como trabalhos futuros no Capítulo 5.

<!-- orientador: revisar -->
Na Figura 3, encontra-se o Diagrama de Casos de Uso, que apresenta graficamente a relação entre os atores do sistema e as funcionalidades disponíveis na plataforma. Os atores são representados por retângulos, os casos de uso por elipses, e a seta tracejada indica que o produtor herda os casos de uso do cliente.

###### Figura 3 - Diagrama de Casos de Uso

![](diagramas/fig03-casos-de-uso.png){width="6.3in"}

**Fonte:** Confeccionado pelo autor (2026).

#### 

#### 3.2.5.2 Diagramas de Sequência {#diagramas-de-sequência}

Os diagramas de sequência apresentados nesta seção representam os principais fluxos de interação entre os atores do sistema e os componentes da arquitetura da aplicação. Cada diagrama descreve a ordem das mensagens trocadas entre o usuário, a interface web, a API/Backend e o banco de dados, permitindo compreender o comportamento dinâmico do sistema em funcionalidades essenciais do Agro Store.

##### 3.2.5.2.1 Diagrama de Sequência I - Cadastro de Usuário {#diagrama-de-sequência-i---cadastro-de-usuário}

<!-- orientador: revisar -->
O Diagrama de Sequência I busca representar visualmente a lógica por trás do processo de cadastro de um novo usuário na plataforma. Como o cadastro público cria somente contas de cliente, o fluxo é iniciado por um visitante. Possui a seguinte estrutura:

- **Atores:**

  - **Visitante:** pessoa que deseja realizar seu cadastro como cliente para acessar as funcionalidades do sistema.

  - **Frontend:** interface visual da aplicação, responsável por coletar os dados informados pelo usuário.

  - **API/Backend:** componente responsável por receber os dados, realizar validações, proteger a senha e solicitar a gravação das informações.

  - **Banco de dados:** componente responsável pela persistência dos dados do novo usuário.

<!-- -->

- **Fluxo de Eventos:**

  <!-- orientador: revisar -->

  - **Preenche dados de cadastro:** o fluxo inicia-se quando o visitante informa seus dados pessoais na interface: nome, CPF, e-mail, um telefone e o respectivo tipo (Celular, Fixo ou Comercial), data de nascimento, gênero, senha e confirmação da senha. Os tipos de telefone disponíveis são obtidos da API por meio de uma consulta pública, uma vez que o visitante ainda não está autenticado.

  - **Envia dados de cadastro:** o *frontend* encaminha as informações preenchidas para a API/Backend.

  - **Valida os dados informados:** a API/Backend consulta o banco de dados para verificar se o CPF e o e-mail já estão cadastrados e valida os demais dados: o CPF deve ser válido, o telefone deve possuir a quantidade de dígitos correspondente ao tipo informado, considerando o DDD (onze dígitos para Celular, dez para Fixo e dez ou onze para Comercial), o usuário deve ter pelo menos dezesseis anos, o gênero deve corresponder a uma opção disponível e a senha deve atender aos critérios mínimos de segurança. Campos que concederiam privilégios, como o perfil de produtor, são desconsiderados.

  - **Retorna erro de validação:** caso algum dado seja inválido ou já esteja cadastrado, a API/Backend retorna a mensagem correspondente a cada campo, e o *frontend* solicita a correção das informações.

  - **Protege a senha do usuário:** caso os dados sejam válidos, a senha é protegida por meio de algoritmo de hash antes de ser armazenada.

  - **Salva novo usuário:** a API/Backend solicita ao banco de dados a criação do registro do usuário com perfil de cliente e de seu telefone, registrado como telefone principal.

  - **Confirma cadastro:** o banco de dados confirma a persistência das informações.

  - **Gera os tokens de acesso:** a API/Backend gera os tokens JWT de acesso e de renovação do novo usuário.

  - **Retorna usuário cadastrado:** a API/Backend retorna ao *frontend* os tokens e os dados do perfil.

  - **Inicia a sessão:** o *frontend* armazena a sessão e apresenta ao usuário a área autenticada, sem a necessidade de um login adicional.

Abaixo, a Figura 4 apresenta o Diagrama de Sequência I, que detalha o processo de cadastro de usuário.

###### Figura 4 - Diagrama de Sequência I - Cadastro de Usuário

<!-- autor: exportar novamente a imagem diagramas/fig04-seq-cadastro.png a partir do arquivo docs/diagramas/fig04-seq-cadastro.mmd, já atualizado -->

![](diagramas/fig04-seq-cadastro.png){width="6.3in"}

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

![](diagramas/fig05-seq-login.png){width="6.3in"}

**Fonte:** Confeccionado pelo autor (2026).

##### 3.2.5.2.3 Diagrama de Sequência III - Cadastro de Loja pelo Produtor {#diagrama-de-sequência-iii---cadastro-de-loja-pelo-produtor}

O Diagrama de Sequência III busca representar visualmente o processo de cadastro de uma loja por um usuário com perfil de produtor rural. Possui a seguinte estrutura:

- **Atores:**

  - **Produtor:** usuário responsável por cadastrar e gerenciar uma loja na plataforma.

  - **Frontend:** interface visual utilizada pelo produtor para informar os dados da loja.

  - **API/Backend:** componente responsável por verificar a autenticação, validar o perfil do usuário e solicitar a criação da loja.

  - **Banco de dados:** componente responsável por armazenar os dados da loja cadastrada.

  <!-- orientador: revisar -->
  - **Storage de arquivos:** componente responsável por armazenar o arquivo da imagem da loja, quando enviada.

<!-- -->

- **Fluxo de Eventos:**

  <!-- orientador: revisar -->

  - **Informa dados da loja:** o fluxo inicia-se quando o produtor preenche os dados necessários para criação da loja: nome, descrição e CNPJ. Opcionalmente, o produtor pode escolher, nessa mesma etapa, uma imagem para a loja, enviada junto com os demais dados; caso a imagem seja recusada pela validação, a loja não é criada e o produtor pode corrigir o arquivo, conforme descrito na Seção 4.4.

  - **Envia dados da loja:** o *frontend* encaminha as informações para a API/Backend.

  - **Verifica autenticação:** a API/Backend valida se o usuário está autenticado no sistema. Caso não esteja, a requisição é recusada.

  - **Valida os dados da loja:** quando uma imagem é enviada, a API/Backend confere sua extensão (JPG, PNG ou WEBP), seu tamanho, de até 5 MB, e seu conteúdo; se a imagem for recusada, é retornada a mensagem correspondente, e a loja não é criada. Em seguida, a API/Backend consulta o banco de dados e verifica, nesta ordem, se o CNPJ já está cadastrado, se o usuário possui perfil de produtor e se ele já possui uma loja, uma vez que cada produtor pode possuir somente uma loja. Em qualquer desses casos, a API/Backend retorna um erro de validação com a mensagem correspondente, e o processo é interrompido.

  - **Salva loja vinculada ao produtor:** caso os dados sejam válidos, a API/Backend grava a imagem, quando enviada, no armazenamento de arquivos, com um nome gerado aleatoriamente, e solicita ao banco de dados a criação da loja, já ativa, vinculando-a ao usuário autenticado.

  - **Confirma criação da loja:** o banco de dados confirma o armazenamento das informações.

  - **Retorna dados da loja:** a API/Backend devolve ao *frontend* os dados cadastrados, incluindo o endereço da imagem, quando houver.

  - **Exibe loja cadastrada:** o *frontend* apresenta ao produtor a confirmação do cadastro.

<!-- orientador: revisar -->
A verificação de loja já existente, realizada pela API, é reforçada por uma restrição de unicidade no banco de dados, descrita na Seção 3.2.4. Assim, caso duas solicitações de cadastro de loja do mesmo produtor sejam processadas ao mesmo tempo e ambas passem pela verificação da API, o banco de dados recusa a segunda gravação, e o produtor recebe a mesma mensagem de erro de validação.

Abaixo, a Figura 6 apresenta o Diagrama de Sequência III, que detalha o processo de cadastro de loja pelo produtor.

###### Figura 6 - Diagrama de Sequência III - Cadastro de Loja pelo Produtor

![](diagramas/fig06-seq-cadastro-loja.png){width="6.3in"}

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

  <!-- orientador: revisar -->

  - **Preenche dados do produto:** o fluxo inicia-se quando o produtor informa os dados do produto, como nome, descrição, categoria, código de barras, estoque, preço de venda e percentual de desconto. A loja não é informada, pois o sistema vincula o produto automaticamente à loja do produtor autenticado.

  - **Envia produto:** o *frontend* encaminha os dados do produto para a API/Backend.

  - **Valida os dados do produto:** a API/Backend recusa estoque negativo e categoria inativa, retornando a mensagem correspondente.

  - **Verifica autenticação e perfil:** a API/Backend confirma se o usuário está autenticado, se possui perfil de produtor e se já cadastrou sua loja. Caso contrário, a operação é recusada.

  - **Salva produto e gera o SKU:** a API/Backend solicita ao banco de dados a gravação do novo produto e, na mesma transação, gera o SKU (*Stock Keeping Unit*, código de identificação do item em estoque) de forma automática, a partir dos identificadores da loja, da categoria e do produto.

  - **Confirma produto cadastrado:** o banco de dados confirma a criação do registro.

  - **Retorna produto criado:** a API/Backend devolve ao *frontend* as informações do produto cadastrado, incluindo o SKU.

  - **Envia preço do produto:** em seguida, o *frontend* encaminha à API/Backend o preço de venda e o percentual de desconto do produto.

  - **Valida o preço:** a API/Backend verifica se o percentual de desconto está entre 0 e 100 e se o produto pertence à loja do produtor.

  - **Encerra o preço anterior e calcula o desconto:** a API/Backend encerra a vigência do preço anterior, preservando o histórico de preços, e calcula o valor do desconto a partir do percentual informado.

  - **Salva preço vigente:** a API/Backend solicita ao banco de dados o armazenamento do novo preço vigente associado ao produto.

  - **Confirma preço cadastrado:** o banco de dados confirma a gravação das informações.

  - **Exibe produto com preço atual:** o *frontend* apresenta ao produtor o produto cadastrado com seu respectivo preço.

Abaixo, a Figura 7 apresenta o Diagrama de Sequência IV, que detalha o processo de cadastro de produto e definição de preço.

###### Figura 7 - Diagrama de Sequência IV - Cadastro de Produto e Definição de Preço

![](diagramas/fig07-seq-produto-preco.png){width="6.3in"}

**Fonte:** Confeccionado pelo autor (2026).

##### 3.2.5.2.5 Diagrama de Sequência V - Consulta de Catálogo de Produtos {#diagrama-de-sequência-v---consulta-de-catálogo-de-produtos}

O Diagrama de Sequência V busca representar visualmente o processo de consulta pública dos produtos disponíveis na plataforma. Possui a seguinte estrutura:

- **Atores:**

  - **Visitante ou cliente:** pessoa que acessa a plataforma para consultar os produtos disponíveis, com ou sem autenticação.

  - **Frontend:** interface visual responsável por apresentar o catálogo ao usuário.

  - **API/Backend:** componente responsável por buscar e organizar os dados dos produtos.

  - **Banco de dados:** componente onde são consultadas as informações de produtos, lojas, categorias e preços.

<!-- -->

- **Fluxo de Eventos:**

  - **Abre o catálogo de produtos:** o fluxo inicia-se quando o cliente acessa a área de catálogo da plataforma.

  - **Solicita lista de produtos:** o *frontend* envia à API/Backend uma solicitação para recuperar os produtos disponíveis.

  <!-- orientador: revisar -->

  - **Busca produtos, lojas, categorias, preços vigentes e imagens:** a API/Backend consulta o banco de dados para obter os produtos disponíveis, isto é, os produtos ativos, pertencentes a lojas ativas e com estoque maior que zero. Opcionalmente, a consulta pode ser filtrada por categoria.

  - **Retorna produtos encontrados:** o banco de dados devolve os registros localizados.

  - **Monta catálogo formatado:** a API/Backend organiza as informações, incluindo preço atual, preço original, desconto, quando houver, e o endereço da imagem principal de cada produto.

  - **Envia catálogo formatado:** a API/Backend retorna ao *frontend* a lista de produtos preparada para exibição.

  - **Exibe produtos disponíveis:** o *frontend* apresenta os produtos em cartões com a imagem principal ou, na ausência de imagens, com a indicação "Sem foto". Por se tratar de um recurso público, esse fluxo não exige autenticação.

  - **Acessa o detalhe pelo endereço direto:** de forma opcional, o usuário pode abrir a página de um produto ativo de loja ativa mesmo que seu estoque seja zero. Nesse caso, a página informa a condição "Sem estoque" e bloqueia a compra; caso contrário, exibe a galeria de imagens e permite a inclusão no carrinho.

Abaixo, a Figura 8 apresenta o Diagrama de Sequência V, que detalha o processo de consulta do catálogo de produtos.

###### Figura 8 - Diagrama de Sequência V - Consulta de Catálogo de Produtos

![](diagramas/fig08-seq-catalogo.png){width="6.3in"}

**Fonte:** Confeccionado pelo autor (2026).

#### 3.2.5.3 Diagrama de Atividades {#diagrama-de-atividades}

Finalizando a apresentação dos diagramas de modelagem UML, encontram-se os diagramas de atividades, responsáveis por representar o fluxo de execução das ações realizadas dentro de processos específicos do sistema. Esses diagramas permitem visualizar a sequência das atividades, os pontos de decisão e os possíveis caminhos alternativos existentes durante a utilização da plataforma.

##### 3.2.5.3.1 Diagrama de Atividades I - Geração de Pedido pelo Cliente {#diagrama-de-atividades-i---geração-de-pedido-pelo-cliente}

O Diagrama de Atividades I busca modelar o fluxo realizado pelo cliente desde o acesso ao catálogo de produtos até a geração do pedido. Esse processo representa uma das principais funcionalidades do Agro Store, pois descreve o caminho percorrido pelo consumidor para selecionar produtos disponíveis na plataforma, adicioná-los ao carrinho e confirmar a compra. O fluxo possui a seguinte estrutura:

- **Acessar catálogo de produtos:** descreve a ação inicial do cliente ao acessar a listagem de produtos disponíveis na plataforma. A partir dessa ação, o sistema busca os produtos disponíveis, isto é, os produtos ativos, pertencentes a lojas ativas e com estoque maior que zero, com suas respectivas lojas, categorias e preços vigentes, retornando o catálogo formatado para exibição ao usuário.

- **Selecionar produto:** representa a escolha de um item pelo cliente dentro do catálogo. Após a seleção, o sistema busca as informações detalhadas do produto, incluindo dados da loja, descrição, preço vigente e demais informações necessárias para que o cliente decida pela inclusão no carrinho.

- **Adicionar produto ao carrinho:** ocorre quando o cliente informa a quantidade desejada e solicita a inclusão do produto no carrinho. Essa ação gera um nó de decisão responsável por verificar se o cliente está autenticado. Caso não esteja autenticado \[Não\], o sistema informa a necessidade de realizar login e encerra o fluxo. Caso esteja autenticado \[Sim\], o processo continua.

  <!-- orientador: revisar -->

- **Verificar existência do produto no carrinho:** após a autenticação, o sistema verifica se o produto e a loja estão ativos, recusando a inclusão em caso contrário, e se o produto selecionado já está presente no carrinho do cliente. Caso o produto já exista \[Sim\], a quantidade informada é somada à quantidade já registrada. Caso o produto ainda não esteja no carrinho \[Não\], um novo item é criado. Em ambos os casos, a quantidade resultante fica limitada ao estoque disponível do produto: se a ultrapassar, a inclusão é recusada e o cliente é informado de que não há estoque suficiente. Quando a inclusão é aceita, o sistema consulta o preço vigente do produto e atualiza os valores do carrinho.

- **Exibir produto no carrinho:** representa o retorno visual ao cliente após a inclusão ou atualização do item. O sistema apresenta o carrinho atualizado, contendo os produtos selecionados, suas quantidades e os subtotais calculados.

- **Abrir carrinho:** descreve a ação do cliente ao acessar o resumo da compra. Nesse momento, o sistema busca os itens vinculados ao carrinho do usuário autenticado, retornando os produtos, lojas, quantidades e preços para exibição.

- **Alterar carrinho:** representa uma ação opcional do cliente antes da confirmação da compra. Caso deseje alterar o carrinho \[Sim\], o cliente pode modificar a quantidade de um item ou removê-lo. O sistema atualiza os dados e exibe novamente o resumo da compra. Caso não deseje realizar alterações \[Não\], o fluxo segue para a confirmação da compra.

- **Confirmar compra:** ocorre quando o cliente decide gerar o pedido a partir dos itens selecionados no carrinho. O sistema recebe a lista de itens e verifica novamente a credencial de acesso do cliente antes de buscar os itens pertencentes ao seu carrinho.

- **Verificar itens válidos:** esse nó de decisão valida se todos os itens enviados estão aptos para a geração do pedido. Um item é considerado inválido quando não pertence ao carrinho do cliente, quando o produto ou a loja estão inativos, quando sua quantidade é zero (item "Sem estoque"), quando o estoque é insuficiente para a quantidade solicitada ou quando o produto não possui preço vigente. Caso algum item seja inválido \[Não\], a finalização é recusada por inteiro: nenhum pedido é gerado e o cliente é informado do motivo, com a indicação do produto envolvido. Caso todos os itens sejam válidos \[Sim\], o sistema segue para o processamento da compra.

- **Agrupar itens por loja:** os itens selecionados são organizados de acordo com a loja responsável por cada produto. Essa etapa é necessária porque um mesmo carrinho pode conter produtos de diferentes produtores, exigindo a geração de pedidos separados para cada loja envolvida.

- **Calcular valores do pedido:** para cada loja envolvida, o sistema consulta os preços vigentes dos produtos, calcula o valor bruto, os descontos aplicáveis e o valor líquido do pedido.

- **Criar pedido:** após o cálculo dos valores, o sistema cria o pedido com status inicial Pendente, registra os produtos vinculados ao pedido e copia os dados do cliente para preservar as informações existentes no momento da compra.

- **Remover itens comprados do carrinho:** depois que os pedidos são criados, os itens processados são removidos do carrinho, evitando que permaneçam disponíveis para nova compra duplicada.

  <!-- orientador: revisar -->

- **Baixar o estoque e ajustar os carrinhos afetados:** na criação dos pedidos, o sistema subtrai do estoque de cada produto a quantidade vendida. Em seguida, nos carrinhos de outros clientes que contêm esses produtos, as quantidades que ultrapassam o novo estoque são reduzidas a esse valor, podendo chegar a zero, caso em que o item permanece no carrinho com a indicação "Sem estoque". Essas operações ocorrem na mesma transação da geração do pedido, conforme descrito na seção 4.1.

- **Exibir confirmação da compra:** ao final do processo, o sistema apresenta ao cliente a confirmação da compra realizada e informa que o pedido foi criado com status Pendente, encerrando o fluxo no nó final.

A seguir, apresenta-se a Figura 9, referente ao Diagrama de Atividades I, que descreve o processo de seleção de produto, inclusão no carrinho e geração de pedido pelo cliente.

###### Figura 9 - Diagrama de Atividades I - Geração de Pedido pelo Cliente

![](diagramas/fig09-atividades-pedido.png){width="6.3in"}

> **Fonte:** Confeccionado pelo autor (2026).

# [4 DESENVOLVIMENTO E RESULTADOS]{.smallcaps} {#desenvolvimento-e-resultados}

<!-- orientador: revisar -->
Este capítulo apresenta os resultados do desenvolvimento do Agro Store, descrevendo as funcionalidades implementadas no MVP (Produto Mínimo Viável, do inglês *Minimum Viable Product*), isto é, a versão do sistema que reúne o conjunto mínimo de funcionalidades necessário para demonstrar a proposta. O código do sistema foi organizado em um único repositório, que contém dois projetos independentes: a API REST, desenvolvida em Python com Django e Django REST Framework, e a interface web, desenvolvida com Vue.js. Durante o desenvolvimento, utilizou-se o banco de dados SQLite, enquanto o PostgreSQL é o banco de dados adotado para a versão final.

<!-- orientador: revisar -->
Ao longo da implementação, os requisitos levantados no Capítulo 3 foram detalhados em regras de negócio, isto é, em definições sobre como o sistema deve se comportar em cada situação. As seções a seguir apresentam essas regras e as decisões técnicas adotadas para garantir sua consistência. As regras críticas são sempre validadas no *backend*, de modo que a interface não seja a única camada de proteção. A Seção 4.9 descreve a verificação das funcionalidades, e as limitações identificadas são apresentadas no Capítulo 5.

<!-- orientador: revisar -->
## 4.1 Regras de Negócio de Estoque {#regras-de-negócio-de-estoque}

Durante o desenvolvimento, identificou-se a necessidade de regras específicas para o tratamento do estoque dos produtos, aspecto que não havia sido detalhado na versão inicial dos requisitos. Esta seção descreve as regras implementadas e as decisões técnicas adotadas para garantir sua consistência.

### 4.1.1 Disponibilidade dos Produtos por Estoque {#disponibilidade-dos-produtos-por-estoque}

Na versão inicial do sistema, não havia tratamento específico para produtos com estoque zerado ou reduzido, de modo que itens esgotados permaneciam listados no catálogo e podiam induzir o cliente a tentar uma compra impossível de ser atendida. Para corrigir essa situação, foi definida e implementada uma regra de disponibilidade baseada na quantidade em estoque. O produto cujo estoque atinge zero deixa de ser exibido na listagem pública do catálogo, sem que seu cadastro seja inativado. Como a busca do catálogo é realizada no *frontend* sobre o resultado dessa listagem fornecida pela API, o produto também deixa de ser encontrado pela busca. A página de detalhe permanece acessível por meio do endereço direto e informa a condição "Sem estoque", com a compra bloqueada. Quando o produtor repõe o estoque, o produto volta a ser exibido no catálogo automaticamente, sem nenhuma ação adicional. Essa decisão separa dois conceitos distintos: a inativação, que representa a decisão do produtor de retirar o produto de venda, e a indisponibilidade temporária, que decorre apenas da falta de unidades.

Para apoiar o produtor no acompanhamento do estoque, o sistema adota um limite único e global de cinco unidades para caracterizar o estoque baixo. Na área do produtor, os produtos com estoque entre uma e cinco unidades recebem o indicador "Estoque baixo", e os produtos com estoque zerado recebem o indicador "Sem estoque — fora do catálogo". Um aviso resumido informa a quantidade de produtos ativos em cada situação. Trata-se de uma sinalização apenas visual, exibida quando o produtor acessa a plataforma. Além disso, a API recusa, com mensagem explicativa, qualquer tentativa de registrar estoque negativo.

### 4.1.2 Coerência entre Carrinho e Estoque {#coerência-entre-carrinho-e-estoque}

Como o carrinho é persistido no servidor, a quantidade escolhida pelo cliente pode deixar de corresponder ao estoque real entre o momento da inclusão e o da finalização. Para manter a coerência, o sistema limita a quantidade de cada item ao estoque disponível do produto. Sempre que o estoque diminui, seja pela venda a outro cliente, seja por ajuste feito pelo produtor, as quantidades de todos os carrinhos que ultrapassam o novo estoque são reduzidas a esse valor e gravadas no banco de dados. Essa redução pode chegar a zero. Nesse caso, o item permanece no carrinho com a indicação "Sem estoque" e não pode ser finalizado. Se o cliente tentar finalizar um conjunto de itens que inclua um item nessa condição, a finalização é recusada por inteiro e nenhum pedido é gerado, seguindo o mesmo critério adotado para estoque insuficiente ou produto inativo. Por decisão de projeto, a reposição posterior do estoque não restaura a quantidade que o cliente havia escolhido, pois essa informação não é mantida após o ajuste.

Essas regras complementam o fluxo apresentado no Diagrama de Atividades I (Figura 9): a inclusão e a alteração de itens no carrinho passam a respeitar o estoque disponível, e a geração do pedido, ao baixar o estoque dos produtos vendidos, ajusta também os carrinhos de outros clientes que contenham esses produtos.

### 4.1.3 Tratamento de Concorrência na Baixa de Estoque {#tratamento-de-concorrência-na-baixa-de-estoque}

Em um sistema com vários usuários simultâneos, duas compras do mesmo produto podem ser processadas ao mesmo tempo. Cada uma pode ler o mesmo estoque antes que a outra o atualize e, assim, vender mais unidades do que as disponíveis. Esse fenômeno é conhecido como condição de corrida (*race condition*) [CITAÇÃO NECESSÁRIA]. Para evitá-lo, a finalização do pedido e a edição do estoque pelo produtor são executadas dentro de uma transação, isto é, um conjunto de operações tratado pelo banco de dados como uma unidade indivisível. Nessa transação, as linhas dos produtos envolvidos recebem um bloqueio pessimista, obtido pela instrução SQL `SELECT ... FOR UPDATE` [CITAÇÃO NECESSÁRIA]. Enquanto uma operação mantém o bloqueio, as demais que precisam do mesmo produto aguardam sua conclusão e então leem o estoque já atualizado, o que impede a venda acima do disponível. Na finalização, os produtos são bloqueados sempre na mesma ordem, o que reduz o risco de impasse (*deadlock*) entre transações concorrentes.

Esse bloqueio por linha é efetivo no PostgreSQL, banco de dados adotado para a versão final do sistema. Durante o desenvolvimento, utiliza-se o SQLite, sistema gerenciador de banco de dados que armazena todos os dados em um único arquivo e dispensa a instalação de um servidor. O SQLite não oferece bloqueio por linha. Nesse ambiente, a proteção decorre do próprio SQLite, que serializa as operações de escrita no banco de dados [CITAÇÃO NECESSÁRIA]. Por essa razão, o comportamento de referência para o controle de concorrência é o do PostgreSQL.

<!-- orientador: revisar -->
## 4.2 Pedidos e Ciclo de Status {#pedidos-e-ciclo-de-status}

Ao finalizar a compra, o cliente seleciona os itens do carrinho que deseja adquirir, e somente esses itens são convertidos em pedidos; os demais permanecem no carrinho. Os itens selecionados são agrupados pela loja responsável, e um pedido separado é gerado para cada loja envolvida, todos com o status inicial Pendente. Essa separação permite que cada produtor acompanhe apenas os pedidos destinados à sua loja, conforme apresentado no Diagrama de Atividades I (Figura 9). Não há pagamento online: o pedido representa uma solicitação de reserva para retirada presencial na feira. O dia e o horário da feira, todos os sábados das 6h às 12h, constituem uma configuração única da plataforma, válida para todas as lojas, e são apenas informados ao cliente; o sistema não impede a criação de pedidos fora desse período.

O ciclo de vida do pedido segue um fluxo rígido de status, apresentado na Figura 10. O produtor avança o pedido de Pendente para Em preparo, de Em preparo para Pronto para retirada e, por fim, para Entregue, quando o cliente retira os produtos na feira. Não é permitido retornar a um status anterior nem pular etapas. O cancelamento segue regras distintas para cada perfil: o cliente pode cancelar somente os próprios pedidos que ainda estejam com o status Pendente, enquanto o produtor pode cancelar os pedidos da sua loja com o status Pendente ou Em preparo. A partir do status Pronto para retirada, o pedido não pode mais ser cancelado. O cancelamento é imediato, não exige justificativa e mantém o pedido no histórico com o status Cancelado. Todas essas transições são validadas pela API, que recusa, com mensagem explicativa, qualquer alteração fora do fluxo; na interface, o quadro de pedidos do produtor exibe apenas as ações permitidas para o status atual de cada pedido.

Quando um pedido é cancelado, seja pelo cliente, seja pelo produtor, a quantidade de cada item é devolvida ao estoque do respectivo produto. Como Cancelado é um estado final, do qual o pedido não pode sair, a devolução ocorre uma única vez, o que impede que o mesmo pedido incremente o estoque repetidas vezes. Essa operação é executada dentro de uma transação, com o bloqueio das linhas dos produtos envolvidos, seguindo o mesmo mecanismo descrito na Seção 4.1.3. Para organizar a retirada, o produtor tem acesso somente ao nome do cliente registrado no pedido e, enquanto o pedido estiver em aberto, isto é, com o status Pendente, Em preparo ou Pronto para retirada, ao telefone principal atual do cliente; nos pedidos Entregue e Cancelado, o telefone não é exibido. Essa restrição limita a exposição dos demais dados pessoais registrados na compra, e a decisão de não preservar o telefone no pedido é justificada na Seção 4.7.

###### Figura 10 - Diagrama de Estados do Pedido

![](diagramas/fig10-estados-pedido.png){width="6.3in"}

**Fonte:** Confeccionado pelo autor (2026).

<!-- orientador: revisar -->
## 4.3 Imagens dos Produtos {#imagens-dos-produtos}

Cada produto pode reunir de zero a cinco imagens, armazenadas na entidade Imagem com sua ordem de exibição e um indicador de imagem principal. A principal representa o produto no catálogo, enquanto a página de detalhe apresenta uma galeria com todas as fotos, começando pela principal. Uma restrição no banco de dados garante que exista no máximo uma imagem principal por produto, e a API promove automaticamente a imagem seguinte, pela ordem de exibição, quando a principal é excluída, de modo que o catálogo nunca fique sem foto enquanto houver imagens cadastradas. A primeira imagem enviada torna-se a principal automaticamente, e a definição de outra imagem como principal desmarca a anterior. O fluxo de envio e de exclusão é apresentado na Figura 11.

Somente o produtor responsável pelo produto, ou o administrador, pode enviar, ordenar, definir a principal ou excluir imagens. No envio, o *backend* aceita apenas arquivos nos formatos JPG, PNG ou WEBP com até 5 MB, conferindo tanto a extensão quanto o conteúdo do arquivo, e armazena cada imagem com um nome gerado aleatoriamente, o que evita conflitos entre arquivos e não expõe o nome original enviado pelo usuário. Uma imagem já enviada não é substituída: para trocá-la, o produtor a exclui e envia outra, e o arquivo excluído é removido do armazenamento. O limite de cinco imagens é verificado com o produto bloqueado, para que envios simultâneos não o ultrapassem.

Para padronizar a apresentação dos produtos, cujos cartões no catálogo utilizam proporção quadrada, a interface oferece um editor opcional de enquadramento. Nele, o produtor posiciona a área de recorte e ajusta o zoom entre uma e três vezes; o recorte quadrado é então gerado no próprio navegador, por meio do elemento Canvas do HTML [CITAÇÃO NECESSÁRIA], que permite desenhar e exportar imagens por programação. O arquivo resultante é salvo no formato WEBP ou, quando o navegador não oferece esse formato, em JPEG, com lado máximo de 1200 pixels, o que também reduz o tamanho dos arquivos enviados. O recorte no navegador é apenas uma facilidade de uso: as validações de formato, tamanho e permissão permanecem no *backend*.

###### Figura 11 - Diagrama de Sequência VI - Imagens do Produto

![](diagramas/fig11-seq-imagens-produto.png){width="6.3in"}

**Fonte:** Confeccionado pelo autor (2026).

<!-- orientador: revisar -->
## 4.4 Área do Produtor e Perfil do Usuário {#área-do-produtor-e-perfil-do-usuário}

Todo usuário autenticado dispõe de uma página de perfil, na qual pode alterar nome, e-mail, data de nascimento e gênero, com as mesmas validações aplicadas no cadastro, além de gerenciar seus telefones de contato e sua foto de perfil, descritos adiante nesta seção. O CPF, por ser o identificador utilizado no acesso ao sistema, e o perfil de acesso não podem ser alterados pelo próprio usuário. A alteração do perfil não modifica os pedidos já realizados, que preservam os dados do cliente no momento da compra, conforme a Seção 4.7. Ao usuário que não possui perfil de produtor, a interface apresenta apenas a orientação para procurar a organização da feira, sem oferecer a criação de loja. Na página de pedidos, o cliente consulta o histórico de compras, que pode ser filtrado por status, cancela os pedidos pendentes e avalia os itens de pedidos entregues.

O produtor dispõe de uma área própria, organizada em quatro partes. O painel inicial apresenta indicadores de acompanhamento, como vendas do mês, pedidos no mês, ticket médio, vendas dos últimos sete dias e produtos mais vendidos, considerando apenas os pedidos não cancelados. Esses indicadores são calculados na interface, a partir dos pedidos da loja, e têm caráter exclusivamente informativo, não substituindo relatórios gerenciais. A segunda parte é um quadro de pedidos no estilo *kanban*, método de organização visual do trabalho em colunas que representam as etapas de um processo [CITAÇÃO NECESSÁRIA]; nele, cada coluna corresponde a um status, e cada pedido apresenta somente as ações permitidas pelo ciclo descrito na Seção 4.2. A terceira parte reúne os produtos da loja, com os indicadores de estoque descritos na Seção 4.1.1, e permite cadastrar e editar produtos, preços e imagens. Os produtos não são excluídos, pois a exclusão afetaria os itens de pedidos já realizados: o produtor pode desativá-los, após confirmação em uma janela de diálogo, e reativá-los a qualquer momento. A quarta parte, denominada Dados da loja, permite alterar o nome, a descrição e a imagem da loja e desativá-la. O CNPJ e o proprietário não podem ser alterados nessa área, e a desativação da loja preserva o histórico de pedidos e impede novas compras, sem impedir que o proprietário continue a editar o nome, a descrição e a imagem da loja inativa.

<!-- orientador: revisar -->
Na versão inicial do sistema, cada usuário possuía um único telefone, armazenado diretamente em seu cadastro e restrito ao formato de celular. Para permitir que o usuário informe mais de um contato e indique a natureza de cada número, essa estrutura foi substituída pelas entidades Telefone e Tipo_Telefone, descritas na Seção 3.2.3. Cada usuário, seja cliente ou produtor, pode cadastrar quantos telefones desejar, classificados como Celular, Fixo ou Comercial, e exatamente um deles é indicado como principal. No cadastro, o usuário informa um telefone e o seu tipo, que se torna o principal. Na página de perfil, somente o próprio usuário pode adicionar novos telefones, editar o número e o tipo dos existentes, excluí-los e definir qual é o principal; a definição de um novo telefone principal desmarca automaticamente o anterior. Para assegurar que o usuário mantenha sempre um meio de contato, a API recusa a exclusão do último telefone e a exclusão do telefone principal, exigindo, neste último caso, que outro telefone seja definido como principal antes da exclusão. Essas operações são executadas dentro de uma transação, com o bloqueio do registro do usuário, de modo que requisições simultâneas não resultem em um usuário sem telefone ou com mais de um telefone principal.

<!-- orientador: revisar -->
O número é validado no *backend* de acordo com o tipo, considerando somente os dígitos e incluindo o DDD: o celular deve possuir onze dígitos, o telefone fixo, dez, e o telefone comercial, dez ou onze, uma vez que pode corresponder tanto a uma linha fixa quanto a uma linha móvel. Quando o tipo de um telefone é alterado, o número é validado novamente segundo o novo tipo. O número é armazenado como texto, somente com dígitos, e não há restrição de unicidade, de modo que o mesmo número pode estar cadastrado para usuários diferentes. Os tipos de telefone são fixos, não podem ser cadastrados pelos usuários e são disponibilizados por uma consulta pública da API, necessária ao formulário de cadastro, que é preenchido sem autenticação. O administrador pode consultar e corrigir os telefones dos usuários pela área administrativa, sujeito às mesmas regras de no mínimo um telefone e de exatamente um telefone principal.

<!-- orientador: revisar -->
A introdução da nova estrutura exigiu a migração dos dados existentes, isto é, a transferência das informações já gravadas para as novas tabelas, realizada por meio do mecanismo de migrações do Django [CITAÇÃO NECESSÁRIA]. O telefone que cada usuário possuía foi copiado para a entidade Telefone como telefone principal, classificado como Celular quando possuía onze dígitos e como Fixo quando possuía dez. Os valores fora desse padrão foram registrados como Celular e podem ser listados por um comando administrativo, para correção posterior, e os valores vazios não geraram registros. Concluída a cópia, a coluna de telefone do cadastro do usuário foi removida. Por consequência, contas antigas que não possuíam telefone, assim como contas de superusuário criadas pela linha de comando do Django, podem permanecer sem nenhum telefone. Nessas contas, o primeiro telefone cadastrado torna-se automaticamente o principal, e a página de perfil exibe um aviso solicitando o cadastro enquanto não houver telefone; a ausência de telefone não impede o acesso ao sistema nem a realização de compras.

<!-- orientador: revisar -->
Complementarmente, o sistema permite que cada usuário possua uma foto de perfil e que cada loja possua uma imagem de apresentação, ambas opcionais e únicas. A foto de perfil é enviada, trocada ou removida pelo próprio usuário na página de perfil e é exibida somente a ele, nessa página e no menu da conta; ela não aparece em avaliações, em pedidos nem na área do produtor, o que limita a exposição de um dado pessoal. Quando o usuário não possui foto, a interface apresenta as iniciais do seu nome. A imagem da loja pode ser escolhida já no cadastro da loja, conforme descrito na Seção 3.2.5.2.3, ou enviada posteriormente na parte Dados da loja, e somente o proprietário pode enviá-la, trocá-la ou removê-la. Ela é exibida na parte Dados da loja, onde é gerenciada, e na página de detalhe do produto, junto ao nome da loja, apenas como identificação; os cartões do catálogo continuam a apresentar a imagem principal do produto. Quando a loja não possui imagem, a interface apresenta a inicial do nome da loja.

<!-- orientador: revisar -->
Ambas as imagens seguem as mesmas validações adotadas para as imagens dos produtos (Seção 4.3): o *backend* aceita apenas arquivos JPG, PNG ou WEBP com até 5 MB, conferindo tanto a extensão quanto o conteúdo do arquivo, e armazena cada um com um nome gerado aleatoriamente. Quando o envio é recusado, a imagem atual é mantida. Diferentemente das imagens dos produtos, o envio de uma nova imagem substitui a anterior, e a remoção pode ser feita sem o envio de outra, mediante confirmação em uma janela de diálogo. O arquivo substituído ou removido é excluído do armazenamento somente após a confirmação da transação no banco de dados, isto é, depois que a alteração foi efetivamente gravada, o que evita apagar um arquivo ainda referenciado caso a gravação falhe. Valores antigos de imagem da loja que não seguem o padrão de nome gerado pelo sistema são exibidos como ausência de imagem e não são apagados. A foto de perfil e a imagem da loja não fazem parte do *snapshot* do pedido (Seção 4.7), de modo que sua troca ou remoção não altera os pedidos já realizados. Os arquivos são armazenados no disco local durante o desenvolvimento e no Supabase Storage, serviço de armazenamento de arquivos em nuvem [CITAÇÃO NECESSÁRIA], no ambiente de produção.

<!-- autor: registrar aqui, se desejar, a validação manual no navegador da foto de perfil e da imagem da loja, após concluí-la -->

<!-- orientador: revisar -->
## 4.5 Favoritos {#favoritos}

A funcionalidade de favoritos permite que qualquer usuário autenticado, seja cliente ou produtor, marque produtos de interesse para consultá-los posteriormente. Os favoritos são persistidos no servidor e vinculados ao usuário autenticado, o que os mantém disponíveis em diferentes dispositivos e sessões. A lista de favoritos é privada, acessível apenas pelo próprio usuário, e apresenta primeiro os produtos favoritados mais recentemente. Um mesmo produto não pode ser favoritado mais de uma vez pelo mesmo usuário, regra garantida tanto pela validação da API quanto por uma restrição de unicidade no banco de dados. Os produtos que se tornam inativos, que ficam sem estoque ou cuja loja é desativada permanecem na lista de favoritos para consulta, mas não podem ser adicionados ao carrinho enquanto estiverem indisponíveis.

<!-- orientador: revisar -->
## 4.6 Avaliações de Produtos {#avaliações-de-produtos}

As avaliações permitem que os compradores registrem sua opinião sobre os produtos adquiridos, contribuindo para a escolha de outros consumidores. Para garantir que somente produtos efetivamente comprados sejam avaliados, a avaliação é feita sobre um item de pedido, e não diretamente sobre o produto. Somente o usuário autenticado que realizou o pedido pode avaliar seus itens, e somente quando o pedido estiver com o status Entregue. Cada item de pedido pode ser avaliado uma única vez, regra reforçada por uma restrição de unicidade no banco de dados; caso o mesmo produto tenha sido comprado em pedidos diferentes, cada item entregue pode receber sua própria avaliação. A avaliação possui uma nota inteira de um a cinco e um comentário opcional de até quinhentos caracteres. O produto avaliado e o autor da avaliação são definidos pelo *backend* a partir do item e do usuário autenticado, e não a partir de dados enviados pela interface. O fluxo é apresentado na Figura 12.

Na interface, a página de pedidos exibe o botão "Avaliar" nos itens de pedidos entregues que ainda não foram avaliados. O botão abre uma janela de diálogo para o registro da nota e do comentário, desenvolvida com atenção a recursos de acessibilidade, e, após o envio, o item passa a exibir a indicação "Avaliado". As avaliações são públicas: qualquer visitante pode consultá-las na página de detalhe do produto, junto com a média das notas, calculada apenas para exibição. Para preservar a privacidade do avaliador, a API retorna somente o primeiro nome e a inicial do sobrenome, sem expor o nome completo.

Depois de enviada, a avaliação não pode ser editada nem removida pelo autor. A remoção é reservada ao administrador, como forma de moderação, por meio da área administrativa, na qual as avaliações podem ser consultadas e excluídas, mas não criadas nem editadas. Após a remoção de uma avaliação pelo administrador, o item de pedido correspondente pode ser avaliado novamente.

###### Figura 12 - Diagrama de Sequência VII - Avaliação de Item Entregue

![](diagramas/fig12-seq-avaliacao.png){width="6.3in"}

**Fonte:** Confeccionado pelo autor (2026).

<!-- orientador: revisar -->
## 4.7 Preservação do Histórico de Pedidos {#preservação-do-histórico-de-pedidos}

O histórico de pedidos constitui um registro das transações realizadas entre clientes e produtores e, por isso, deve permanecer consistente mesmo que os cadastros sejam alterados ao longo do tempo. Para isso, o sistema adota o registro de uma cópia dos dados no momento da compra, denominada *snapshot*. Os dados do cliente são preservados na entidade Pedido_Cliente, e os dados dos itens, como o nome do produto, a quantidade, o valor unitário, o desconto e o subtotal, são preservados na entidade Pedido_Produto. Assim, alterações posteriores no perfil do cliente ou no cadastro e no preço dos produtos não modificam os pedidos já realizados.

<!-- orientador: revisar -->
Por decisão de projeto, o telefone constitui uma exceção a esse princípio e não integra o *snapshot* do cliente. Diferentemente do nome, do CPF, do e-mail, da data de nascimento e do gênero, que continuam preservados em Pedido_Cliente, o telefone tem no sistema uma finalidade exclusivamente operacional: permitir que o produtor entre em contato com o cliente para organizar a retirada dos produtos na feira. Para essa finalidade, somente o número atual é útil, pois um número registrado no momento da compra e posteriormente substituído pelo cliente não permitiria o contato. Por essa razão, nos pedidos em aberto, com o status Pendente, Em preparo ou Pronto para retirada, o produtor visualiza o telefone principal atual do cliente, consultado em seu cadastro no momento da exibição, de modo que a troca do telefone principal no perfil altera o contato apresentado nesses pedidos; o telefone permanece visível nesses pedidos mesmo que a conta do cliente tenha sido desativada. Nos pedidos Entregue e Cancelado, nos quais a retirada já foi concluída ou não ocorrerá mais, o telefone não é exibido. Nas contas sem telefone cadastrado, descritas na Seção 4.4, o produtor não visualiza nenhum telefone.

<!-- orientador: revisar -->
Essa decisão também se relaciona à proteção de dados pessoais. A Lei Geral de Proteção de Dados Pessoais (LGPD) [CITAÇÃO NECESSÁRIA] estabelece, entre seus princípios, o da necessidade, que orienta a limitação do tratamento de dados pessoais ao mínimo necessário para a realização de suas finalidades, prática também referida como minimização de dados [CITAÇÃO NECESSÁRIA]. Ao não copiar o telefone em cada pedido e ao deixar de exibi-lo quando o contato para a retirada não é mais necessário, o sistema reduz a quantidade de cópias desse dado e o período em que ele fica exposto ao produtor, sem prejuízo para o histórico comercial, que permanece íntegro quanto aos produtos, aos valores e à identificação do comprador. Em contrapartida, o pedido deixa de registrar o telefone utilizado no momento da compra, limitação discutida no Capítulo 5.

Conforme descrito nas Seções 3.2.3 e 3.2.4, o vínculo entre o pedido e o cliente que o realizou é registrado na própria entidade Pedido_Cliente, e não diretamente na entidade Pedido. Essa organização concentra em um único lugar a identificação do comprador e os dados utilizados na compra, evitando que a mesma informação seja mantida em duas entidades.

Complementarmente, o sistema impede a exclusão de registros dos quais o histórico depende. Um usuário que possua pedidos e um produtor cuja loja tenha recebido pedidos não podem ser excluídos: a tentativa de exclusão pela área administrativa é recusada, e são exibidos os pedidos que a impedem. A loja não possui operação própria de exclusão, nem na área administrativa nem na API, e a API também não oferece a exclusão de usuários. Para encerrar o acesso de um usuário, o administrador o desativa, mantendo a conta; para encerrar a atividade de uma loja, utiliza-se a desativação, descrita na Seção 4.4. Os pedidos, por sua vez, ficam disponíveis na área administrativa apenas para consulta, sem a possibilidade de inclusão, edição ou exclusão, e a alteração de status ocorre exclusivamente pela API, respeitando o fluxo descrito na Seção 4.2.

<!-- orientador: revisar -->
No caso dos produtores, a proteção é mais ampla: enquanto possuir loja, o produtor não pode ser excluído, tenha ou não pedidos associados, pois a referência da loja ao seu proprietário utiliza a regra de exclusão restritiva descrita na Seção 3.2.4. Dessa forma, a loja e os seus produtos nunca são removidos em cascata junto com o usuário. O encerramento da atividade do produtor ocorre por meio de exclusão lógica, isto é, pela marcação do registro como inativo em vez de sua remoção física do banco de dados: a loja é desativada e, quando necessário, o administrador inativa o usuário, preservando o histórico de pedidos, a loja e os produtos.

<!-- orientador: revisar -->
## 4.8 Redefinição de Senha {#redefinição-de-senha}

Como o acesso ao sistema depende de CPF e senha, um usuário que esquece a senha ficaria impedido de utilizar a plataforma sem um meio de recuperá-la. Para atender a essa necessidade, foi implementado um fluxo de redefinição de senha baseado no envio de um *link*, isto é, de um endereço de acesso, para o e-mail cadastrado na conta. Na tela de login, a opção "Esqueci minha senha" conduz a uma tela na qual o usuário informa esse e-mail. A API responde sempre com a mesma mensagem, "Se houver uma conta com este e-mail, enviaremos um link para redefinir a senha.", exista ou não uma conta associada ao endereço informado. Essa resposta neutra impede que a funcionalidade seja utilizada para descobrir quais e-mails estão cadastrados na plataforma, prática conhecida como enumeração de contas [CITAÇÃO NECESSÁRIA]. O e-mail é comparado sem diferenciar letras maiúsculas e minúsculas, e contas inativas não recebem o *link*, embora a resposta permaneça a mesma. O fluxo completo é apresentado na Figura 13.

Quando existe uma conta ativa com o e-mail informado, o *backend* gera um código aleatório e registra, na tabela redefinicao_senha, somente o *hash* desse código, conforme descrito na Seção 3.2.4, junto com a data de expiração. O código em si é enviado apenas no *link* do e-mail. Cada *link* vale por trinta minutos e pode ser utilizado uma única vez, condição registrada pelo preenchimento da data de utilização. Ao solicitar um novo *link*, os anteriores que ainda não foram utilizados são invalidados, de modo que apenas o mais recente permanece válido. No *link*, o código é posicionado no fragmento do endereço, a parte que sucede o caractere "#" e que o navegador não envia ao servidor nas requisições [CITAÇÃO NECESSÁRIA]. Ao abrir a tela de redefinição, a interface lê o código e o remove imediatamente da barra de endereços e do histórico de navegação, mantendo-o apenas na memória da própria tela, o que reduz o risco de exposição do código em registros de acesso, no histórico do navegador ou no compartilhamento acidental do endereço.

Na tela de redefinição, o usuário informa a nova senha e sua confirmação. A nova senha é submetida às mesmas validações aplicadas no cadastro: deve possuir no mínimo oito caracteres, atender aos critérios de segurança de senha do *backend* e coincidir com a confirmação. Um *link* expirado, já utilizado, invalidado ou inexistente é recusado com a mensagem "Este link de redefinição é inválido ou expirou. Solicite um novo.", e a interface oferece a opção de solicitar um novo *link*; a mesma mensagem é apresentada quando a conta foi desativada, para não revelar o estado da conta. A marcação do *link* como utilizado e a gravação da nova senha ocorrem em uma única transação, e a marcação só é efetivada se o *link* ainda estiver pendente e dentro do prazo, o que impede que duas tentativas simultâneas utilizem o mesmo *link*. Concluída a troca, os demais *links* pendentes do usuário também são invalidados. O usuário não é autenticado automaticamente: a interface encerra a sessão local que eventualmente exista no navegador, apresenta a mensagem "Senha redefinida. Entre com a nova senha." e o encaminha à tela de login, exigindo que a nova senha seja efetivamente informada para o acesso.

Os dois serviços da API envolvidos no fluxo, o de solicitação e o de confirmação, são públicos, pois são utilizados por quem não consegue se autenticar. Para limitar o uso abusivo, como o envio massivo de e-mails ou tentativas sucessivas de adivinhar códigos, o *backend* restringe a quantidade de requisições por endereço IP (*Internet Protocol*) de origem: até cinco solicitações de *link* e até dez tentativas de confirmação por hora. Ao exceder esses limites, a API recusa a requisição com a mensagem "Muitas solicitações. Tente novamente mais tarde.".

O envio do e-mail utiliza o recurso nativo do Django. Em ambiente de desenvolvimento, a mensagem é apenas exibida no console do servidor, enquanto, em produção, é enviada por um servidor SMTP (*Simple Mail Transfer Protocol*), protocolo padrão de envio de mensagens eletrônicas [CITAÇÃO NECESSÁRIA], configurado por variáveis de ambiente, de modo que as credenciais de acesso não ficam registradas no código-fonte. O e-mail é enviado somente após a gravação da solicitação no banco de dados e, em caso de falha no envio, o erro é registrado no servidor, sem alteração da resposta neutra apresentada ao usuário. Cabe destacar que esse e-mail constitui uma mensagem transacional, isto é, uma resposta direta a uma ação iniciada pelo próprio usuário e necessária para concluí-la. Ele não se confunde com as notificações ativas tratadas no Capítulo 5, como os avisos de mudança de status dos pedidos ou de estoque baixo, que seriam enviadas por iniciativa do sistema e permanecem como trabalho futuro.

As regras desse fluxo, como a resposta neutra, a validade e o uso único dos *links*, a invalidação dos *links* anteriores, as validações da nova senha e os limites de requisições, foram verificadas por testes automatizados do *backend*, nos mesmos moldes descritos na Seção 4.9.

<!-- orientador: revisar -->
Além dos testes automatizados, o fluxo foi validado manualmente em ambiente real em 16 de outubro de 2026. Nessa validação, o *backend* foi executado com o banco de dados PostgreSQL hospedado no Supabase e com envio efetivo de e-mails por meio do servidor SMTP do Gmail, na porta 587 e com criptografia TLS (*Transport Layer Security*), protocolo que protege a comunicação entre a aplicação e o servidor de e-mail [CITAÇÃO NECESSÁRIA], configurado por variáveis de ambiente; o *frontend* foi executado localmente. A solicitação de redefinição obteve a resposta neutra prevista, com código HTTP (*Hypertext Transfer Protocol*) 200, que indica sucesso no processamento da requisição, e gerou um registro de redefinição com expiração exatamente trinta minutos após sua criação e data de utilização ainda não preenchida. Verificou-se também que a nova solicitação invalidou uma solicitação anterior da mesma conta, conforme a regra descrita nesta seção. O e-mail foi recebido na caixa de entrada do destinatário e, a partir do *link* recebido, a nova senha foi cadastrada com sucesso pela tela de redefinição. A recusa de um *link* já utilizado e o acesso com a nova senha não foram repetidos manualmente nessa validação, permanecendo verificados pelos testes automatizados do *backend*.

<!-- autor: registrar aqui, se desejar, a validação manual das telas "Esqueci minha senha" e "Crie uma nova senha" no navegador, após concluí-la -->

###### Figura 13 - Diagrama de Sequência VIII - Redefinição de Senha

![](diagramas/fig13-seq-redefinicao-senha.png){width="6.3in"}

**Fonte:** Confeccionado pelo autor (2026).

<!-- orientador: revisar -->
## 4.9 Verificação das Funcionalidades {#verificação-das-funcionalidades}

As regras de negócio descritas neste capítulo foram verificadas por meio de testes automatizados do *backend*, que simulam as requisições à API e conferem as respostas e os dados gravados no banco de dados. Na data de redação desta seção, 18 de outubro de 2026, a suíte completa de testes do *backend* reunia 370 testes automatizados, todos executados com sucesso no banco de dados SQLite. Entre eles, estão os testes que verificam a retirada do produto sem estoque do catálogo, os limites do indicador de estoque baixo, a recusa de estoque negativo, o ajuste dos carrinhos, as transições de status e a devolução do estoque no cancelamento, o vínculo do cliente com os pedidos, o bloqueio da exclusão de usuários com pedidos, a recusa de uma segunda loja para o mesmo produtor, tanto pela API quanto pela restrição de unicidade do banco de dados, inclusive em uma situação que simula requisições simultâneas, o bloqueio da exclusão de produtor que possui loja, com ou sem pedidos, preservando a loja e o histórico, as regras de avaliação, a redefinição de senha, o envio, a troca e a remoção da imagem da loja e da foto de perfil e os telefones do usuário, incluindo a validação do número conforme o tipo, a existência de um único telefone principal, a recusa da exclusão do último telefone e do telefone principal, a exibição do telefone ao produtor somente nos pedidos em aberto e a migração dos telefones existentes para a nova estrutura. Complementarmente, as telas relacionadas ao controle de estoque foram inspecionadas visualmente nas larguras de 375 e 1280 pixels, representativas de *smartphones* e de computadores de mesa, respectivamente, em atenção ao requisito não funcional de responsividade da interface.
<!-- autor: registrar aqui a validação manual da tela de avaliações no navegador, se desejar; não há testes de usabilidade com usuários a relatar -->

# [5 LIMITAÇÕES E TRABALHOS FUTUROS]{.smallcaps} {#limitações-e-trabalhos-futuros}

<!-- orientador: revisar -->
Este capítulo reúne as limitações identificadas nas funcionalidades implementadas e as evoluções que podem ser exploradas em trabalhos futuros.

<!-- orientador: revisar -->
## 5.1 Limitações das Funcionalidades Implementadas {#limitações-das-funcionalidades-implementadas}

O controle de estoque implementado atende às necessidades do MVP, mas apresenta limitações que podem orientar trabalhos futuros, no âmbito de um controle de estoque mais avançado. A sinalização de estoque baixo é apenas visual e depende do acesso do produtor à plataforma. Uma evolução possível é a notificação ativa, por e-mail ou por notificação *push*. O limite de cinco unidades é único para todos os produtos e poderia passar a ser configurável por produto, considerando as diferentes unidades de venda e o giro de cada item. Quando a quantidade de um item do carrinho é reduzida sem chegar a zero, o cliente não recebe um aviso específico. Esse aviso exigiria armazenar a quantidade escolhida originalmente. Por fim, a proibição de estoque negativo é hoje garantida apenas pela validação da API. A restrição equivalente no banco de dados, que reforçaria a integridade independentemente da aplicação, está planejada e ainda não foi implementada.

<!-- orientador: revisar -->
No ciclo de pedidos, o cancelamento não registra uma justificativa, e o cliente não é notificado ativamente quando o produtor altera o status ou cancela um pedido; a informação fica disponível apenas na página de pedidos. Além disso, o dia e o horário da feira são apenas informativos, e o sistema não restringe a criação de pedidos com base nesse período.

<!-- orientador: revisar -->
Nas avaliações, não há edição pelo autor: uma avaliação enviada só pode ser removida pelo administrador, como moderação. Além disso, embora as avaliações de produtos desativados ou de lojas desativadas continuem disponíveis na API, elas não são exibidas na interface, pois a página de detalhe desses produtos deixa de ficar acessível.

<!-- orientador: revisar -->
Quanto aos dados pessoais, a preservação do histórico impede a exclusão de usuários que possuam pedidos, e o *snapshot* mantém dados como nome, CPF, e-mail, data de nascimento e gênero registrados em cada pedido. O telefone, por decisão de projeto descrita na Seção 4.7, não é copiado para o pedido e é exibido ao produtor apenas nos pedidos em aberto, o que reduz a exposição desse dado, mas não resolve a questão para os demais dados preservados. O sistema ainda não dispõe de um procedimento de anonimização desses dados, que seria necessário para atender a solicitações de eliminação de dados pessoais previstas na LGPD [CITAÇÃO NECESSÁRIA] sem comprometer a integridade do histórico de vendas.

<!-- orientador: revisar -->
Quanto aos telefones, descritos na Seção 4.4, a validação considera apenas a quantidade de dígitos de acordo com o tipo, sem verificar se o DDD corresponde a um código de área existente nem se o número de celular inicia pelo nono dígito, de modo que números com formato válido, mas inexistentes, são aceitos. A exigência de ao menos um telefone por usuário é garantida pela API e pela área administrativa, e não por uma restrição do banco de dados, o que admite as contas sem telefone mencionadas na Seção 4.4; nos pedidos dessas contas, o produtor não dispõe de um telefone para contato. Como o telefone não integra o *snapshot*, o pedido não registra o número utilizado no momento da compra, e os telefones migrados com formato fora do padrão dependem de correção manual. Por fim, o telefone do produtor não é exibido ao cliente, e a forma de contato com a loja ainda não foi definida.

<!-- orientador: revisar -->
Na redefinição de senha, descrita na Seção 4.8, as sessões já abertas antes da troca não são encerradas: os tokens JWT emitidos anteriormente continuam válidos até expirarem pelo prazo normal, de até cento e vinte minutos para o token de acesso e de um dia para o token de renovação. Assim, se a senha tiver sido redefinida por suspeita de acesso indevido, uma sessão já aberta por terceiros não é interrompida de imediato. Além disso, o usuário não recebe um aviso por e-mail informando que a senha foi alterada, o envio do e-mail de redefinição ocorre durante o próprio processamento da solicitação, o que pode aumentar o tempo de resposta quando o servidor de e-mail estiver lento, e os registros de solicitações expiradas ou já utilizadas não são removidos periodicamente.

<!-- orientador: revisar -->
Quanto às imagens descritas na Seção 4.4, a página pública da loja ainda não foi construída; quando existir, a imagem da loja também será exibida nela, e o nome da loja na página de detalhe do produto passará a conduzir a essa página. Além disso, a versão atual apresenta três limitações. Primeiro, embora a foto de perfil seja exibida apenas ao próprio usuário na interface, o arquivo fica acessível a quem conhecer o seu endereço; o nome gerado aleatoriamente torna esse endereço difícil de descobrir, mas não constitui um controle de acesso. Segundo, como o arquivo é gravado no armazenamento antes da confirmação da transação no banco de dados, uma falha nessa gravação pode deixar um arquivo sem referência no armazenamento, denominado arquivo órfão, que ocupa espaço sem ser utilizado; situação semelhante ocorre quando a remoção do arquivo anterior falha, caso em que o erro é apenas registrado no servidor. Terceiro, a troca dessas imagens pela área administrativa não aplica as mesmas validações de formato e de tamanho adotadas no envio pelo usuário.

<!-- orientador: revisar -->
Por fim, o desenvolvimento e os testes automatizados foram realizados com o banco de dados SQLite. Das alterações da estrutura do banco de dados, somente a transferência do vínculo do cliente para a entidade Pedido_Cliente, descrita na Seção 4.7, e a restrição de uma loja por produtor, descrita na Seção 3.2.4, já foram aplicadas ao banco de dados PostgreSQL do ambiente de produção. As demais alterações estruturais, como a nova organização dos telefones do usuário, descrita na Seção 4.4, e a preservação dos itens de pedido e das avaliações em caso de exclusão do produto, encontram-se implementadas e verificadas pelos testes automatizados, mas sua aplicação ao banco de dados PostgreSQL de produção permanece pendente. Além disso, o comportamento do bloqueio por linha descrito na Seção 4.1.3 ainda precisa ser verificado nesse banco de dados.

<!-- orientador: revisar -->
## 5.2 Trabalhos Futuros {#trabalhos-futuros}

A partir das limitações identificadas e do escopo definido para o MVP, as seguintes evoluções podem ser exploradas em trabalhos futuros:

- Fluxo de habilitação de produtores, no qual o usuário solicitaria o perfil de produtor e a criação de sua loja, e o administrador aprovaria a solicitação. No MVP, o perfil de produtor é atribuído diretamente pela administração da plataforma;

- Agrupamento, em uma única compra, dos pedidos gerados para diferentes lojas em uma mesma finalização, permitindo ao cliente consultar a compra como um todo;

<!-- orientador: revisar -->
- Página pública da loja, com a apresentação da loja, de sua imagem e de seus produtos, acessível também a partir do nome da loja na página de detalhe do produto;

<!-- orientador: revisar -->
- Moderação, pelo administrador, das imagens das lojas e das fotos de perfil, com as mesmas validações aplicadas ao envio pelo usuário, e separação da imagem da loja em logotipo e imagem de capa;

- Edição das avaliações pelo autor e exibição das avaliações de produtos desativados;

- Procedimento de anonimização de dados pessoais, em conformidade com a LGPD;

<!-- orientador: revisar -->
- Validação mais rigorosa dos telefones, com a verificação do DDD e do nono dígito dos números de celular;

<!-- orientador: revisar -->
- Definição dos dados de contato e da cidade da loja, permitindo ao cliente contatar o produtor, uma vez que, no MVP, o telefone do produtor não é exibido ao cliente;

<!-- orientador: revisar -->
- Evoluções da segurança da conta: envio assíncrono do e-mail de redefinição de senha, isto é, realizado em segundo plano, sem que a resposta ao usuário dependa da conclusão do envio; encerramento imediato das sessões JWT abertas após a troca de senha; envio de um e-mail de aviso informando que a senha foi alterada; troca de senha pela página de perfil, mediante a informação da senha atual; e remoção periódica dos registros de redefinição expirados ou já utilizados;

- Verificação do controle de concorrência no PostgreSQL do ambiente de produção;

- Pagamento online e integração com meios de pagamento;

- Entrega em domicílio, como alternativa à retirada na feira;

- Notificações ativas, por e-mail ou notificação *push*, para mudanças de status dos pedidos e para o estoque baixo;

- Controle avançado de estoque, com limite de estoque baixo configurável por produto e restrição de estoque não negativo no banco de dados;

- Aplicativo para dispositivos móveis, relatórios avançados de vendas e comunicação direta entre cliente e produtor por meio de *chat*.

# [6 CRONOGRAMA]{.smallcaps} {#cronograma}

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
