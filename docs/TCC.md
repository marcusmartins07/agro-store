INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA SUL-RIO-GRANDENSE

CAMPUS CAMAQUÃ

TECNÓLOGO EM ANÁLISE E DESENVOLVIMENTO DE SISTEMAS

Marcus Vinícius da Silva Martins

<!-- orientador: revisar -->
**AGRO STORE: plataforma digital de comercialização B2C para produtores rurais**

Camaquã, RS

2026

Marcus Vinícius da Silva Martins

<!-- orientador: revisar -->
**AGRO STORE: plataforma digital de comercialização B2C para produtores rurais**

<!-- orientador: revisar -->
> Trabalho de Conclusão de Curso apresentado como requisito parcial à obtenção do título de Tecnólogo em Análise e Desenvolvimento de Sistemas, do Instituto Federal Sul-rio-grandense – Câmpus Camaquã.
>
> Orientador(a): Prof. Marcelo Gonçalves de Souza

Camaquã

2026

Marcus Vinícius da Silva Martins

<!-- orientador: revisar -->
**AGRO STORE: plataforma digital de comercialização B2C para produtores rurais**

> Trabalho de Conclusão de Curso apresentado como requisito parcial à obtenção do título de Tecnólogo em Análise e Desenvolvimento de Sistemas, do Instituto Federal Sul-rio-grandense – Câmpus Camaquã.
>
> Orientador(a): Prof. Marcelo Gonçalves de Souza

**Banca Examinadora**

Prof. Marcelo Gonçalves de Souza

Orientador

Instituto Federal Sul-rio-grandense – Câmpus Camaquã

Prof. Diego Pereira

Avaliador

Instituto Federal Sul-rio-grandense – Câmpus Camaquã

Prof. Geraldo Barbosa

Avaliador

Instituto Federal Sul-rio-grandense – Câmpus Camaquã

**RESUMO**

<!-- orientador: revisar -->
Este trabalho apresenta o desenvolvimento do Agro Store, uma plataforma web de comercialização voltada aos produtores rurais participantes da Feira do Produtor Rural Willi Dummer, no município de Camaquã/RS. A proposta surgiu da observação da dinâmica presencial da feira, realizada apenas nas manhãs de sábado, o que limita o alcance comercial dos produtores e dificulta a organização antecipada dos pedidos. A pesquisa caracterizou-se como aplicada, de natureza qualitativa e com abordagem de desenvolvimento de software, e foi conduzida nas etapas de levantamento de requisitos, modelagem, implementação e verificação. A modelagem contemplou o Diagrama Entidade-Relacionamento, o modelo lógico do banco de dados e diagramas UML dos principais fluxos da aplicação. O sistema foi construído com arquitetura desacoplada, composta por uma API REST desenvolvida em Python com Django e Django REST Framework, com autenticação por tokens JWT, e por uma interface web desenvolvida em Vue.js, mantidas em um único repositório. Utilizou-se o SQLite durante o desenvolvimento e o PostgreSQL, hospedado no Supabase, no ambiente de produção. Como resultado, foi entregue um Produto Mínimo Viável que atende a vinte e quatro requisitos funcionais, entre eles o cadastro de clientes, o catálogo público de produtos, o carrinho persistido no servidor, a geração de um pedido separado para cada loja, o acompanhamento do ciclo de status do pedido até a retirada presencial na feira, a gestão de lojas, produtos, preços e imagens pelos produtores, os favoritos e as avaliações de itens entregues. As regras de negócio críticas, como o controle de estoque com tratamento de concorrência e a preservação do histórico de pedidos, foram validadas no servidor e verificadas por 399 testes automatizados do backend. Pagamento online, entrega em domicílio e notificações ativas permaneceram fora do escopo e foram indicados como trabalhos futuros.

**Palavras-chave:** Agro Store; agricultura familiar; produtores rurais; desenvolvimento web; comercialização digital.

**ABSTRACT**

<!-- orientador: revisar -->
This work presents the development of Agro Store, a web commercialization platform aimed at rural producers participating in the Willi Dummer Rural Producer Fair, in the municipality of Camaquã/RS. The proposal arose from the observation of the fair's in-person dynamics, held only on Saturday mornings, which limits the producers' commercial reach and makes it difficult to organize orders in advance. The research was characterized as applied, qualitative in nature, and based on a software development approach, and it was conducted through the stages of requirements gathering, modeling, implementation, and verification. The modeling included the Entity-Relationship Diagram, the logical database model, and UML diagrams of the main application flows. The system was built with a decoupled architecture, composed of a REST API developed in Python with Django and Django REST Framework, with JWT token-based authentication, and a web interface developed in Vue.js, both kept in a single repository. SQLite was used during development and PostgreSQL, hosted on Supabase, in the production environment. As a result, a Minimum Viable Product was delivered that meets twenty-four functional requirements, including customer registration, a public product catalog, a server-side shopping cart, the creation of a separate order for each store, the tracking of the order status cycle up to in-person pickup at the fair, the management of stores, products, prices, and images by producers, favorites, and reviews of delivered items. Critical business rules, such as stock control with concurrency handling and the preservation of order history, were validated on the server and verified by 399 automated backend tests. Online payment, home delivery, and active notifications remained out of scope and were indicated as future work.

**Keywords:** Agro Store; family farming; rural producers; web development; digital commercialization.

**LISTA DE FIGURAS**

<!-- autor: atualizar a numeração de páginas das listas e do sumário após aplicar o texto no Google Doc -->

<!-- orientador: revisar -->
Figura 1 - Modelo Conceitual do Diagrama Entidade-Relacionamento

Figura 2 - Modelo Lógico do Diagrama Entidade-Relacionamento

Figura 3 - Diagrama de Casos de Uso

Figura 4 - Diagrama de Sequência I - Cadastro de Cliente

Figura 5 - Diagrama de Sequência II - Acesso ao Sistema

Figura 6 - Diagrama de Sequência III - Cadastro de Loja pelo Produtor

Figura 7 - Diagrama de Sequência IV - Cadastro de Produto e Definição de Preço

Figura 8 - Diagrama de Sequência V - Consulta do Catálogo de Produtos

Figura 9 - Diagrama de Atividades I - Geração de Pedido pelo Cliente

Figura 10 - Ciclo de uma Requisição na API

Figura 11 - Diagrama de Estados do Pedido

Figura 12 - Diagrama de Sequência VI - Imagens do Produto

Figura 13 - Diagrama de Sequência VII - Avaliação de Item Entregue

Figura 14 - Diagrama de Sequência VIII - Redefinição de Senha

Figura 15 - Tela de login

Figura 16 - Tela de cadastro de cliente

Figura 17 - Tela de solicitação de redefinição de senha

Figura 18 - Tela de cadastro da nova senha

Figura 19 - Catálogo de produtos

Figura 20 - Detalhe do produto

Figura 21 - Avaliações no detalhe do produto

Figura 22 - Carrinho

Figura 23 - Favoritos

Figura 24 - Meus pedidos

Figura 25 - Janela de confirmação de recebimento

Figura 26 - Janela de avaliação de produto

Figura 27 - Perfil do usuário

Figura 28 - Telefones do perfil

Figura 29 - Cadastro da loja

Figura 30 - Painel do produtor

Figura 31 - Quadro de pedidos do produtor

Figura 32 - Produtos da loja

Figura 33 - Formulário de cadastro de produto

Figura 34 - Editor de enquadramento da imagem

Figura 35 - Dados da loja

**LISTA DE QUADROS**

<!-- orientador: revisar -->
Quadro 1 - Requisitos funcionais

Quadro 2 - Requisitos não funcionais

Quadro 3 - Códigos de status HTTP retornados pela API

Quadro 4 - Endpoints de autenticação e perfil do usuário

Quadro 5 - Endpoints de telefones do usuário

Quadro 6 - Endpoints de lojas

Quadro 7 - Endpoints de produtos e categorias

Quadro 8 - Endpoints de preços e imagens dos produtos

Quadro 9 - Endpoints do carrinho

Quadro 10 - Endpoints de pedidos

Quadro 11 - Endpoints de favoritos e avaliações

Quadro 12 - Configuração dos ambientes de desenvolvimento e produção

Quadro 13 - Testes automatizados do backend por área

Quadro 14 - Conformidade dos requisitos funcionais

Quadro 15 - Conformidade dos requisitos não funcionais

Quadro 16 - Cronograma de atividades

**LISTA DE ABREVIATURAS E SIGLAS**

<!-- orientador: revisar -->
API Application Programming Interface

B2B Business to Business

B2C Business to Consumer

C2C Consumer to Consumer

CNPJ Cadastro Nacional da Pessoa Jurídica

CORS Cross-Origin Resource Sharing

CPF Cadastro de Pessoas Físicas

DDD Discagem Direta a Distância

DER Diagrama Entidade-Relacionamento

DOM Document Object Model

DRF Django REST Framework

HTML HyperText Markup Language

HTTP Hypertext Transfer Protocol

IBGE Instituto Brasileiro de Geografia e Estatística

IP Internet Protocol

JPEG Joint Photographic Experts Group

JSON JavaScript Object Notation

JWT JSON Web Token

LGPD Lei Geral de Proteção de Dados Pessoais

MTV Model-Template-View

MVC Model-View-Controller

MVP Minimum Viable Product (Produto Mínimo Viável)

ORM Object-Relational Mapping

OWASP Open Worldwide Application Security Project

PBKDF2 Password-Based Key Derivation Function 2

PNG Portable Network Graphics

REST Representational State Transfer

RFC Request for Comments

SHA Secure Hash Algorithm

SKU Stock Keeping Unit

SMTP Simple Mail Transfer Protocol

SPA Single Page Application

SQL Structured Query Language

TLS Transport Layer Security

UML Unified Modeling Language

URL Uniform Resource Locator

**SUMÁRIO**

<!-- orientador: revisar -->
1 INTRODUÇÃO

1.1 Objetivos

1.1.1 Objetivo Geral

1.1.2 Objetivos Específicos

1.2 Justificativa

1.3 Organização do Trabalho

2 FUNDAMENTAÇÃO TEÓRICA

2.1 Agricultura Familiar e Feiras de Produtores Rurais

2.2 Plataformas Digitais de Comercialização

2.3 Modelo B2C

2.4 Ferramentas e Tecnologias Utilizadas

2.4.1 Aplicação Web

2.4.2 API e REST

2.4.3 Python

2.4.4 Django e Django REST Framework

2.4.5 Vue.js

2.4.6 PostgreSQL

2.4.7 MVC e MTV

2.4.8 JSON

2.4.9 JWT

3 METODOLOGIA

3.1 Requisitos

3.1.1 Requisitos Funcionais

3.1.2 Requisitos Não Funcionais

3.2 Modelagem

3.2.1 Confecção de Diagramas

3.2.2 Modelagem do Banco de Dados

3.2.3 Diagrama Entidade-Relacionamento (DER)

3.2.4 Modelo Lógico

3.2.5 Diagramas UML

3.2.5.1 Diagrama de Casos de Uso

3.2.5.2 Diagramas de Sequência

3.2.5.2.1 Diagrama de Sequência I - Cadastro de Cliente

3.2.5.2.2 Diagrama de Sequência II - Acesso ao Sistema

3.2.5.2.3 Diagrama de Sequência III - Cadastro de Loja pelo Produtor

3.2.5.2.4 Diagrama de Sequência IV - Cadastro de Produto e Definição de Preço

3.2.5.2.5 Diagrama de Sequência V - Consulta do Catálogo de Produtos

3.2.5.3 Diagrama de Atividades

3.2.5.3.1 Diagrama de Atividades I - Geração de Pedido pelo Cliente

4 DESENVOLVIMENTO

4.1 Arquitetura do Sistema

4.2 Tecnologias e Ferramentas

4.3 API REST e Endpoints

4.4 Regras de Negócio Implementadas

4.4.1 Controle de Estoque e Concorrência

4.4.2 Pedidos e Ciclo de Status

4.4.3 Imagens dos Produtos

4.4.4 Telefones, Foto de Perfil e Imagem da Loja

4.4.5 Favoritos

4.4.6 Avaliações de Produtos

4.4.7 Preservação do Histórico de Pedidos

4.4.8 Redefinição de Senha

4.5 Interfaces do Sistema

4.5.1 Login

4.5.2 Cadastro de Cliente

4.5.3 Recuperação de Senha

4.5.4 Catálogo de Produtos

4.5.5 Detalhe do Produto

4.5.6 Carrinho

4.5.7 Favoritos

4.5.8 Meus Pedidos

4.5.9 Perfil do Usuário

4.5.10 Cadastro da Loja

4.5.11 Área do Produtor e Painel

4.5.12 Quadro de Pedidos do Produtor

4.5.13 Produtos da Loja

4.5.14 Dados da Loja

4.6 Implantação

4.7 Testes e Verificação

5 CONSIDERAÇÕES FINAIS

5.1 Limitações

5.2 Trabalhos Futuros

6 CRONOGRAMA

REFERÊNCIAS

# 1 INTRODUÇÃO

<!-- orientador: revisar -->
O presente trabalho apresenta o desenvolvimento do Agro Store, uma plataforma digital voltada à intermediação de pedidos entre consumidores e produtores rurais participantes da Feira do Produtor Rural Willi Dummer, no município de Camaquã/RS. A iniciativa surgiu da observação direta do evento, realizado semanalmente nas manhãs de sábado, na qual foi possível constatar a ausência de ferramentas digitais nos processos de divulgação e comercialização dos produtos ofertados pelos agricultores locais.

<!-- orientador: revisar -->
A Feira do Produtor Rural Willi Dummer representa uma importante fonte de renda para pequenos produtores da região, mas sua dinâmica presencial e o horário restrito limitam significativamente o alcance das vendas. Sem um canal digital, os produtores perdem oportunidades de negócio fora do período do evento e enfrentam dificuldades para organizar seus pedidos com antecedência. Essa lacuna motivou o desenvolvimento de um sistema que permitisse gerenciar os quatro pilares essenciais da cadeia comercial: o produtor rural, o produto, o cliente e a venda.

## 1.1 Objetivos

Nas seções abaixo estão descritos o objetivo geral e os objetivos específicos desta pesquisa.

### 1.1.1 Objetivo Geral

Desenvolver uma plataforma digital para intermediar pedidos entre consumidores e produtores rurais da Feira do Produtor Rural Willi Dummer, em Camaquã/RS, permitindo o cadastro de produtos, a realização de pedidos e o acompanhamento do status de cada venda, com perfis distintos para produtor, cliente e administrador, utilizando Django REST Framework no backend e Vue.js no frontend, com retirada dos pedidos na própria feira.

### 1.1.2 Objetivos Específicos

Para alcançar o objetivo geral, foram definidos os seguintes objetivos específicos:

- Realizar pesquisa bibliográfica sobre agricultura familiar, feiras de produtores rurais, plataformas digitais B2C e tecnologias de desenvolvimento web;

- Realizar o levantamento dos requisitos funcionais e não funcionais do sistema, com base na observação da dinâmica da Feira do Produtor Rural Willi Dummer, em Camaquã/RS;

- Modelar o banco de dados do sistema, elaborando os diagramas entidade-relacionamento conceitual e lógico;

- Confeccionar os diagramas UML do sistema, incluindo diagrama de casos de uso, diagramas de sequência e diagramas de atividades;

- Desenvolver a API REST utilizando Python com Django REST Framework, implementando os endpoints para cada funcionalidade do sistema;

- Desenvolver o frontend da aplicação utilizando Vue.js, com as interfaces para os usuários.

## 1.2 Justificativa

A Feira do Produtor Rural Willi Dummer, em Camaquã, é uma importante fonte de renda para pequenos produtores da região, porém fica limitada ao formato presencial e ao horário restrito de funcionamento, das 6h às 12h de sábado (SILVA, 2025). Sem uma plataforma digital, esses produtores perdem vendas e têm dificuldade de organizar seus pedidos fora do evento. O sistema proposto pode contribuir para o aumento da renda desses produtores e para a movimentação da economia local, ampliando o alcance dos produtos além do dia de feira.

Do ponto de vista acadêmico, o trabalho envolve conceitos fundamentais do curso de Tecnólogo em Análise e Desenvolvimento de Sistemas, como modelagem de banco de dados relacional, desenvolvimento de APIs REST, controle de acesso por perfis de usuário e construção de interfaces web. A integração entre um backend construído em Django REST Framework e um frontend em Vue.js demonstra na prática a arquitetura de sistemas desacoplados, amplamente utilizada no mercado de desenvolvimento de software.

<!-- orientador: revisar -->
## 1.3 Organização do Trabalho

Além desta introdução, o trabalho está organizado em cinco capítulos. O Capítulo 2 apresenta a fundamentação teórica, abordando a agricultura familiar e as feiras de produtores rurais, as plataformas digitais de comercialização, o modelo B2C e os conceitos e tecnologias que sustentam a solução. O Capítulo 3 descreve a metodologia, com o levantamento dos requisitos funcionais e não funcionais e a modelagem do sistema, compreendendo o Diagrama Entidade-Relacionamento, o modelo lógico do banco de dados e os diagramas UML. O Capítulo 4 relata o desenvolvimento do sistema: a arquitetura, as tecnologias empregadas, a API REST, as regras de negócio implementadas, as interfaces, a implantação e a verificação das funcionalidades. O Capítulo 5 apresenta as considerações finais, retomando os objetivos propostos e discutindo as limitações e os trabalhos futuros. Por fim, o Capítulo 6 apresenta o cronograma de atividades.

# 2 FUNDAMENTAÇÃO TEÓRICA

O desenvolvimento do Agro Store apoia-se em um conjunto de conceitos e tecnologias que, articulados, sustentam tanto as decisões de projeto quanto as escolhas técnicas adotadas ao longo do trabalho. Este capítulo percorre esse embasamento em três eixos: o papel da agricultura familiar e das feiras de produtores rurais no Brasil como contexto que motivou a solução; o modelo de marketplace e plataforma digital B2C como referência para a arquitetura de comercialização proposta; e as principais ferramentas e tecnologias empregadas na construção do sistema.

## 2.1 Agricultura Familiar e Feiras de Produtores Rurais

A agricultura familiar é definida pela Lei n.º 11.326/2006 como a atividade agropecuária praticada em estabelecimento rural de até quatro módulos fiscais, sob gestão direta da família, com mão de obra predominantemente familiar (BRASIL, 2006). Os dados do Censo Agropecuário de 2017 evidenciam o peso desse segmento na estrutura agrária brasileira: a agricultura familiar representa 77% dos estabelecimentos rurais do país e responde por 67% da produção nacional de feijão, 70% da produção de mandioca e 34% do leite produzido no Brasil (IBGE, 2019).

No município de Camaquã/RS, a Feira do Produtor Rural Willi Dummer acontece semanalmente, reunindo produtores locais que comercializam hortifrutigranjeiros, produtos artesanais e derivados da agricultura familiar, com funcionamento das 6h às 12h de sábado (SILVA, 2025).

Ainda que economicamente relevantes, essas feiras operam sem suporte digital. Sem canais de venda online, o alcance dos produtores fica restrito ao público presente no local e ao horário do evento, o que representa uma lacuna concreta que o uso de tecnologias da informação pode contribuir para suprir.

## 2.2 Plataformas Digitais de Comercialização

As plataformas digitais de comercialização podem ser compreendidas como sistemas web que possibilitam a divulgação, organização e realização de processos comerciais por meio da internet, conectando ofertantes e consumidores em um mesmo ambiente virtual. Essas plataformas contribuem para ampliar o alcance dos produtos, facilitar o acesso às informações e otimizar etapas relacionadas à compra, venda e gestão de pedidos.

Entre os modelos de plataforma digital de comercialização, destaca-se o marketplace, caracterizado por reunir diferentes vendedores e compradores em um único ambiente online, permitindo a oferta de produtos ou serviços de múltiplos fornecedores. O que diferencia esse modelo de uma loja virtual comum é a presença de diversos vendedores, possibilitando que o consumidor consulte produtos, compare ofertas e realize pedidos de forma centralizada (SEBRAE RS, 2024).

No contexto da agricultura familiar, plataformas digitais e iniciativas de comercialização direta podem ampliar o alcance da produção local, conectando produtores rurais a consumidores além dos limites físicos e horários das feiras presenciais. O Agro Store adapta esse conceito à realidade dos produtores participantes da Feira do Produtor Rural Willi Dummer, em Camaquã/RS, permitindo a divulgação digital de produtos, a realização antecipada de pedidos e a organização da demanda pelos produtores, mantendo a retirada dos pedidos na feira física.

## 2.3 Modelo B2C

<!-- orientador: revisar -->
O modelo B2C, sigla para Business to Consumer, representa uma forma de transação comercial em que empresas vendem produtos ou serviços diretamente ao consumidor final. Esse modelo é comum em setores como varejo, comércio eletrônico e serviços, tendo como foco o atendimento das necessidades de consumidores individuais. Diferencia-se do modelo B2B, no qual as transações ocorrem entre empresas, e do modelo C2C, no qual a negociação ocorre entre consumidores (STRONG BUSINESS SCHOOL, [2026?]).

No contexto do Agro Store, o modelo B2C é utilizado como referência conceitual, uma vez que os produtores rurais participantes da plataforma precisam possuir CNPJ para atuar na feira física. Dessa forma, os produtores cadastrados são tratados no sistema como fornecedores formalizados, que disponibilizam seus produtos diretamente aos consumidores finais. Embora a retirada dos pedidos ocorra presencialmente na feira, o processo de divulgação, seleção de produtos e geração de pedidos é realizado por meio da plataforma digital, aproximando a solução do modelo de comercialização direta entre fornecedor e consumidor.

## 2.4 Ferramentas e Tecnologias Utilizadas

### 2.4.1 Aplicação Web

Uma aplicação web é um programa armazenado em um servidor remoto e acessado pelo usuário por meio de um navegador, sem necessidade de instalação local no dispositivo. Diferentemente de aplicações desktop tradicionais, pode ser utilizada em qualquer dispositivo com acesso à internet, sejam computadores, tablets ou smartphones (YASAR, 2024).

### 2.4.2 API e REST

<!-- orientador: revisar -->
API (Application Programming Interface) é um conjunto de definições e protocolos que viabiliza a comunicação entre sistemas distintos (ANTUNES, 2019). O estilo arquitetural REST (Representational State Transfer), formulado por Fielding (2000), estrutura a comunicação entre sistemas por meio de requisições HTTP, utilizando verbos como GET, POST, PUT, PATCH e DELETE para definir as operações realizadas sobre os recursos. As respostas são habitualmente retornadas no formato JSON, compatível com a grande maioria das linguagens de programação modernas. Esse modelo é amplamente adotado no desenvolvimento de APIs por favorecer a separação entre o backend e o frontend da aplicação, permitindo que diferentes clientes consumam os mesmos endpoints de forma padronizada (RAMOS, 2024).

### 2.4.3 Python

<!-- orientador: revisar -->
Criada em 1991 por Guido van Rossum, Python é uma linguagem de programação de alto nível, interpretada e de código aberto. Sua sintaxe clara e sua extensa biblioteca padrão contribuem para que seja adotada em áreas tão distintas quanto desenvolvimento web, ciência de dados e automação (PYTHON SOFTWARE FOUNDATION, 2024). O índice TIOBE, que acompanha a popularidade das linguagens de programação, a posiciona consistentemente entre as linguagens mais utilizadas no mundo (TIOBE SOFTWARE, 2026).

### 2.4.4 Django e Django REST Framework

Django é um framework web desenvolvido em Python com foco em produtividade e segurança. Segue o padrão arquitetural MTV (Model-Template-View), variação do MVC, e oferece recursos prontos como autenticação de usuários, ORM para mapeamento objeto-relacional e painel administrativo gerado automaticamente, além de proteções nativas contra vulnerabilidades recorrentes em aplicações web (DJANGO SOFTWARE FOUNDATION, 2024).

O Django REST Framework (DRF) complementa o Django com ferramentas voltadas especificamente à construção de APIs REST, incluindo serialização de dados, controle de permissões e documentação automática de endpoints. É a biblioteca mais adotada para esse fim no ecossistema Python (CHRISTIE, 2024).

### 2.4.5 Vue.js

Vue.js é um framework JavaScript de código aberto para construção de interfaces de usuário, criado por Evan You em 2014. Organiza a aplicação em componentes reutilizáveis e conta com um sistema de reatividade que reflete alterações de estado diretamente na interface, sem a necessidade de manipulação manual do DOM. Sua curva de aprendizado acessível e a facilidade de integração com projetos já existentes contribuem para sua ampla adoção (VUE.JS, 2024).

### 2.4.6 PostgreSQL

PostgreSQL é um sistema gerenciador de banco de dados relacional de código aberto com desenvolvimento ativo desde 1994. Destaca-se pela conformidade com o padrão SQL, pelo suporte a tipos de dados avançados e pela robustez em ambientes com múltiplos acessos simultâneos, características que o tornam uma escolha consolidada em aplicações web de produção (THE POSTGRESQL GLOBAL DEVELOPMENT GROUP, 2024).

### 2.4.7 MVC e MTV

O padrão arquitetural MVC, formulado por Reenskaug em 1978, organiza uma aplicação em três camadas com responsabilidades distintas: o Model, responsável pelos dados e pela lógica de negócio da aplicação; a View, encarregada da apresentação das informações ao usuário; e o Controller, que define como a interface responde às interações recebidas. Essa separação de responsabilidades torna o sistema mais organizado e facilita a manutenção do projeto por diferentes desenvolvedores ao longo do tempo (GAMMA et al., 2000). O Django adota uma variação desse padrão denominada MTV, na qual o Template corresponde à View do MVC e a View do Django exerce o papel do Controller, preservando os mesmos princípios de separação de responsabilidades.

### 2.4.8 JSON

JSON (JavaScript Object Notation) é um formato textual de troca de dados baseado na sintaxe de objetos do JavaScript, criado por Douglas Crockford nos anos 1990. Por ser leve, legível e amplamente suportado, tornou-se o formato predominante na comunicação entre APIs REST e clientes web (SÁ, 2023).

### 2.4.9 JWT

<!-- orientador: revisar -->
JWT (JSON Web Token) é um padrão aberto definido pela RFC 7519 (JONES; BRADLEY; SAKIMURA, 2015) que representa de forma segura informações entre duas partes por meio de um objeto JSON, geralmente assinado digitalmente. Sua aplicação mais comum é a autenticação: após o login do usuário, um token é gerado e retornado ao cliente, que o envia nas requisições seguintes para acessar recursos protegidos. O token é composto por três partes, cabeçalho, carga útil e assinatura. Pode ser verificado diretamente pelo servidor sem necessidade de consultar o banco de dados a cada requisição (IBM, 2024).

# 3 METODOLOGIA

<!-- orientador: revisar -->
Este capítulo descreve o conjunto de métodos e técnicas adotados para o desenvolvimento do Agro Store. A pesquisa classificou-se como aplicada, de natureza qualitativa, com abordagem de desenvolvimento de software. O trabalho foi conduzido em etapas sequenciais: levantamento de requisitos, modelagem do sistema, implementação e verificação das funcionalidades. As duas primeiras etapas são descritas neste capítulo, e as duas últimas, no Capítulo 4.

## 3.1 Requisitos

<!-- orientador: revisar -->
Os requisitos foram levantados a partir da observação da dinâmica da Feira do Produtor Rural Willi Dummer e refinados ao longo da implementação, à medida que as regras de negócio foram detalhadas. Para permitir sua rastreabilidade ao longo do texto, cada requisito funcional recebeu um código no formato RFnn e cada requisito não funcional, no formato RNFnn. Nos quadros desta seção, a coluna Regra relaciona cada requisito à regra de negócio correspondente, identificada pelo código RN-nnn ou, quando a regra não é numerada, pelo nome da seção correspondente das regras de negócio do projeto, e detalhada no Capítulo 4. O escopo do MVP não contempla pagamento online, entrega em domicílio nem cálculo de frete: o pedido representa uma reserva para retirada presencial na feira, e essas possibilidades são discutidas no Capítulo 5.

### 3.1.1 Requisitos Funcionais

<!-- orientador: revisar -->
O Quadro 1 apresenta os vinte e quatro requisitos funcionais do sistema, isto é, as funções que a plataforma oferece aos seus usuários, conforme implementadas.

**Quadro 1** - Requisitos funcionais

| Código | Descrição | Regra |
| --- | --- | --- |
| RF01 | Cadastro público de conta de cliente, com nome, CPF válido e único, e-mail único, um telefone e seu tipo, que se torna o telefone principal, data de nascimento, com idade mínima de dezesseis anos, gênero e senha com no mínimo oito caracteres e confirmação. O cadastro inicia a sessão automaticamente e não concede o papel de produtor nem privilégios administrativos. | Usuários e autenticação, RN-021, RN-023 |
| RF02 | Autenticação do usuário por CPF e senha, com emissão de token JWT de acesso e de renovação; a interface renova o acesso automaticamente quando ele expira. | — |
| RF03 | Redefinição de senha a partir do e-mail da conta, com envio de um link válido por trinta minutos e de uso único; a solicitação de um novo link invalida os anteriores, a resposta é sempre neutra, a conta inativa não recebe o link e o usuário não é autenticado automaticamente após a troca. | RN-020 |
| RF04 | Alteração do perfil pelo próprio usuário (nome, e-mail, data de nascimento e gênero), com as mesmas validações do cadastro; CPF e papéis não podem ser alterados, e a alteração do perfil não modifica os pedidos já realizados, que preservam o snapshot dos dados do cliente. | Usuários e autenticação, RN-021 |
| RF05 | Foto de perfil opcional e única, enviada, trocada ou removida somente pelo próprio usuário e exibida apenas a ele; sem foto, a interface exibe as iniciais do nome; são aceitos arquivos JPG, PNG ou WEBP de até 5 MB. | RN-018 |
| RF06 | Telefones do usuário: um ou mais, sem limite de quantidade, classificados como Celular (11 dígitos com DDD), Fixo (10 dígitos) ou Comercial (10 ou 11 dígitos), com exatamente um principal; o último telefone não pode ser excluído e, para excluir o principal, é preciso definir outro como principal antes. | RN-021 |
| RF07 | Catálogo público com os produtos ativos, de lojas ativas e com estoque maior que zero, exibindo imagem principal, preço vigente e desconto, com filtro por categoria; a categoria inativa não oculta o produto; busca, ordenação e paginação são feitas na interface. | RN-017 |
| RF08 | Página de detalhe do produto, acessível também pelo endereço direto quando o estoque é zero, com a compra bloqueada; exibe a galeria começando pela imagem principal, o nome e a imagem da loja, sem link, o preço vigente e o desconto, a disponibilidade e as avaliações com a média. | RN-010, RN-016, RN-017, RN-018 |
| RF09 | Somente o usuário com papel de produtor cadastra sua loja (nome, descrição, CNPJ e imagem opcional); cada produtor tem uma única loja, garantida na API e no banco. | RN-013, RN-018 |
| RF10 | Gestão da loja pelo proprietário: alterar nome, descrição e imagem e desativar a loja, o que preserva o histórico e impede novas compras; CNPJ e proprietário não são alterados; a loja não pode ser excluída; a loja inativa continua editável pelo proprietário, e a desativação não apaga a imagem. | RN-013, RN-018, RN-019 |
| RF11 | Gestão dos produtos somente pelo produtor dono: cadastrar, editar, desativar e reativar, sem exclusão; categoria ativa obrigatória no cadastro e na troca de categoria, permanecendo visível e editável o produto cuja categoria se tornou inativa; estoque não negativo validado pela API, com a trava no banco pendente; SKU de 14 dígitos gerado automaticamente e imutável. | RN-017, RN-019 |
| RF12 | Histórico de preços com controle de vigência: o registro de um novo preço encerra automaticamente o preço vigente anterior, e a API não edita nem exclui preços; o desconto é um percentual inteiro entre 0 e 100, calculado pelo backend, e valores negativos são recusados. | — |
| RF13 | Imagens do produto: de zero a cinco, com ordem definida pelo produtor e exatamente uma principal quando houver imagem; a primeira enviada torna-se principal e, ao excluir a principal, a próxima pela ordem é promovida; uma imagem enviada não é substituída, devendo ser excluída para que outra seja enviada; arquivos JPG, PNG ou WEBP de até 5 MB, com editor opcional de enquadramento. | RN-016 |
| RF14 | Listagem pública das categorias ativas, usada no filtro do catálogo e no formulário de produto. As demais regras (sugestão pelo produtor, que nasce inativa; criação, renomeação, ativação e inativação pelo administrador; sem exclusão) são aplicadas pela API, sem interface no MVP. | — |
| RF15 | Disponibilidade por estoque: o produto com estoque zero deixa a listagem e a busca do catálogo, sem alteração do campo ativo, e retorna quando o estoque é reposto; o estoque baixo, de uma a cinco unidades, é sinalizado ao produtor como indicador apenas visual, sendo a notificação ativa um trabalho futuro. | RN-017 |
| RF16 | Carrinho persistido no backend, guardado por loja e agregado pela interface: adicionar, alterar a quantidade, de um até o estoque, e remover itens; produto repetido soma a quantidade; quando o estoque diminui, as quantidades excedentes são reduzidas, e o item que chega a zero permanece como "Sem estoque" e não pode ser finalizado; a reposição não restaura a quantidade anterior. | RN-017 |
| RF17 | Finalização dos itens selecionados do carrinho, com validação do preço vigente no backend, criação de um pedido por loja com status Pendente, sem agrupamento dos pedidos, snapshot dos dados do cliente, sem o telefone, e dos produtos, baixa do estoque, remoção dos itens finalizados e ajuste dos carrinhos de outros clientes; a finalização inteira é recusada se algum item for inválido. | RN-011, RN-017, RN-019, RN-021 |
| RF18 | Acompanhamento dos pedidos pelo comprador, com filtro por status; cancelamento imediato e sem motivo dos pedidos Pendente, com restauração do estoque uma única vez; confirmação do recebimento dos pedidos Pronto para retirada, que passam ao status final Entregue; vale também para o produtor que compra de outra loja. | Status do pedido, RN-022 |
| RF19 | Gestão dos pedidos da própria loja pelo produtor, em quadro kanban: avança somente para o próximo status, sem retorno; cancela pedidos Pendente ou Em preparo, com devolução do estoque; vê o nome do cliente registrado no pedido e, apenas nos pedidos Pendente, Em preparo e Pronto para retirada, o telefone principal atual do cliente. | Status do pedido, RN-021, RN-022 |
| RF20 | Painel de indicadores do produtor (vendas do mês, pedidos no mês, ticket médio, vendas dos últimos sete dias e produtos mais vendidos), considerando somente os pedidos não cancelados, agrupados pela data de criação do pedido e calculados na interface, apenas para acompanhamento. | — |
| RF21 | Favoritos para qualquer usuário autenticado, inclusive o produtor: favoritar e desfavoritar produtos, em lista privada e sem duplicidade; produtos inativos, sem estoque ou de loja inativa permanecem na lista, mas não podem ser adicionados ao carrinho. | — |
| RF22 | Avaliação de item de pedido Entregue por qualquer comprador dono do pedido, com nota de 1 a 5 e comentário opcional de até 500 caracteres, uma vez por item e sem edição ou remoção pelo autor; o item cujo produto foi excluído não pode ser avaliado; as avaliações são públicas, com o nome do avaliador abreviado, e permanecem disponíveis na API mesmo com o produto ou a loja desativados. | RN-010 |
| RF23 | Administração pela área administrativa do Django: remover avaliações, como moderação; consultar pedidos sem editar nem excluir; corrigir telefones, mantendo no mínimo um e exatamente um principal; desativar usuários, com exclusão bloqueada para quem possui pedidos ou loja; conceder o papel de produtor, após contato presencial com a organização da feira. | RN-010, RN-013, RN-019, RN-021, RN-023 |
| RF24 | Exibir ao cliente o dia, o horário e o local de retirada na feira (sábados, das 6h às 12h, Rua Major Lúcio Meireles, nº 61, Centro, Camaquã), informação única para toda a plataforma; o sistema não valida nem bloqueia pedidos fora desse horário. | RN-008 |

Fonte: Confeccionado pelo autor (2026).

### 3.1.2 Requisitos Não Funcionais

<!-- orientador: revisar -->
O Quadro 2 apresenta os dezesseis requisitos não funcionais, que tratam das qualidades e das restrições técnicas do sistema, como segurança, integridade dos dados e organização da arquitetura.

**Quadro 2** - Requisitos não funcionais

| Código | Descrição | Regra |
| --- | --- | --- |
| RNF01 | O sistema expõe seus recursos por meio de uma API REST, com dados no formato JSON, sob o prefixo /api/v1/. | — |
| RNF02 | A autenticação utiliza tokens JWT, com token de acesso válido por cento e vinte minutos e token de renovação válido por um dia; os endpoints são protegidos por padrão, e os públicos são liberados explicitamente. | — |
| RNF03 | O acesso é controlado por perfil (cliente, produtor, administrador) e por propriedade do recurso; operações sobre recursos de outro usuário são recusadas sem expor seus dados. | — |
| RNF04 | O frontend, uma aplicação de página única (SPA), e o backend são projetos independentes, mantidos no mesmo repositório e comunicando-se exclusivamente por HTTP, de modo que diferentes clientes possam consumir a mesma API. | — |
| RNF05 | A interface é acessada por navegador web, sem instalação de software adicional, e adota layout responsivo baseado no Bootstrap. | — |
| RNF06 | As senhas são armazenadas com o algoritmo PBKDF2, padrão do Django, e submetidas aos quatro validadores de senha do Django (similaridade com os dados do usuário, tamanho mínimo de oito caracteres, senhas comuns e senha apenas numérica). | RN-020 |
| RNF07 | O banco de dados garante a integridade referencial e a unicidade de CPF, e-mail, CNPJ, SKU, nome de categoria, favorito por usuário e produto, avaliação por item de pedido, loja por produtor, imagem principal por produto e telefone principal por usuário. | RN-010, RN-013, RN-016, RN-021 |
| RNF08 | O histórico de pedidos é preservado por exclusão restritiva, snapshot dos dados da compra e desativação de produtos, lojas e usuários em vez de exclusão. | RN-019 |
| RNF09 | O sistema impede a venda de quantidade superior ao estoque, inclusive em pedidos simultâneos, por meio de transações e de bloqueio das linhas dos produtos no banco de dados. | RN-017 |
| RNF10 | As regras de negócio críticas são validadas no backend; a interface realiza apenas cálculos de exibição. | — |
| RNF11 | A redefinição de senha armazena somente o hash SHA-256 do código enviado, limita as solicitações a cinco e as confirmações a dez por hora por endereço de origem e transmite o código no fragmento do endereço. | RN-020 |
| RNF12 | O tratamento de dados pessoais segue o princípio da necessidade: o telefone não integra o snapshot do pedido, o nome do avaliador é exibido abreviado e a foto de perfil é exibida apenas ao próprio usuário. | RN-010, RN-018, RN-021 |
| RNF13 | As imagens são aceitas somente nos formatos JPG, PNG ou WEBP, com até 5 MB, conferindo extensão e conteúdo, e são gravadas com nome aleatório; o arquivo antigo é removido do armazenamento ao trocar ou excluir; os arquivos ficam no disco local em desenvolvimento e no Supabase Storage em produção. | RN-016, RN-018 |
| RNF14 | A configuração é feita por variáveis de ambiente, sem credenciais no código-fonte; o banco de dados é o SQLite em desenvolvimento e o PostgreSQL em produção. | — |
| RNF15 | O backend é organizado em aplicações de domínio independentes (usuários, lojas, produtos, carrinhos, pedidos, favoritos e avaliações), permitindo acrescentar módulos sem impacto sobre os existentes. | — |
| RNF16 | As mensagens da API e da interface são apresentadas em português do Brasil. | — |

Fonte: Confeccionado pelo autor (2026).

## 3.2 Modelagem

### 3.2.1 Confecção de Diagramas

A modelagem de um sistema de software envolve a construção de representações abstratas que permitem compreender, comunicar e validar suas estruturas e comportamentos antes mesmo de sua implementação.

<!-- orientador: revisar -->
Nesta seção, a organização dos dados do sistema é abordada por meio do Diagrama Entidade-Relacionamento (DER), proposto por Chen (1976), e do Modelo Lógico do banco de dados, que descrevem as entidades, seus atributos e os vínculos estabelecidos entre elas. Complementarmente, são apresentados diagramas UML (Unified Modeling Language), linguagem padronizada pelo Object Management Group (2017), que documentam o comportamento do sistema sob diferentes perspectivas: o diagrama de casos de uso mapeia as funcionalidades disponíveis e os atores que delas fazem uso; o diagrama de sequência ilustra a troca de mensagens entre os componentes ao longo do tempo; e o diagrama de atividades detalha os fluxos de decisão internos da aplicação.

<!-- orientador: revisar -->
Com exceção do modelo conceitual (Figura 1), elaborado na notação de Peter Chen, os diagramas deste trabalho foram produzidos com o Mermaid, ferramenta de código aberto que gera diagramas a partir de uma descrição textual (MERMAID, 2026). Essa abordagem permite manter o código-fonte de cada diagrama versionado junto ao código do sistema e atualizá-lo sempre que uma regra de negócio é alterada, favorecendo a coerência entre a modelagem e a implementação. Como o Mermaid não oferece um tipo específico para diagramas de casos de uso nem para diagramas de atividades da UML, esses dois diagramas foram representados por fluxogramas que aproximam a notação original. Os diagramas foram exportados como imagens para inclusão no texto.

### 3.2.2 Modelagem do Banco de Dados

Nesta seção são apresentados o Diagrama Entidade-Relacionamento (DER) e o Modelo Lógico do banco de dados da aplicação desenvolvida. Tais diagramas buscam descrever, de maneira gráfica e estruturada, a organização dos dados do sistema, destacando as entidades do sistema, com seus atributos e relacionamentos.

### 3.2.3 Diagrama Entidade-Relacionamento (DER)

<!-- orientador: revisar -->
O diagrama confeccionado para este trabalho apresenta dezoito entidades, descritas a seguir com suas respectivas relações.

<!-- orientador: revisar -->
**Usuário**: representa as pessoas cadastradas no sistema, sejam clientes, produtores rurais ou administradores, que compartilham o mesmo cadastro. Armazena os dados necessários para identificação, autenticação e controle de acesso, como nome, CPF, e-mail, data de nascimento, foto de perfil (opcional), senha e último login, além dos indicadores e_produtor, esta_ativo, e_equipe e e_superusuario, que definem o papel do usuário e a situação da conta. Na versão inicial da modelagem, essa entidade era denominada Cliente; o nome Usuário foi adotado por representar também os produtores e os administradores. Os números de telefone não são armazenados diretamente nessa entidade, mas na entidade Telefone, descrita adiante, o que permite ao usuário manter mais de um contato. Relaciona-se com a entidade Gênero, que classifica o usuário, e com a entidade Loja, permitindo que usuários com papel de produtor estejam vinculados a uma loja cadastrada na plataforma. Também se relaciona com as entidades Telefone, Favorito, Avaliação, Carrinho, Pedido_Cliente e Redefinicao_Senha, uma vez que um usuário pode cadastrar seus telefones de contato, favoritar produtos, avaliar produtos adquiridos, possuir carrinhos de compra, ter seus dados preservados no momento da compra e solicitar a redefinição de sua senha. O vínculo entre o usuário e os pedidos que realiza não é registrado diretamente na entidade Pedido, mas por intermédio da entidade Pedido_Cliente, na cardinalidade (1,1) para (0,n): um usuário pode estar associado a nenhum ou a diversos registros de Pedido_Cliente, enquanto cada registro pertence a exatamente um usuário.

**Loja**: representa as lojas cadastradas pelos produtores rurais na plataforma, armazenando informações como nome, descrição, CNPJ, imagem de perfil e situação de atividade. Relaciona-se com a entidade Usuário, pois uma loja pertence a um usuário produtor, e com a entidade Pedido, visto que uma loja pode receber diversos pedidos. Também se relaciona com a entidade Carrinho, permitindo que os itens adicionados pelos clientes sejam organizados conforme a loja responsável pelos produtos.

<!-- orientador: revisar -->
O relacionamento entre Usuário e Loja ocorre na cardinalidade (0,1) para (1,1): cada loja pertence a exatamente um usuário produtor, e cada usuário possui no máximo uma loja, de modo que o usuário sem papel de produtor não possui loja. Por decisão de projeto, a possibilidade de um mesmo produtor manter várias lojas não foi contemplada no MVP.

<!-- orientador: revisar -->
**Produto**: representa os produtos disponibilizados para comercialização na plataforma, armazenando informações como nome, descrição, código de barras, estoque, SKU, situação de atividade, data de criação e data de atualização. Relaciona-se com a entidade Preço, que armazena os valores associados ao produto; com a entidade Categoria, responsável pela classificação dos produtos; com a entidade Imagem, já que um produto pode possuir de nenhuma a cinco imagens; com a entidade Favorito, pois pode ser favoritado por diferentes usuários; com a entidade Avaliação, uma vez que pode receber avaliações; com a entidade Pedido_Produto, representando sua participação em pedidos; e com a entidade Carrinho_Produto, representando sua inclusão nos carrinhos de compra.

**Preço**: armazena os dados referentes à precificação dos produtos, incluindo valor de venda, valor de custo, valor de desconto, porcentagem de desconto, vigência inicial, vigência final, data de criação e data de atualização. Relaciona-se com a entidade Produto, permitindo que os valores praticados sejam associados aos produtos comercializados na plataforma.

**Categoria**: armazena os dados referentes às categorias dos produtos, como nome, status, data de criação e data de atualização. Relaciona-se com a entidade Produto na cardinalidade 1:N, pois uma categoria pode estar associada a diversos produtos, enquanto cada produto pertence a uma categoria.

<!-- orientador: revisar -->
**Imagem**: armazena os dados das imagens vinculadas aos produtos, como caminho da imagem, ordem de exibição, indicador de imagem principal, data de criação e data de atualização. Relaciona-se com a entidade Produto na cardinalidade (0,n) para (1,1): cada imagem pertence a exatamente um produto, enquanto um produto pode não possuir imagem ou possuir até cinco imagens, limite verificado pela aplicação. Quando há imagens cadastradas, exatamente uma delas é a principal.

<!-- orientador: revisar -->
**Carrinho**: representa o agrupamento dos produtos selecionados por um usuário antes da geração do pedido, armazenando valores como valor líquido, valor bruto, valor de desconto, data de criação e data de atualização. Relaciona-se com a entidade Usuário, indicando o proprietário do carrinho, e com a entidade Loja, permitindo que os carrinhos sejam organizados de acordo com a loja responsável pelos produtos; cada usuário possui no máximo um carrinho por loja. Os produtos inseridos no carrinho são representados pela entidade Carrinho_Produto.

**Carrinho_Produto**: entidade associativa que representa os itens adicionados ao carrinho de compras. Armazena dados como quantidade, data de criação e data de atualização, além de estabelecer o vínculo entre Carrinho e Produto. Essa entidade permite que um carrinho possua múltiplos produtos e que um mesmo produto possa aparecer em diferentes carrinhos de clientes distintos.

<!-- orientador: revisar -->
**Pedido**: representa os pedidos gerados a partir dos itens selecionados no carrinho, armazenando informações financeiras como valor líquido, valor bruto e valor de desconto, além de data de criação e data de atualização. Relaciona-se com a entidade Loja, pois cada pedido está associado à loja responsável pelos produtos; com a entidade Status_Pedido, que indica a situação atual do pedido; com a entidade Pedido_Produto, que armazena os itens do pedido; e com a entidade Pedido_Cliente, na cardinalidade (1,1) para (1,1), que identifica o cliente responsável pela compra e preserva os seus dados no momento em que o pedido foi gerado. Dessa forma, a entidade Pedido não possui referência direta ao usuário.

<!-- orientador: revisar -->
**Pedido_Produto**: entidade associativa que representa os produtos pertencentes a um pedido, armazenando informações como nome do produto, quantidade, valor unitário, valor de desconto, subtotal, data de criação e data de atualização. Relaciona-se com a entidade Pedido e com a entidade Produto, esta na cardinalidade (0,n) para (0,1): um produto pode participar de diversos itens de pedido, e cada item refere-se a no máximo um produto, pois, caso o produto venha a ser excluído, o vínculo é desfeito e o item permanece com os dados registrados no momento da compra. Essa estrutura preserva as informações do produto mesmo que seus dados sejam alterados posteriormente no cadastro original.

<!-- orientador: revisar -->
**Pedido_Cliente**: armazena os dados do cliente no momento da geração do pedido, como nome, CPF, e-mail, data de nascimento e gênero. Esse conjunto de dados constitui um *snapshot*, isto é, uma cópia das informações tal como se encontravam no instante da compra. Por decisão de projeto, o telefone do cliente não integra esse *snapshot*: quando necessário para a retirada, ele é consultado no cadastro atual do usuário, conforme justificado na Seção 4.4.7. A entidade cumpre duas funções: estabelece o vínculo entre o pedido e o usuário que o realizou e preserva o registro histórico das informações utilizadas na compra. Relaciona-se com a entidade Pedido na cardinalidade (1,1) para (1,1), pois cada pedido possui exatamente um registro de dados do cliente, e com a entidade Usuário na cardinalidade (0,n) para (1,1), pois cada registro pertence a um único usuário, que pode acumular diversos pedidos ao longo do tempo. Essa entidade é importante para preservar os dados do pedido mesmo que o usuário altere posteriormente suas informações cadastrais.

A concentração do vínculo com o cliente e do *snapshot* em uma mesma entidade, separada de Pedido, foi adotada para evitar que a mesma informação seja mantida em dois lugares e para reforçar a preservação do histórico de compras. Com essa organização, a entidade Pedido descreve apenas a transação comercial com a loja, enquanto a identificação do comprador permanece associada aos dados registrados no momento da compra, o que contribui para a integridade e a rastreabilidade das informações.

<!-- orientador: revisar -->
**Status_Pedido**: armazena, por meio do atributo nome, os possíveis status que um pedido pode assumir durante seu ciclo de vida: Pendente, Em preparo, Pronto para retirada, Entregue e Cancelado. Relaciona-se com a entidade Pedido na cardinalidade 1:N, pois um mesmo status pode estar associado a diversos pedidos.

**Favorito**: entidade associativa que representa o vínculo entre usuários e produtos favoritados, armazenando data de criação e data de atualização. Relaciona-se com as entidades Usuário e Produto, refletindo uma relação N:N, na qual um usuário pode favoritar diversos produtos e um produto pode ser favoritado por diferentes usuários.

<!-- orientador: revisar -->
**Avaliação**: armazena os registros de avaliações realizadas pelos compradores sobre os produtos adquiridos, contendo dados como nota, comentário, data de criação e data de atualização. Relaciona-se com a entidade Pedido_Produto, que representa o item do pedido, na cardinalidade (0,1) para (1,1): cada avaliação refere-se a exatamente um item de pedido, e cada item de pedido pode receber no máximo uma avaliação. Relaciona-se também com a entidade Usuário, na cardinalidade (0,n) para (1,1), pois um usuário pode registrar diversas avaliações e cada avaliação pertence a um único usuário, e com a entidade Produto, na cardinalidade (0,n) para (0,1), pois um produto pode receber diversas avaliações e cada avaliação refere-se a no máximo um produto: caso o produto seja excluído, o vínculo é desfeito, e a avaliação permanece associada ao item do pedido. A associação com o pedido ocorre de forma indireta, por meio do item avaliado, o que contribui para que somente produtos efetivamente comprados possam ser avaliados.

<!-- orientador: revisar -->
**Gênero**: armazena os gêneros disponíveis para classificação dos usuários cadastrados no sistema, por meio dos atributos código e nome. Relaciona-se com a entidade Usuário, permitindo associar cada usuário ao gênero informado no cadastro. As opções padrão são Masculino (código M), Feminino (código F) e Prefiro não informar (código I); outras opções podem ser cadastradas ou renomeadas pelo administrador, e um gênero associado a algum usuário não pode ser excluído. Como o *snapshot* de Pedido_Cliente registra o nome do gênero vigente no momento da compra, a renomeação de uma opção não altera os pedidos já realizados.

<!-- orientador: revisar -->
**Telefone**: armazena os telefones de contato dos usuários, contendo o número, com o DDD (Discagem Direta a Distância), um indicador de telefone principal, a data de criação e a data de atualização. Relaciona-se com a entidade Usuário na cardinalidade (1,n) para (1,1): cada telefone pertence a exatamente um usuário, e cada usuário possui ao menos um telefone, podendo possuir diversos, sem limite de quantidade, dos quais exatamente um é o principal. Essa cardinalidade mínima representa a regra de negócio adotada, segundo a qual todo usuário mantém ao menos um meio de contato. No modelo lógico (Figura 2), o mesmo relacionamento aparece com a cardinalidade (0,n), pois o banco de dados não impõe esse mínimo: ele é garantido pela aplicação, conforme a Seção 3.2.4, e o banco admite a exceção das contas anteriores a essa funcionalidade e das contas de superusuário criadas pela linha de comando, descrita na Seção 4.4.4. Relaciona-se também com a entidade Tipo_Telefone, que classifica cada número. Não há restrição de unicidade sobre o número, de modo que um mesmo telefone pode estar cadastrado para usuários diferentes, como pode ocorrer com um telefone compartilhado por membros de uma mesma família.

<!-- orientador: revisar -->
**Tipo_Telefone**: armazena os tipos de telefone admitidos pelo sistema, por meio do atributo descrição, cujos valores são Celular, Fixo e Comercial. Esses tipos são previamente carregados no banco de dados e não são cadastrados pelos usuários. Relaciona-se com a entidade Telefone na cardinalidade (1,1) para (0,n): cada telefone possui exatamente um tipo, e um tipo pode classificar diversos telefones.

<!-- orientador: revisar -->
**Redefinicao_Senha**: armazena as solicitações de redefinição de senha realizadas pelos usuários, contendo o resumo criptográfico (*hash*) do código enviado por e-mail, a data de expiração, a data de utilização e a data de criação. Relaciona-se com a entidade Usuário na cardinalidade (0,n) para (1,1): cada solicitação pertence a exatamente um usuário, enquanto um usuário pode não possuir nenhuma solicitação ou acumular diversas ao longo do tempo, uma vez que o histórico das solicitações é preservado. A data de utilização, quando preenchida, indica que o *link* correspondente já foi utilizado ou invalidado e não pode mais ser aceito.

A Figura 1 apresenta o Diagrama Entidade-Relacionamento, confeccionado na etapa de modelagem do sistema.

**Figura 1** - Modelo Conceitual do Diagrama Entidade-Relacionamento

<!-- autor: redesenhar a Figura 1 (versão 2.4, coerente com docs/modelo-logico.sql e a Figura 2). (1) Renomear a entidade Cliente para Usuário e incluir o atributo e_equipe. (2) Remover o atributo "telefone celular" de Usuário e o atributo telefone de Pedido_Cliente. (3) Incluir a entidade Telefone (numero como texto, somente dígitos com DDD; e_principal; data_criacao; data_atualizacao) e a entidade Tipo_Telefone (descricao: Celular, Fixo, Comercial). (4) Usuário (1,1) — possui — (1,n) Telefone; Tipo_Telefone (1,1) — classifica — (0,n) Telefone. (5) Conferir se Redefinicao_Senha consta, com Usuário (1,1) — solicita — (0,n) Redefinicao_Senha. (6) Usuário (0,1) — possui — (1,1) Loja. (7) Produto (0,1) — (0,n) Avaliação e Produto (0,1) — (0,n) Pedido_Produto. (8) Usar "Pedido" no singular. -->

[INSERIR IMAGEM: Figura 1 redesenhada pelo autor (modelo conceitual, versão 2.4)]

Fonte: Confeccionado pelo autor (2026).

### 3.2.4 Modelo Lógico

<!-- orientador: revisar -->
A partir do modelo conceitual, foi elaborado o modelo lógico do banco de dados, apresentado na Figura 2. Nessa representação, as dezoito entidades são convertidas em tabelas, com a definição dos tipos de dados de cada coluna, das chaves primárias e das chaves estrangeiras responsáveis por materializar os relacionamentos entre os dados. Os relacionamentos N:N identificados no DER, como o vínculo entre pedidos e produtos, entre usuários e produtos favoritados e entre carrinhos e produtos, dão origem às tabelas associativas pedido_produto, favorito e carrinho_produto. Além disso, as restrições de unicidade, como as aplicadas às colunas cpf, email, cnpj, sku, ao nome da categoria e do status e a token_hash, contribuem para assegurar a integridade dos dados prevista nos requisitos não funcionais do sistema (RNF07).

<!-- orientador: revisar -->
A tabela imagem possui, além da chave estrangeira para o produto, uma restrição de unicidade condicional, isto é, aplicada apenas às linhas que atendem a uma condição: entre as imagens de um mesmo produto, somente uma pode estar marcada como principal. Dessa forma, o próprio banco de dados impede a existência de duas imagens principais para o mesmo produto, enquanto o limite de zero a cinco imagens por produto é verificado pela API.

<!-- orientador: revisar -->
No modelo lógico, a tabela pedido possui chaves estrangeiras apenas para loja e status_pedido, enquanto a referência ao usuário fica na tabela pedido_cliente, por meio da coluna id_usuario, de preenchimento obrigatório. A coluna id_pedido dessa tabela é única, o que limita a um o número de registros de dados do cliente por pedido. Por fidelidade ao modelo lógico, a Figura 2 representa as relações de pedido com pedido_cliente e com pedido_produto com cardinalidade mínima zero, pois o banco de dados não obriga sua existência; a API, entretanto, cria na mesma transação o pedido, o *snapshot* do cliente e ao menos um item, de modo que todo pedido possui exatamente um registro de dados do cliente e pelo menos um item, conforme representado no DER. Para preservar o histórico de pedidos, as chaves estrangeiras de pedido_cliente para o usuário e de pedido para a loja utilizam a regra de exclusão restritiva (ON DELETE RESTRICT), segundo a qual o banco de dados recusa a exclusão de um registro enquanto existirem outros registros que dependem dele. Assim, não é possível excluir um usuário ou uma loja que possua pedidos associados. Essa escolha substitui a exclusão em cascata (ON DELETE CASCADE), na qual a remoção do registro principal provocaria a remoção automática dos pedidos vinculados e, consequentemente, a perda do histórico de vendas e de compras. Já as referências de pedido_produto e de avaliacao para o produto utilizam a anulação da referência (ON DELETE SET NULL): caso um produto seja excluído, os itens de pedido e as avaliações permanecem, apenas sem o vínculo com o produto.

<!-- orientador: revisar -->
Na tabela loja, a coluna id_proprietario, que referencia o usuário produtor, também é única, o que materializa a relação de no máximo uma loja por produtor. Essa restrição de unicidade complementa a validação realizada pela API e garante a regra mesmo quando duas requisições de criação de loja para o mesmo produtor são processadas simultaneamente: nesse caso, o banco de dados recusa a segunda inclusão, e a API responde com a mesma mensagem de validação apresentada ao usuário. A chave estrangeira dessa coluna adota igualmente a regra de exclusão restritiva, de forma que um produtor que possua loja não pode ser excluído, ainda que a loja não tenha recebido pedidos, e a loja nunca é removida em cascata junto com o seu proprietário.

<!-- orientador: revisar -->
A tabela redefinicao_senha possui chave estrangeira obrigatória para o usuário e uma restrição de unicidade sobre a coluna token_hash, que armazena o *hash* do código enviado no *link* de redefinição. O *hash* é o resultado de uma função criptográfica de mão única, que transforma um valor em uma sequência de tamanho fixo da qual não é possível, na prática, recuperar o valor original (STALLINGS, 2015); no sistema, utiliza-se o algoritmo SHA-256 (NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY, 2015). Assim, mesmo que o conteúdo do banco de dados seja exposto, os códigos dos *links* válidos não podem ser obtidos a partir dele. A tabela possui ainda uma restrição de verificação (CHECK), isto é, uma condição que toda linha deve satisfazer para ser gravada, que exige que a data de expiração seja posterior à data de criação. Diferentemente das tabelas ligadas aos pedidos, a chave estrangeira para o usuário utiliza a exclusão em cascata: como os registros de redefinição de senha são auxiliares ao acesso e não compõem o histórico comercial, não há razão para que impeçam a exclusão de um usuário, e são removidos junto com ele.

<!-- orientador: revisar -->
A restrição de unicidade condicional descrita para as imagens dos produtos também é empregada na tabela telefone, que possui chaves estrangeiras obrigatórias para o usuário e para o tipo de telefone: entre os telefones de um mesmo usuário, no máximo um pode estar marcado como principal. A exigência de que exista exatamente um telefone principal, e de que o usuário mantenha ao menos um telefone, é completada pela aplicação, que marca automaticamente como principal o primeiro telefone cadastrado e recusa a exclusão do último telefone e do telefone principal. Por essa razão, na Figura 2 o relacionamento entre usuario e telefone é representado com a cardinalidade (0,n), que corresponde ao que o banco de dados efetivamente impõe e acomoda as contas sem telefone descritas na Seção 4.4.4, enquanto o DER (Figura 1) adota (1,n), por representar a regra de negócio. A coluna numero é do tipo texto e armazena somente os dígitos, com o DDD, seguindo o mesmo critério adotado para CPF, CNPJ e SKU: trata-se de um identificador sobre o qual não se realizam operações aritméticas, e a quantidade de dígitos é relevante para a validação de acordo com o tipo. A tabela tipo_telefone possui restrição de unicidade sobre a coluna descricao. Assim como na tabela redefinicao_senha, a chave estrangeira de telefone para o usuário utiliza a exclusão em cascata, pois os telefones são dados auxiliares do cadastro e não compõem o histórico comercial; já a chave estrangeira para o tipo utiliza a exclusão restritiva, o que impede a remoção de um tipo que ainda classifique algum telefone. Com a criação dessas tabelas, as colunas de telefone das tabelas usuario e pedido_cliente foram removidas, e os telefones existentes foram transferidos para a nova estrutura, conforme descrito na Seção 4.4.4.

<!-- orientador: revisar -->
Cabe destacar que a Figura 2 representa o modelo lógico-alvo do banco de dados, definido para o PostgreSQL. O esquema implementado, gerado pelas migrações do Django a partir das classes de modelo do backend, já utiliza os mesmos nomes físicos de tabelas, chaves e colunas e chaves primárias do tipo BIGINT, mas ainda difere do modelo-alvo em quatro pontos. Primeiro, quatro relações utilizam a exclusão em cascata onde o modelo-alvo adota a exclusão restritiva: as referências do produto à loja, do preço ao produto e da avaliação ao usuário e ao item do pedido. Segundo, parte das restrições de verificação e de unicidade existe somente no modelo-alvo e é hoje garantida apenas pela validação da API, como as que impedem estoque negativo e valores negativos nos preços, nos carrinhos e nos pedidos, limitam a porcentagem de desconto a valores entre 0 e 100, verificam a vigência dos preços, limitam a nota de 1 a 5 e o comentário a quinhentos caracteres e impedem duas imagens na mesma posição de ordem de um produto. Os itens de pedido constituem exceção: a tabela pedido_produto já possui, no banco de dados implementado, quatro restrições de verificação, que exigem quantidade positiva e valor unitário, valor do desconto e subtotal não negativos. Terceiro, quatro restrições possuem nomes gerados automaticamente pelo framework. Quarto, a obrigatoriedade das colunas sku e codigo_barras está invertida em relação ao modelo-alvo. Ressalta-se ainda que as ações de exclusão e os valores padrão são aplicados pelo ORM do Django, e que a regra PROTECT do Django equivale à exclusão restritiva. Essas diferenças são retomadas como limitação na Seção 5.1 e como trabalho futuro na Seção 5.2.

A Figura 2 apresenta o modelo lógico do banco de dados.

**Figura 2** - Modelo Lógico do Diagrama Entidade-Relacionamento

[INSERIR IMAGEM: docs/diagramas/fig02-modelo-logico.png]

Fonte: Confeccionado pelo autor (2026).

### 3.2.5 Diagramas UML

Nesta seção são apresentados os diagramas UML elaborados durante a modelagem do sistema proposto. Os diagramas têm como objetivo representar de forma visual e estruturada o funcionamento da aplicação e a interação entre seus componentes, contemplando diagramas de casos de uso, de sequência e de atividade, que auxiliam na compreensão de fluxos e comportamentos do sistema.

#### 3.2.5.1 Diagrama de Casos de Uso

Conforme detalhado nos requisitos do sistema, a distinção entre os perfis de usuários exige a especificação das ações permitidas a cada um, caracterizando-os como atores do sistema. Dessa forma, a Figura 3 apresenta o Diagrama de Casos de Uso do Agro Store, que ilustra as interações entre esses atores e as funcionalidades disponíveis na plataforma.

- **Atores:**

<!-- orientador: revisar -->
- **Visitante:** representa a pessoa que acessa a plataforma sem estar autenticada. Pode consultar o catálogo, o detalhe dos produtos e as avaliações publicadas, além de criar sua conta de cliente e, caso já possua conta e tenha esquecido a senha, solicitar a redefinição.

<!-- orientador: revisar -->
- **Cliente:** representa o usuário consumidor da plataforma, responsável por acessar o catálogo de produtos, adicionar itens ao carrinho, realizar pedidos, acompanhar o andamento das compras, cancelar pedidos ainda pendentes, confirmar o recebimento dos pedidos retirados na feira, editar seus dados de perfil, favoritar produtos e avaliar os itens de pedidos entregues. Esse ator utiliza o sistema com o objetivo de consultar os produtos disponibilizados pelos produtores rurais e realizar pedidos para posterior retirada na feira física.

<!-- orientador: revisar -->
- **Produtor Rural:** representa o usuário responsável pela comercialização dos produtos na plataforma. Por também ser um usuário da plataforma, o produtor herda as funcionalidades do cliente. Além delas, pode cadastrar sua loja, limitada a uma por produtor, gerenciar os dados da loja, cadastrar e manter produtos, preços e imagens, sugerir categorias, acompanhar os pedidos recebidos, cancelar pedidos que ainda não estejam prontos para retirada e atualizar o status dos pedidos conforme o andamento da preparação e da retirada na feira. Esse ator é fundamental para a manutenção do catálogo de produtos e para o atendimento das solicitações realizadas pelos clientes.

<!-- orientador: revisar -->
- **Administrador:** representa o usuário responsável pela gestão e validação de informações dentro da plataforma. Suas atribuições são exercidas, em sua maior parte, na área administrativa do Django: conceder o papel de produtor ao usuário que, após contato presencial com a organização da feira, for habilitado a vender na plataforma; moderar as avaliações publicadas; consultar pedidos; corrigir telefones; e desativar usuários. Pela API, o administrador pode ainda ativar, renomear ou inativar as categorias sugeridas pelos produtores, operação que não dispõe de interface no MVP. A solicitação de habilitação pelo próprio sistema e a aprovação formal de produtores e lojas não fazem parte do MVP e são tratadas como trabalho futuro (Seção 5.2).

- **Casos de Uso:**

<!-- orientador: revisar -->
- **Cadastrar-se como cliente:** caso de uso disponível para o visitante. Permite a criação de uma conta de cliente na plataforma por meio do preenchimento dos dados pessoais necessários para identificação e acesso ao sistema. O cadastro público não cria contas de produtor nem de administrador: o papel de produtor é concedido pelo administrador.

- **Efetuar login:** caso de uso base para todos os atores. Realiza a autenticação do usuário na plataforma, permitindo o acesso às funcionalidades de acordo com o perfil identificado.

<!-- orientador: revisar -->
- **Redefinir senha:** caso de uso disponível a qualquer usuário cadastrado que não esteja autenticado por ter esquecido a senha. O usuário informa o e-mail da conta e recebe, por e-mail, um *link* válido por trinta minutos e de uso único, por meio do qual cadastra uma nova senha. A resposta à solicitação é sempre a mesma, exista ou não uma conta com o e-mail informado, e, após a troca, o usuário deve efetuar login com a nova senha. O fluxo é detalhado na Seção 4.4.8.

<!-- orientador: revisar -->
- **Visualizar catálogo de produtos:** permite ao visitante e ao cliente consultar os produtos disponíveis na plataforma, visualizando informações como nome, descrição, preço, imagens, categoria e loja responsável pela oferta.

- **Gerenciar carrinho:** permite ao cliente adicionar produtos ao carrinho, alterar quantidades, remover itens e consultar os valores relacionados aos produtos selecionados antes da geração do pedido.

- **Realizar pedido:** possibilita ao cliente confirmar a compra dos itens selecionados no carrinho. A partir dessa ação, o sistema gera o pedido, registra os produtos adquiridos, calcula os valores correspondentes e preserva os dados do cliente no momento da compra.

<!-- orientador: revisar -->
- **Acompanhar pedido:** permite ao cliente consultar o andamento dos pedidos realizados, verificando o status atual de cada solicitação, como Pendente, Em preparo, Pronto para retirada, Entregue ou Cancelado.

<!-- orientador: revisar -->
- **Cancelar pedido pendente:** permite ao cliente cancelar um pedido próprio enquanto ele estiver com o status Pendente.

<!-- orientador: revisar -->
- **Confirmar recebimento:** permite ao cliente registrar que retirou na feira um pedido próprio com o status Pronto para retirada, que passa então ao status Entregue. A confirmação não pode ser desfeita e libera a avaliação dos itens do pedido. Por herdar os casos de uso do cliente, o produtor também pode confirmar o recebimento dos pedidos que realizou em outras lojas.

<!-- orientador: revisar -->
- **Editar perfil:** permite ao usuário alterar seus dados pessoais, com exceção do CPF e do perfil de acesso, gerenciar seus telefones de contato, adicionando, editando, excluindo e definindo o telefone principal, bem como enviar, trocar ou remover sua foto de perfil, que é opcional.

<!-- orientador: revisar -->
- **Favoritar produto:** permite ao usuário autenticado, seja cliente ou produtor, marcar produtos de interesse para facilitar consultas futuras. Essa funcionalidade cria um vínculo entre o usuário e o produto favoritado.

<!-- orientador: revisar -->
- **Avaliar item entregue:** possibilita ao cliente registrar uma avaliação sobre um item de pedido com status Entregue, informando uma nota e, opcionalmente, um comentário, garantindo que apenas produtos comprados possam ser avaliados.

<!-- orientador: revisar -->
- **Consultar avaliações do produto:** permite a qualquer pessoa, autenticada ou não, consultar as avaliações publicadas na página de detalhe do produto.

<!-- orientador: revisar -->
- **Cadastrar loja:** funcionalidade atribuída ao produtor rural. Permite que o usuário com papel de produtor cadastre sua loja na plataforma, informando nome, descrição e CNPJ e, opcionalmente, uma imagem da loja. Cada produtor pode possuir somente uma loja.

<!-- orientador: revisar -->
- **Gerenciar loja:** permite ao produtor rural consultar e atualizar o nome, a descrição e a imagem de sua loja, bem como desativá-la, mantendo os dados de apresentação disponíveis aos clientes da plataforma.

<!-- orientador: revisar -->
- **Gerenciar produtos, preços e imagens:** permite ao produtor rural cadastrar, consultar, atualizar e desativar produtos vinculados à sua loja, incluindo informações como nome, descrição, categoria, estoque, código de barras, preços e imagens. O SKU é gerado automaticamente pelo sistema.

<!-- orientador: revisar -->
- **Atualizar status do pedido:** funcionalidade atribuída ao produtor rural. Permite alterar o andamento dos pedidos recebidos, indicando as etapas de preparação dos produtos solicitados pelos clientes e de sua retirada na feira.

<!-- orientador: revisar -->
- **Cancelar pedido da loja:** permite ao produtor rural cancelar um pedido recebido enquanto ele estiver com o status Pendente ou Em preparo.

<!-- orientador: revisar -->
- **Sugerir categoria:** permite ao produtor rural sugerir uma nova categoria de produtos quando as categorias existentes não forem suficientes para classificar adequadamente seus itens. A categoria sugerida é criada inativa. No MVP, esse caso de uso está disponível somente pela API, sem interface própria.

<!-- orientador: revisar -->
- **Ativar ou renomear categoria:** funcionalidade atribuída ao administrador. Permite ativar as categorias sugeridas pelos produtores, bem como renomeá-las ou inativá-las, mantendo a organização e a padronização do catálogo de produtos. No MVP, esse caso de uso está disponível somente pela API.

<!-- orientador: revisar -->
- **Moderar avaliações:** funcionalidade atribuída ao administrador. Permite consultar e remover avaliações pela área administrativa, sem a possibilidade de criá-las ou editá-las.

<!-- orientador: revisar -->
- **Conceder papel de produtor:** funcionalidade atribuída ao administrador. Após o contato presencial do interessado com a organização da feira, o administrador concede o papel de produtor ao usuário pela área administrativa do Django, o que o habilita a cadastrar sua loja.

<!-- autor: incluir na Figura 3 (docs/diagramas/fig03-casos-de-uso.mmd) o caso de uso "Conceder papel de produtor", ligado ao Administrador (RN-023), e exportar a imagem novamente -->

<!-- orientador: revisar -->
- **Solicitar habilitação e criação de loja** e **Aprovar produtor e loja:** casos de uso previstos na modelagem inicial, nos quais o usuário solicitaria a habilitação como produtor pelo próprio sistema e o administrador aprovaria a solicitação. Esses casos de uso não foram implementados no MVP, no qual a habilitação ocorre presencialmente, e aparecem tracejados na Figura 3. Eles são tratados como trabalhos futuros na Seção 5.2.

<!-- orientador: revisar -->
Na Figura 3, encontra-se o Diagrama de Casos de Uso, que apresenta graficamente a relação entre os atores do sistema e as funcionalidades disponíveis na plataforma. Os atores são representados por retângulos, os casos de uso por elipses, e a seta tracejada indica que o produtor herda os casos de uso do cliente.

**Figura 3** - Diagrama de Casos de Uso

[INSERIR IMAGEM: docs/diagramas/fig03-casos-de-uso.png]

Fonte: Confeccionado pelo autor (2026).

#### 3.2.5.2 Diagramas de Sequência

Os diagramas de sequência apresentados nesta seção representam os principais fluxos de interação entre os atores do sistema e os componentes da arquitetura da aplicação. Cada diagrama descreve a ordem das mensagens trocadas entre o usuário, a interface web, a API/Backend e o banco de dados, permitindo compreender o comportamento dinâmico do sistema em funcionalidades essenciais do Agro Store.

##### 3.2.5.2.1 Diagrama de Sequência I - Cadastro de Cliente

<!-- orientador: revisar -->
O Diagrama de Sequência I busca representar visualmente a lógica por trás do processo de cadastro de um novo cliente na plataforma. Como o cadastro público cria somente contas de cliente, o fluxo é iniciado por um visitante. Possui a seguinte estrutura:

- **Atores:**

  - **Visitante:** pessoa que deseja realizar seu cadastro como cliente para acessar as funcionalidades do sistema.

  - **Frontend:** interface visual da aplicação, responsável por coletar os dados informados pelo usuário.

  - **API/Backend:** componente responsável por receber os dados, realizar validações, proteger a senha e solicitar a gravação das informações.

  - **Banco de dados:** componente responsável pela persistência dos dados do novo usuário.

- **Fluxo de Eventos:**

  <!-- orientador: revisar -->

  - **Preenche dados de cadastro:** o fluxo inicia-se quando o visitante informa seus dados pessoais na interface: nome, CPF, e-mail, um telefone e o respectivo tipo (Celular, Fixo ou Comercial), data de nascimento, gênero, senha e confirmação da senha. Os tipos de telefone e as opções de gênero disponíveis são obtidos da API por meio de consultas públicas, uma vez que o visitante ainda não está autenticado.

  - **Envia dados de cadastro:** o *frontend* encaminha as informações preenchidas para a API/Backend.

  - **Valida os dados informados:** a API/Backend consulta o banco de dados para verificar se o CPF e o e-mail já estão cadastrados e valida os demais dados: o CPF deve ser válido, o telefone deve possuir a quantidade de dígitos correspondente ao tipo informado, considerando o DDD (onze dígitos para Celular, dez para Fixo e dez ou onze para Comercial), o usuário deve ter pelo menos dezesseis anos, o gênero deve corresponder a uma opção disponível e a senha deve atender aos critérios mínimos de segurança. Campos que concederiam privilégios, como o papel de produtor, são desconsiderados.

  - **Retorna erro de validação:** caso algum dado seja inválido ou já esteja cadastrado, a API/Backend retorna a mensagem correspondente a cada campo, e o *frontend* solicita a correção das informações.

  - **Protege a senha do usuário:** caso os dados sejam válidos, a senha é protegida por meio de algoritmo de hash antes de ser armazenada.

  - **Salva novo usuário:** a API/Backend solicita ao banco de dados, em uma única transação, a criação do registro do usuário com perfil de cliente e de seu telefone, registrado como telefone principal.

  - **Confirma cadastro:** o banco de dados confirma a persistência das informações.

  - **Gera os tokens de acesso:** a API/Backend gera os tokens JWT de acesso e de renovação do novo usuário.

  - **Retorna usuário cadastrado:** a API/Backend retorna ao *frontend* os tokens e os dados do perfil.

  - **Inicia a sessão:** o *frontend* armazena a sessão e apresenta ao usuário a área autenticada, sem a necessidade de um login adicional.

A Figura 4 apresenta o Diagrama de Sequência I, que detalha o processo de cadastro de cliente.

**Figura 4** - Diagrama de Sequência I - Cadastro de Cliente

[INSERIR IMAGEM: docs/diagramas/fig04-seq-cadastro.png]

Fonte: Confeccionado pelo autor (2026).

##### 3.2.5.2.2 Diagrama de Sequência II - Acesso ao Sistema

O Diagrama de Sequência II busca representar visualmente o fluxo de autenticação do usuário na plataforma. Possui a seguinte estrutura:

- **Atores:**

  - **Usuário:** representa o cliente, produtor rural ou administrador que deseja acessar a área autenticada do sistema.

  - **Frontend:** interface visual responsável por receber CPF e senha.

  - **API/Backend:** componente responsável por validar as credenciais e gerar as credenciais de acesso.

  - **Banco de dados:** componente onde são consultadas as informações do usuário cadastrado.

- **Fluxo de Eventos:**

  - **Informa CPF e senha:** o fluxo inicia-se quando o usuário informa suas credenciais de acesso na tela de login.

  - **Envia credenciais:** o *frontend* encaminha CPF e senha para a API/Backend.

  <!-- orientador: revisar -->

  - **Procura usuário pelo CPF:** a API/Backend mantém somente os dígitos do CPF informado e consulta o banco de dados para localizar o usuário correspondente.

  - **Retorna dados do usuário:** o banco de dados retorna as informações encontradas.

  <!-- orientador: revisar -->

  - **Confere a senha e a situação da conta:** a API/Backend compara a senha informada com a senha protegida armazenada e verifica se a conta está ativa.

  <!-- orientador: revisar -->

  - **Gera credenciais de acesso:** caso as credenciais estejam corretas, a API/Backend gera o token de acesso, válido por cento e vinte minutos, e o token de renovação, válido por um dia.

  - **Retorna acesso autorizado:** a API/Backend envia ao *frontend* a confirmação de autenticação.

  - **Libera área autenticada:** o *frontend* permite que o usuário acesse as funcionalidades disponíveis ao seu perfil. Caso as credenciais estejam incorretas, é retornado um erro de autenticação e o usuário é informado de que o CPF ou a senha são inválidos.

A Figura 5 apresenta o Diagrama de Sequência II, que detalha o processo de acesso ao sistema.

**Figura 5** - Diagrama de Sequência II - Acesso ao Sistema

[INSERIR IMAGEM: docs/diagramas/fig05-seq-login.png]

Fonte: Confeccionado pelo autor (2026).

##### 3.2.5.2.3 Diagrama de Sequência III - Cadastro de Loja pelo Produtor

O Diagrama de Sequência III busca representar visualmente o processo de cadastro de uma loja por um usuário com papel de produtor rural. Possui a seguinte estrutura:

- **Atores:**

  - **Produtor:** usuário responsável por cadastrar e gerenciar uma loja na plataforma.

  - **Frontend:** interface visual utilizada pelo produtor para informar os dados da loja.

  - **API/Backend:** componente responsável por verificar a autenticação, validar o perfil do usuário e solicitar a criação da loja.

  - **Banco de dados:** componente responsável por armazenar os dados da loja cadastrada.

  <!-- orientador: revisar -->
  - **Storage de arquivos:** componente responsável por armazenar o arquivo da imagem da loja, quando enviada.

- **Fluxo de Eventos:**

  <!-- orientador: revisar -->

  - **Informa dados da loja:** o fluxo inicia-se quando o produtor preenche os dados necessários para criação da loja: nome, descrição e CNPJ. Opcionalmente, o produtor pode escolher, nessa mesma etapa, uma imagem para a loja, enviada junto com os demais dados; caso a imagem seja recusada pela validação, a loja não é criada e o produtor pode corrigir o arquivo, conforme descrito na Seção 4.4.4.

  - **Envia dados da loja:** o *frontend* encaminha as informações para a API/Backend.

  - **Verifica autenticação:** a API/Backend valida se o usuário está autenticado no sistema. Caso não esteja, a requisição é recusada.

  - **Valida os dados da loja:** quando uma imagem é enviada, a API/Backend confere sua extensão (JPG, PNG ou WEBP), seu tamanho, de até 5 MB, e seu conteúdo; se a imagem for recusada, é retornada a mensagem correspondente, e a loja não é criada. Em seguida, a API/Backend consulta o banco de dados e verifica, nesta ordem, se o CNPJ já está cadastrado, se o usuário possui papel de produtor e se ele já possui uma loja, uma vez que cada produtor pode possuir somente uma loja. Em qualquer desses casos, a API/Backend retorna um erro de validação com a mensagem correspondente, e o processo é interrompido.

  - **Salva loja vinculada ao produtor:** caso os dados sejam válidos, a API/Backend grava a imagem, quando enviada, no armazenamento de arquivos, com um nome gerado aleatoriamente, e solicita ao banco de dados a criação da loja, já ativa, vinculando-a ao usuário autenticado.

  - **Confirma criação da loja:** o banco de dados confirma o armazenamento das informações.

  - **Retorna dados da loja:** a API/Backend devolve ao *frontend* os dados cadastrados, incluindo o endereço da imagem, quando houver.

  - **Exibe loja cadastrada:** o *frontend* apresenta ao produtor a confirmação do cadastro.

<!-- orientador: revisar -->
A verificação de loja já existente, realizada pela API, é reforçada por uma restrição de unicidade no banco de dados, descrita na Seção 3.2.4. Assim, caso duas solicitações de cadastro de loja do mesmo produtor sejam processadas ao mesmo tempo e ambas passem pela verificação da API, o banco de dados recusa a segunda gravação, e o produtor recebe a mesma mensagem de erro de validação.

A Figura 6 apresenta o Diagrama de Sequência III, que detalha o processo de cadastro de loja pelo produtor.

**Figura 6** - Diagrama de Sequência III - Cadastro de Loja pelo Produtor

[INSERIR IMAGEM: docs/diagramas/fig06-seq-cadastro-loja.png]

Fonte: Confeccionado pelo autor (2026).

##### 3.2.5.2.4 Diagrama de Sequência IV - Cadastro de Produto e Definição de Preço

O Diagrama de Sequência IV busca representar visualmente o processo de cadastro de produtos e definição de seus respectivos preços. Possui a seguinte estrutura:

- **Atores:**

  - **Produtor:** usuário responsável por cadastrar produtos vinculados à sua loja.

  - **Frontend:** interface visual utilizada para informar os dados do produto e seu preço.

  - **API/Backend:** componente responsável por validar a autenticação, registrar o produto e associar as informações de preço.

  - **Banco de dados:** componente responsável pela persistência dos dados de produto e preço.

- **Fluxo de Eventos:**

  <!-- orientador: revisar -->

  - **Carrega as categorias ativas:** ao abrir o formulário de produto, antes do preenchimento dos dados, o *frontend* consulta na API/Backend as categorias ativas, que são obtidas do banco de dados e apresentadas ao produtor no campo de seleção de categoria.

  <!-- orientador: revisar -->

  - **Preenche dados do produto:** em seguida, o produtor informa os dados do produto, como nome, descrição, categoria, código de barras, estoque, preço de venda e percentual de desconto. A loja não é informada, pois o sistema vincula o produto automaticamente à loja do produtor autenticado.

  - **Envia produto:** o *frontend* encaminha os dados do produto para a API/Backend.

  - **Valida os dados do produto:** a API/Backend recusa estoque negativo e categoria inativa, retornando a mensagem correspondente.

  - **Verifica autenticação e perfil:** a API/Backend confirma se o usuário está autenticado, se possui papel de produtor e se já cadastrou sua loja. Caso contrário, a operação é recusada.

  - **Salva produto e gera o SKU:** a API/Backend solicita ao banco de dados a gravação do novo produto e, na mesma transação, gera o SKU (*Stock Keeping Unit*, código de identificação do item em estoque) de forma automática, com quatorze dígitos formados a partir dos identificadores da loja, da categoria e do produto.

  - **Confirma produto cadastrado:** o banco de dados confirma a criação do registro.

  - **Retorna produto criado:** a API/Backend devolve ao *frontend* as informações do produto cadastrado, incluindo o SKU.

  - **Envia preço do produto:** em seguida, o *frontend* encaminha à API/Backend, em uma requisição separada, o preço de venda e o percentual de desconto do produto.

  - **Valida o preço:** a API/Backend verifica se o percentual de desconto está entre 0 e 100, se os valores não são negativos e se o produto pertence à loja do produtor.

  - **Encerra o preço anterior e calcula o desconto:** a API/Backend encerra a vigência do preço anterior, preservando o histórico de preços, e calcula o valor do desconto a partir do percentual informado.

  - **Salva preço vigente:** a API/Backend solicita ao banco de dados o armazenamento do novo preço vigente associado ao produto.

  - **Confirma preço cadastrado:** o banco de dados confirma a gravação das informações.

  - **Exibe produto com preço atual:** o *frontend* apresenta ao produtor o produto cadastrado com seu respectivo preço.

A Figura 7 apresenta o Diagrama de Sequência IV, que detalha o processo de cadastro de produto e definição de preço.

**Figura 7** - Diagrama de Sequência IV - Cadastro de Produto e Definição de Preço

[INSERIR IMAGEM: docs/diagramas/fig07-seq-produto-preco.png]

Fonte: Confeccionado pelo autor (2026).

##### 3.2.5.2.5 Diagrama de Sequência V - Consulta do Catálogo de Produtos

O Diagrama de Sequência V busca representar visualmente o processo de consulta pública dos produtos disponíveis na plataforma. Possui a seguinte estrutura:

- **Atores:**

  - **Visitante ou cliente:** pessoa que acessa a plataforma para consultar os produtos disponíveis, com ou sem autenticação.

  - **Frontend:** interface visual responsável por apresentar o catálogo ao usuário.

  - **API/Backend:** componente responsável por buscar e organizar os dados dos produtos.

  - **Banco de dados:** componente onde são consultadas as informações de produtos, lojas, categorias e preços.

- **Fluxo de Eventos:**

  - **Abre o catálogo de produtos:** o fluxo inicia-se quando o usuário acessa a área de catálogo da plataforma.

  - **Solicita lista de produtos:** o *frontend* envia à API/Backend uma solicitação para recuperar os produtos disponíveis.

  <!-- orientador: revisar -->

  - **Busca produtos, lojas, categorias, preços vigentes e imagens:** a API/Backend consulta o banco de dados para obter os produtos disponíveis, isto é, os produtos ativos, pertencentes a lojas ativas e com estoque maior que zero. Opcionalmente, a consulta pode ser filtrada por categoria.

  - **Retorna produtos encontrados:** o banco de dados devolve os registros localizados.

  - **Monta catálogo formatado:** a API/Backend organiza as informações, incluindo preço atual, preço original, desconto, quando houver, e o endereço da imagem principal de cada produto.

  - **Envia catálogo formatado:** a API/Backend retorna ao *frontend* a lista de produtos preparada para exibição.

  - **Exibe produtos disponíveis:** o *frontend* apresenta os produtos em cartões com a imagem principal ou, na ausência de imagens, com a indicação "Sem foto". Por se tratar de um recurso público, esse fluxo não exige autenticação.

  - **Acessa o detalhe pelo endereço direto:** de forma opcional, o usuário pode abrir a página de um produto ativo de loja ativa mesmo que seu estoque seja zero. Nesse caso, a página informa a condição "Sem estoque" e bloqueia a compra; caso contrário, exibe a galeria de imagens e permite a inclusão no carrinho.

A Figura 8 apresenta o Diagrama de Sequência V, que detalha o processo de consulta do catálogo de produtos.

**Figura 8** - Diagrama de Sequência V - Consulta do Catálogo de Produtos

[INSERIR IMAGEM: docs/diagramas/fig08-seq-catalogo.png]

Fonte: Confeccionado pelo autor (2026).

#### 3.2.5.3 Diagrama de Atividades

Finalizando a apresentação dos diagramas de modelagem UML, encontram-se os diagramas de atividades, responsáveis por representar o fluxo de execução das ações realizadas dentro de processos específicos do sistema. Esses diagramas permitem visualizar a sequência das atividades, os pontos de decisão e os possíveis caminhos alternativos existentes durante a utilização da plataforma.

##### 3.2.5.3.1 Diagrama de Atividades I - Geração de Pedido pelo Cliente

O Diagrama de Atividades I busca modelar o fluxo realizado pelo cliente desde o acesso ao catálogo de produtos até a geração do pedido. Esse processo representa uma das principais funcionalidades do Agro Store, pois descreve o caminho percorrido pelo consumidor para selecionar produtos disponíveis na plataforma, adicioná-los ao carrinho e confirmar a compra. O fluxo possui a seguinte estrutura:

- **Acessar catálogo de produtos:** descreve a ação inicial do cliente ao acessar a listagem de produtos disponíveis na plataforma. A partir dessa ação, o sistema busca os produtos disponíveis, isto é, os produtos ativos, pertencentes a lojas ativas e com estoque maior que zero, com suas respectivas lojas, categorias e preços vigentes, retornando o catálogo formatado para exibição ao usuário.

- **Selecionar produto:** representa a escolha de um item pelo cliente dentro do catálogo. Após a seleção, o sistema busca as informações detalhadas do produto, incluindo dados da loja, descrição, preço vigente e demais informações necessárias para que o cliente decida pela inclusão no carrinho.

- **Adicionar produto ao carrinho:** ocorre quando o cliente informa a quantidade desejada e solicita a inclusão do produto no carrinho. Essa ação gera um nó de decisão responsável por verificar se o cliente está autenticado. Caso não esteja autenticado \[Não\], o sistema informa a necessidade de realizar login e encerra o fluxo. Caso esteja autenticado \[Sim\], o processo continua.

  <!-- orientador: revisar -->

- **Verificar existência do produto no carrinho:** após a autenticação, o sistema verifica se o produto e a loja estão ativos, recusando a inclusão em caso contrário, e se o produto selecionado já está presente no carrinho do cliente. Caso o produto já exista \[Sim\], a quantidade informada é somada à quantidade já registrada. Caso o produto ainda não esteja no carrinho \[Não\], um novo item é criado. Em ambos os casos, a quantidade resultante fica limitada ao estoque disponível do produto: se a ultrapassar, a inclusão é recusada e o cliente é informado de que não há estoque suficiente. Quando a inclusão é aceita, o sistema grava o item no carrinho da loja e recalcula os totais.

- **Exibir produto no carrinho:** representa o retorno visual ao cliente após a inclusão ou atualização do item. O sistema apresenta o carrinho atualizado, contendo os produtos selecionados, suas quantidades e os subtotais calculados.

- **Abrir carrinho:** descreve a ação do cliente ao acessar o resumo da compra. Nesse momento, o sistema busca os itens vinculados aos carrinhos do usuário autenticado, retornando os produtos, lojas, quantidades e preços para exibição.

<!-- orientador: revisar -->
- **Alterar carrinho:** representa uma ação opcional do cliente antes da confirmação da compra. Caso deseje alterar o carrinho \[Sim\], o cliente pode modificar a quantidade de um item, de um até o estoque disponível, ou removê-lo. O sistema atualiza os dados e exibe novamente o resumo da compra. Caso não deseje realizar alterações \[Não\], o fluxo segue para a confirmação da compra.

<!-- orientador: revisar -->
- **Confirmar compra:** ocorre quando o cliente seleciona os itens do carrinho que deseja adquirir e decide gerar o pedido. O sistema recebe a lista de itens selecionados, verifica novamente a credencial de acesso do cliente e bloqueia os produtos envolvidos, sempre na mesma ordem, antes de validá-los.

- **Verificar itens válidos:** esse nó de decisão valida se todos os itens enviados estão aptos para a geração do pedido. Um item é considerado inválido quando não pertence ao carrinho do cliente, quando o produto ou a loja estão inativos, quando sua quantidade é zero (item "Sem estoque"), quando o estoque é insuficiente para a quantidade solicitada ou quando o produto não possui preço vigente. Caso algum item seja inválido \[Não\], a finalização é recusada por inteiro: nenhum pedido é gerado e o cliente é informado do motivo, com a indicação do produto envolvido. Caso todos os itens sejam válidos \[Sim\], o sistema segue para o processamento da compra.

- **Agrupar itens por loja:** os itens selecionados são organizados de acordo com a loja responsável por cada produto. Essa etapa é necessária porque um mesmo carrinho pode conter produtos de diferentes produtores, exigindo a geração de pedidos separados para cada loja envolvida.

- **Calcular valores do pedido:** para cada loja envolvida, o sistema consulta os preços vigentes dos produtos, calcula o valor bruto, os descontos aplicáveis e o valor líquido do pedido.

<!-- orientador: revisar -->
- **Criar pedido:** após o cálculo dos valores, o sistema cria o pedido com status inicial Pendente, registra os produtos vinculados ao pedido e copia os dados do cliente, com exceção do telefone, para preservar as informações existentes no momento da compra.

<!-- orientador: revisar -->
- **Baixar o estoque:** o sistema subtrai do estoque de cada produto a quantidade vendida.

<!-- orientador: revisar -->
- **Remover itens comprados do carrinho:** depois que os pedidos são criados, os itens processados são removidos do carrinho, evitando que permaneçam disponíveis para nova compra duplicada.

<!-- orientador: revisar -->
- **Ajustar os carrinhos afetados:** nos carrinhos de outros clientes que contêm os produtos vendidos, as quantidades que ultrapassam o novo estoque são reduzidas a esse valor, podendo chegar a zero, caso em que o item permanece no carrinho com a indicação "Sem estoque". Todas as operações, desde o bloqueio dos produtos até esse ajuste, ocorrem em uma única transação, conforme descrito na Seção 4.4.1.

- **Exibir confirmação da compra:** ao final do processo, o sistema apresenta ao cliente a confirmação da compra realizada e informa que o pedido foi criado com status Pendente, encerrando o fluxo no nó final.

A Figura 9 apresenta o Diagrama de Atividades I, que descreve o processo de seleção de produto, inclusão no carrinho e geração de pedido pelo cliente.

**Figura 9** - Diagrama de Atividades I - Geração de Pedido pelo Cliente

[INSERIR IMAGEM: docs/diagramas/fig09-atividades-pedido.png]

Fonte: Confeccionado pelo autor (2026).

# 4 DESENVOLVIMENTO

<!-- orientador: revisar -->
Este capítulo apresenta o desenvolvimento do Agro Store e descreve as funcionalidades implementadas no MVP (Produto Mínimo Viável, do inglês *Minimum Viable Product*), isto é, a versão do sistema que reúne o conjunto mínimo de funcionalidades necessário para demonstrar a proposta e obter retorno dos seus usuários (RIES, 2012). O código do sistema foi organizado em um único repositório, que contém dois projetos independentes: a API REST, desenvolvida em Python com Django e Django REST Framework, e a interface web, desenvolvida com Vue.js. Durante o desenvolvimento, utilizou-se o banco de dados SQLite, enquanto o PostgreSQL é o banco de dados adotado no ambiente de produção.

<!-- orientador: revisar -->
Ao longo da implementação, os requisitos levantados no Capítulo 3 foram detalhados em regras de negócio, isto é, em definições sobre como o sistema deve se comportar em cada situação. As regras críticas são sempre validadas no *backend*, de modo que a interface não seja a única camada de proteção (RNF10). As seções a seguir apresentam a arquitetura do sistema (Seção 4.1), as tecnologias empregadas (Seção 4.2), a API REST (Seção 4.3), as regras de negócio implementadas (Seção 4.4), as interfaces (Seção 4.5), a implantação (Seção 4.6) e a verificação das funcionalidades (Seção 4.7).

<!-- orientador: revisar -->
## 4.1 Arquitetura do Sistema

O Agro Store adota uma arquitetura desacoplada, na qual a interface web e a API são projetos independentes que se comunicam exclusivamente por requisições HTTP com dados em JSON (RNF04). Os dois projetos são mantidos em um único repositório, organização conhecida como monorepo: a pasta apps/backend contém a API em Django REST Framework, a pasta apps/frontend contém a interface em Vue.js e a pasta scripts reúne os utilitários que iniciam os dois serviços em conjunto durante o desenvolvimento. Essa organização facilita manter a API e a interface coerentes entre si, pois uma alteração de contrato e o ajuste correspondente na interface podem ser registrados juntos.

No *backend*, o código é organizado em aplicações de domínio independentes, uma para cada área do negócio: usuários, lojas, produtos, carrinhos, pedidos, favoritos e avaliações, além de um módulo comum com funções compartilhadas, como a validação de imagens (RNF15). Cada aplicação segue a divisão de responsabilidades do Django descrita na Seção 2.4.7: as classes de modelo (*models*) descrevem as tabelas e são traduzidas pelo ORM em instruções SQL; os *serializers* convertem os dados entre JSON e objetos do modelo e concentram as validações de campos e de regras; e as *views*, em geral organizadas como *ViewSets* do DRF e registradas em roteadores de URLs, recebem as requisições, aplicam autenticação e permissões e coordenam a operação. Regras que envolvem várias entidades, como o ajuste dos carrinhos quando o estoque diminui, foram isoladas em módulos de serviço (*services*), o que evita duplicá-las entre as *views*.

No *frontend*, a interface é uma aplicação de página única (SPA, do inglês *Single Page Application*): o navegador carrega a aplicação uma única vez, e a troca de telas ocorre sem recarregar a página, com a navegação controlada por um roteador. As telas são compostas por componentes reutilizáveis, e o estado compartilhado entre elas, como a sessão do usuário, o carrinho, os favoritos e os dados da área do produtor, é mantido em *stores*, isto é, repositórios centralizados de estado. Toda a comunicação com a API passa por um único módulo de serviço, que envia o token de acesso nas requisições protegidas e, ao receber uma resposta de não autenticado, solicita automaticamente um novo token de acesso com o token de renovação e repete a requisição uma única vez; se a renovação falhar, a sessão é encerrada e o usuário é levado à tela de login. As rotas da área do produtor são protegidas por uma verificação de navegação, que consulta o perfil do usuário na API antes de liberar o acesso. Em desenvolvimento, o servidor da interface encaminha as requisições dos caminhos /api e /media para o *backend*, de modo que a interface não depende de um endereço fixo da API.

A segurança das requisições é tratada na API: a autenticação padrão é feita por JWT, e a permissão padrão exige usuário autenticado, de modo que os endpoints públicos, como o catálogo e o cadastro, precisam ser liberados explicitamente (RNF02). Além do perfil, as consultas são limitadas aos recursos do próprio usuário, e um recurso de outro usuário é tratado como inexistente (RNF03). A Figura 10 apresenta o ciclo de uma requisição na API, desde a ação do usuário na interface até a resposta em JSON, incluindo a renovação automática do token e os pontos em que a requisição pode ser recusada.

**Figura 10** - Ciclo de uma Requisição na API

[INSERIR IMAGEM: docs/diagramas/fig14-ciclo-requisicao.png]

Fonte: Confeccionado pelo autor (2026).

Como mostra a Figura 10, a requisição é encaminhada pelo roteador de URLs à *view* correspondente, que identifica o usuário a partir do token, verifica a permissão do perfil e, nos serviços de redefinição de senha, o limite de requisições por endereço de origem. Nas operações de escrita, o *serializer* valida os dados recebidos e, se forem válidos, o modelo grava as alterações no banco de dados por meio do ORM, dentro de uma transação quando a operação envolve mais de uma tabela. Ao final, o *serializer* converte o resultado em JSON, que é devolvido à interface com o código de status correspondente.

<!-- orientador: revisar -->
## 4.2 Tecnologias e Ferramentas

Os conceitos que fundamentam as principais tecnologias foram apresentados na Seção 2.4. Esta seção lista as tecnologias e ferramentas empregadas no desenvolvimento e o papel de cada uma no Agro Store:

- **Python:** linguagem utilizada no *backend*, na versão 3.14.2 (PYTHON SOFTWARE FOUNDATION, 2024);

- **Django:** *framework* web do *backend*, utilizado pelo ORM, pelas migrações do banco de dados, pela área administrativa, pela autenticação e pelos validadores de senha (DJANGO SOFTWARE FOUNDATION, 2024);

- **Django REST Framework:** biblioteca que fornece as *views*, os *serializers*, as permissões, os roteadores de URLs e a limitação de requisições da API (CHRISTIE, 2024);

- **Simple JWT:** extensão do Django REST Framework responsável pela emissão, pela renovação e pela validação dos tokens JWT (JAZZBAND, 2026);

- **Vue.js:** *framework* utilizado na construção da interface web, na versão 3 (VUE.JS, 2024);

- **Vue Router:** roteador oficial do Vue.js, responsável pela navegação entre as telas e pela verificação de acesso às rotas do produtor (VUE ROUTER, 2026);

- **Pinia:** biblioteca de gerenciamento de estado do Vue.js, utilizada nas *stores* de sessão, carrinho, favoritos, área do produtor, tipos de telefone, gêneros e notificações (PINIA, 2026);

- **Vite:** ferramenta de desenvolvimento e de empacotamento da interface, que fornece o servidor local e o encaminhamento das requisições à API em desenvolvimento (VITE, 2026);

- **Bootstrap:** biblioteca de componentes visuais e de *layout* responsivo, adotada como base visual da interface (BOOTSTRAP, 2026);

- **Node.js:** ambiente de execução JavaScript utilizado para instalar as dependências e executar as ferramentas da interface e os *scripts* do repositório, nas versões 20.19 ou 22.12 e superiores (NODE.JS, 2026);

- **SQLite:** banco de dados que armazena todos os dados em um único arquivo e dispensa um servidor (SQLITE, 2026a), utilizado no desenvolvimento e na execução dos testes automatizados, estes executados também, complementarmente, com o PostgreSQL;

- **PostgreSQL:** banco de dados do ambiente de produção (THE POSTGRESQL GLOBAL DEVELOPMENT GROUP, 2024);

- **Supabase:** plataforma em nuvem que hospeda o banco de dados PostgreSQL de produção e o serviço de armazenamento das imagens, o Supabase Storage (SUPABASE, 2026a; SUPABASE, 2026b);

- **Render:** serviço de hospedagem em nuvem utilizado para executar o *backend* em produção (RENDER, 2026);

- **Vercel:** serviço de hospedagem em nuvem utilizado para publicar a interface web em produção (VERCEL, 2026);

- **Servidor SMTP:** serviço de envio de e-mails utilizado na redefinição de senha em produção (KLENSIN, 2008);

- **Mermaid:** ferramenta utilizada na elaboração dos diagramas a partir de descrições textuais, conforme a Seção 3.2.1 (MERMAID, 2026);

- **flake8:** ferramenta de verificação de estilo de código Python, adotada como padrão de estilo do *backend*, com limite de 150 caracteres por linha.

<!-- autor: incluir a referência do flake8 (documentação oficial) ou retirar o item, se preferir -->

<!-- orientador: revisar -->
## 4.3 API REST e Endpoints

A API do Agro Store segue as convenções descritas a seguir. Todos os endpoints são servidos sob o prefixo /api/v1/, e os dados são trocados no formato JSON, com exceção do envio de imagens, que utiliza o formato multipart/form-data, próprio para arquivos (RNF01). As listagens não são paginadas e devolvem a coleção completa. As datas são representadas no padrão ISO 8601, e CPF, CNPJ, SKU, código de barras e telefones são tratados como texto, preservando eventuais zeros à esquerda. As mensagens de validação são apresentadas em português do Brasil (RNF16). Quando um usuário tenta acessar um recurso de outro usuário, a API responde, na maioria dos casos, como se o recurso não existisse, para não revelar sua existência (RNF03).

As respostas utilizam os códigos de status do protocolo HTTP para indicar o resultado de cada requisição (FIELDING; NOTTINGHAM; RESCHKE, 2022). O Quadro 3 apresenta os códigos retornados pela API e as situações em que ocorrem.

**Quadro 3** - Códigos de status HTTP retornados pela API

| Código | Significado | Situação no Agro Store |
| --- | --- | --- |
| 200 | Sucesso | Consulta ou alteração realizada |
| 201 | Criado | Recurso criado, como cadastro, loja, produto, item do carrinho, pedido ou avaliação |
| 204 | Sem conteúdo | Exclusão ou remoção realizada, sem corpo na resposta |
| 400 | Requisição inválida | Dados inválidos ou regra de negócio recusada, com as mensagens por campo ou uma mensagem geral |
| 401 | Não autenticado | Token ausente, inválido ou expirado |
| 403 | Proibido | Usuário autenticado sem permissão para a operação |
| 404 | Não encontrado | Recurso inexistente ou pertencente a outro usuário |
| 405 | Método não permitido | Operação não habilitada na rota, como a edição ou a exclusão de lojas e de produtos |
| 429 | Requisições em excesso | Limite de solicitações da redefinição de senha excedido |

Fonte: Confeccionado pelo autor (2026).

A API reúne sessenta combinações de método e endereço, organizadas por módulo nos Quadros 4 a 11, nos quais os endpoints são apresentados sem o prefixo /api/v1. Na coluna Permissão, "Público" indica acesso sem autenticação, "Autenticado" indica qualquer usuário com sessão ativa, inclusive o produtor, "Dono" indica o proprietário do recurso, "Produtor" indica o usuário com papel de produtor e "Administrador" indica o usuário da equipe da plataforma. O Quadro 4 apresenta os endpoints de autenticação e de perfil do usuário.

**Quadro 4** - Endpoints de autenticação e perfil do usuário

| Método | Endpoint | Permissão | Descrição |
| --- | --- | --- | --- |
| POST | /usuarios/cadastro/ | Público | Cadastra um cliente e devolve os tokens |
| POST | /usuarios/login/ | Público | Autentica por CPF e senha |
| POST | /usuarios/token/refresh/ | Público | Renova o token de acesso |
| GET | /usuarios/me/ | Autenticado | Consulta o perfil do usuário |
| PATCH | /usuarios/me/ | Autenticado | Altera o perfil e envia ou troca a foto |
| DELETE | /usuarios/me/foto/ | Autenticado | Remove a foto de perfil |
| POST | /usuarios/redefinir-senha/ | Público, até 5 por hora | Solicita o link de redefinição de senha |
| POST | /usuarios/redefinir-senha/confirmar/ | Público, até 10 por hora | Define a nova senha a partir do link |
| GET | /generos/ | Público | Lista as opções de gênero, usadas no cadastro e no perfil |

Fonte: Confeccionado pelo autor (2026).

Os endpoints de usuário também respondem pelo prefixo /api/, e a renovação do token possui ainda o endereço /api/token/refresh/; a interface utiliza somente os endereços apresentados no Quadro 4. O Quadro 5 apresenta os endpoints de telefones do usuário.

**Quadro 5** - Endpoints de telefones do usuário

| Método | Endpoint | Permissão | Descrição |
| --- | --- | --- | --- |
| GET | /usuarios/me/telefones/ | Autenticado | Lista os telefones do usuário, com o principal primeiro |
| POST | /usuarios/me/telefones/ | Autenticado | Adiciona um telefone |
| GET | /usuarios/me/telefones/{id}/ | Dono | Consulta um telefone |
| PATCH | /usuarios/me/telefones/{id}/ | Dono | Altera número e tipo ou define o principal |
| DELETE | /usuarios/me/telefones/{id}/ | Dono | Exclui um telefone que não seja o último nem o principal |
| GET | /tipos-telefone/ | Público | Lista os tipos de telefone, usados no cadastro |

Fonte: Confeccionado pelo autor (2026).

O Quadro 6 apresenta os endpoints de lojas. Não há endpoint de edição nem de exclusão no recurso de lojas: a loja é alterada somente pelo endereço da própria loja do usuário, e a exclusão não é oferecida, para preservar o histórico.

**Quadro 6** - Endpoints de lojas

| Método | Endpoint | Permissão | Descrição |
| --- | --- | --- | --- |
| GET | /lojas/lojas/ | Público | Lista as lojas |
| POST | /lojas/lojas/ | Produtor | Cria a loja do produtor, com imagem opcional |
| GET | /lojas/lojas/{id}/ | Público | Consulta uma loja |
| GET | /lojas/me/ | Autenticado | Consulta a loja do usuário |
| PATCH | /lojas/me/ | Dono | Altera nome, descrição, situação e imagem |
| DELETE | /lojas/me/imagem/ | Dono | Remove a imagem da loja |

Fonte: Confeccionado pelo autor (2026).

O Quadro 7 apresenta os endpoints de produtos e de categorias. Os produtos e as categorias também não possuem exclusão: os produtos são desativados, e as categorias, inativadas.

**Quadro 7** - Endpoints de produtos e categorias

| Método | Endpoint | Permissão | Descrição |
| --- | --- | --- | --- |
| GET | /produtos/ | Público | Lista o catálogo: produtos ativos, de lojas ativas e com estoque |
| POST | /produtos/ | Produtor com loja | Cadastra um produto, com SKU gerado automaticamente |
| GET | /produtos/{id}/ | Público | Consulta um produto ativo de loja ativa |
| PATCH | /produtos/{id}/ | Dono ou administrador | Altera um produto, inclusive estoque e situação |
| GET | /produtos/meus/ | Produtor ou administrador | Lista todos os produtos da própria loja |
| GET | /produtos/categorias/ | Público | Lista as categorias, com filtro por situação |
| POST | /produtos/categorias/ | Produtor ou administrador | Sugere categoria, criada inativa, ou cria categoria |
| GET | /produtos/categorias/{id}/ | Público | Consulta uma categoria |
| PATCH | /produtos/categorias/{id}/ | Administrador | Renomeia, ativa ou inativa uma categoria |

Fonte: Confeccionado pelo autor (2026).

O Quadro 8 apresenta os endpoints de preços e de imagens dos produtos. Os preços não podem ser editados nem excluídos, o que preserva o histórico de valores.

**Quadro 8** - Endpoints de preços e imagens dos produtos

| Método | Endpoint | Permissão | Descrição |
| --- | --- | --- | --- |
| GET | /produtos/precos/ | Autenticado | Lista o histórico de preços dos produtos da própria loja |
| POST | /produtos/precos/ | Dono ou administrador | Registra um novo preço vigente e encerra o anterior |
| GET | /produtos/precos/{id}/ | Autenticado | Consulta um preço da própria loja |
| GET | /produtos/{produto_id}/imagens/ | Público | Lista as imagens de um produto visível |
| POST | /produtos/{produto_id}/imagens/ | Dono ou administrador | Envia uma imagem |
| GET | /produtos/{produto_id}/imagens/{id}/ | Público | Consulta uma imagem |
| PATCH | /produtos/{produto_id}/imagens/{id}/ | Dono ou administrador | Define a imagem principal |
| DELETE | /produtos/{produto_id}/imagens/{id}/ | Dono ou administrador | Exclui a imagem e promove a próxima, se era a principal |
| POST | /produtos/{produto_id}/imagens/reordenar/ | Dono ou administrador | Redefine a ordem de exibição das imagens |

Fonte: Confeccionado pelo autor (2026).

O Quadro 9 apresenta os endpoints do carrinho, que é mantido no servidor, com um carrinho por usuário e por loja.

**Quadro 9** - Endpoints do carrinho

| Método | Endpoint | Permissão | Descrição |
| --- | --- | --- | --- |
| GET | /carrinhos/ | Autenticado | Lista os carrinhos do usuário, um por loja |
| GET | /carrinhos/{id}/ | Dono | Consulta um carrinho |
| POST | /carrinhos/ | Autenticado | Adiciona um produto, somando a quantidade se já existir |
| PATCH | /carrinhos/itens/{item_id}/ | Dono | Altera a quantidade de um item |
| DELETE | /carrinhos/itens/{item_id}/ | Dono | Remove um item do carrinho |

Fonte: Confeccionado pelo autor (2026).

O Quadro 10 apresenta os endpoints de pedidos. A alteração genérica de um pedido não é permitida: o status é alterado somente pelos endpoints específicos de cada operação, que aplicam o fluxo descrito na Seção 4.4.2.

**Quadro 10** - Endpoints de pedidos

| Método | Endpoint | Permissão | Descrição |
| --- | --- | --- | --- |
| GET | /pedidos/ | Autenticado | Lista os pedidos feitos pelo usuário |
| GET | /pedidos/{id}/ | Dono | Consulta um pedido do usuário |
| POST | /pedidos/ | Autenticado | Finaliza os itens selecionados, com um pedido por loja |
| PATCH | /pedidos/{id}/ | Autenticado | Sempre recusado (405) |
| PATCH | /pedidos/{id}/status/ | Produtor da loja ou administrador | Avança ou cancela o pedido conforme o fluxo |
| PATCH | /pedidos/{id}/cancelar/ | Dono | Cancela um pedido Pendente |
| PATCH | /pedidos/{id}/confirmar-entrega/ | Dono | Confirma o recebimento de um pedido Pronto para retirada |
| GET | /pedidos/minha-loja/ | Produtor ou administrador | Lista os pedidos recebidos pela loja |
| GET | /pedidos/status-disponiveis/ | Produtor ou administrador | Lista os status de pedido |

Fonte: Confeccionado pelo autor (2026).

Por fim, o Quadro 11 apresenta os endpoints de favoritos e de avaliações. As avaliações não podem ser editadas nem excluídas pela API.

**Quadro 11** - Endpoints de favoritos e avaliações

| Método | Endpoint | Permissão | Descrição |
| --- | --- | --- | --- |
| GET | /favoritos/ | Autenticado | Lista os favoritos do usuário, do mais recente ao mais antigo |
| POST | /favoritos/ | Autenticado | Favorita um produto |
| GET | /favoritos/{id}/ | Dono | Consulta um favorito |
| DELETE | /favoritos/{id}/ | Dono | Remove um favorito |
| GET | /avaliacoes/ | Público | Lista as avaliações, com filtro por produto |
| POST | /avaliacoes/ | Dono do pedido entregue | Avalia um item de pedido |
| GET | /avaliacoes/{id}/ | Autenticado | Consulta uma avaliação |

Fonte: Confeccionado pelo autor (2026).

Das cinquenta e nove combinações, quarenta e quatro são utilizadas pela interface, além da renovação do token, realizada internamente pelo módulo de comunicação. As demais, como a consulta individual de registros e a gestão de categorias, ficam disponíveis na API para uso futuro ou administrativo.

<!-- orientador: revisar -->
## 4.4 Regras de Negócio Implementadas

Esta seção descreve as regras de negócio implementadas e as decisões técnicas adotadas para garantir sua consistência. Algumas dessas regras, como as de estoque, não haviam sido detalhadas na versão inicial dos requisitos e foram definidas durante o desenvolvimento.

<!-- orientador: revisar -->
### 4.4.1 Controle de Estoque e Concorrência

Na versão inicial do sistema, não havia tratamento específico para produtos com estoque zerado ou reduzido, de modo que itens esgotados permaneciam listados no catálogo e podiam induzir o cliente a tentar uma compra impossível de ser atendida. Para corrigir essa situação, foi definida e implementada uma regra de disponibilidade baseada na quantidade em estoque. O produto cujo estoque atinge zero deixa de ser exibido na listagem pública do catálogo, sem que seu cadastro seja inativado. Como a busca do catálogo é realizada no *frontend* sobre o resultado dessa listagem fornecida pela API, o produto também deixa de ser encontrado pela busca. A página de detalhe permanece acessível por meio do endereço direto e informa a condição "Sem estoque", com a compra bloqueada. Quando o produtor repõe o estoque, o produto volta a ser exibido no catálogo automaticamente, sem nenhuma ação adicional. Essa decisão separa dois conceitos distintos: a inativação, que representa a decisão do produtor de retirar o produto de venda, e a indisponibilidade temporária, que decorre apenas da falta de unidades.

Para apoiar o produtor no acompanhamento do estoque, o sistema adota um limite único e global de cinco unidades para caracterizar o estoque baixo. Na área do produtor, os produtos com estoque entre uma e cinco unidades recebem o indicador "Estoque baixo", e os produtos com estoque zerado recebem o indicador "Sem estoque — fora do catálogo". Um aviso resumido informa a quantidade de produtos ativos em cada situação. Trata-se de uma sinalização apenas visual, exibida quando o produtor acessa a plataforma. Além disso, a API recusa, com mensagem explicativa, qualquer tentativa de registrar estoque negativo.

Como o carrinho é persistido no servidor, a quantidade escolhida pelo cliente pode deixar de corresponder ao estoque real entre o momento da inclusão e o da finalização. Para manter a coerência, o sistema limita a quantidade de cada item ao estoque disponível do produto. Sempre que o estoque diminui, seja pela venda a outro cliente, seja por ajuste feito pelo produtor, as quantidades de todos os carrinhos que ultrapassam o novo estoque são reduzidas a esse valor e gravadas no banco de dados. Essa redução pode chegar a zero. Nesse caso, o item permanece no carrinho com a indicação "Sem estoque" e não pode ser finalizado. Se o cliente tentar finalizar um conjunto de itens que inclua um item nessa condição, a finalização é recusada por inteiro e nenhum pedido é gerado, seguindo o mesmo critério adotado para estoque insuficiente ou produto inativo. Por decisão de projeto, a reposição posterior do estoque não restaura a quantidade que o cliente havia escolhido, pois essa informação não é mantida após o ajuste. Essas regras complementam o fluxo apresentado no Diagrama de Atividades I (Figura 9).

Em um sistema com vários usuários simultâneos, duas compras do mesmo produto podem ser processadas ao mesmo tempo. Cada uma pode ler o mesmo estoque antes que a outra o atualize e, assim, vender mais unidades do que as disponíveis. Esse fenômeno é conhecido como condição de corrida (*race condition*) (SILBERSCHATZ; GALVIN; GAGNE, 2015). Para evitá-lo, a finalização do pedido e a edição do estoque pelo produtor são executadas dentro de uma transação, isto é, um conjunto de operações tratado pelo banco de dados como uma unidade indivisível. Nessa transação, as linhas dos produtos envolvidos recebem um bloqueio pessimista, obtido pela instrução SQL `SELECT ... FOR UPDATE` (THE POSTGRESQL GLOBAL DEVELOPMENT GROUP, 2026). Enquanto uma operação mantém o bloqueio, as demais que precisam do mesmo produto aguardam sua conclusão e então leem o estoque já atualizado, o que impede a venda acima do disponível (RNF09). Na finalização, os produtos são bloqueados sempre na mesma ordem, o que reduz o risco de impasse (*deadlock*) entre transações concorrentes.

Esse bloqueio por linha é efetivo no PostgreSQL, banco de dados adotado no ambiente de produção. Durante o desenvolvimento, utiliza-se o SQLite, sistema gerenciador de banco de dados que armazena todos os dados em um único arquivo e dispensa a instalação de um servidor. O SQLite não oferece bloqueio por linha. Nesse ambiente, a proteção decorre do próprio SQLite, que serializa as operações de escrita no banco de dados (SQLITE, 2026b). Por essa razão, o comportamento de referência para o controle de concorrência é o do PostgreSQL, cuja verificação no ambiente de produção é discutida na Seção 5.1.

<!-- orientador: revisar -->
### 4.4.2 Pedidos e Ciclo de Status

Ao finalizar a compra, o cliente seleciona os itens do carrinho que deseja adquirir, e somente esses itens são convertidos em pedidos; os demais permanecem no carrinho. O preço vigente de cada produto é consultado e validado pelo *backend* no momento da finalização, e os valores exibidos pela interface servem apenas como apoio à decisão do cliente. Os itens selecionados são agrupados pela loja responsável, e um pedido separado é gerado para cada loja envolvida, todos com o status inicial Pendente. Por decisão de projeto, os pedidos de uma mesma finalização não são agrupados em uma compra: o cliente os acompanha separadamente, loja por loja. Essa separação permite que cada produtor acompanhe apenas os pedidos destinados à sua loja, conforme apresentado no Diagrama de Atividades I (Figura 9). Não há pagamento online: o pedido representa uma solicitação de reserva para retirada presencial na feira. O dia, o horário e o local da feira, todos os sábados das 6h às 12h, na Rua Major Lúcio Meireles, nº 61, Centro, Camaquã, constituem uma informação fixa e única para todas as lojas, exibida pela interface no catálogo, no carrinho e na página de pedidos apenas como orientação; o sistema não valida nem bloqueia a criação de pedidos fora desse período (RF24).

O ciclo de vida do pedido segue um fluxo rígido de status, apresentado na Figura 11. O produtor avança o pedido de Pendente para Em preparo e de Em preparo para Pronto para retirada. A última transição, de Pronto para retirada para Entregue, ocorre quando o cliente retira os produtos na feira e pode ser registrada tanto pelo produtor quanto pelo próprio cliente, conforme descrito adiante nesta seção. Não é permitido retornar a um status anterior nem pular etapas. O cancelamento segue regras distintas para cada perfil: o cliente pode cancelar somente os próprios pedidos que ainda estejam com o status Pendente, enquanto o produtor pode cancelar os pedidos da sua loja com o status Pendente ou Em preparo. A partir do status Pronto para retirada, o pedido não pode mais ser cancelado. O cancelamento é imediato, não exige justificativa e mantém o pedido no histórico com o status Cancelado. Todas essas transições são validadas pela API, que recusa, com mensagem explicativa, qualquer alteração fora do fluxo; na interface, o quadro de pedidos do produtor exibe apenas as ações permitidas para o status atual de cada pedido.

**Figura 11** - Diagrama de Estados do Pedido

[INSERIR IMAGEM: docs/diagramas/fig10-estados-pedido.png]

Fonte: Confeccionado pelo autor (2026).

Quando um pedido é cancelado, seja pelo cliente, seja pelo produtor, a quantidade de cada item é devolvida ao estoque do respectivo produto. Como Cancelado é um estado final, do qual o pedido não pode sair, a devolução ocorre uma única vez, o que impede que o mesmo pedido incremente o estoque repetidas vezes. Essa operação é executada dentro de uma transação, com o bloqueio das linhas dos produtos envolvidos, seguindo o mesmo mecanismo descrito na Seção 4.4.1. Para organizar a retirada, o produtor tem acesso somente ao nome do cliente registrado no pedido e, enquanto o pedido estiver em aberto, isto é, com o status Pendente, Em preparo ou Pronto para retirada, ao telefone principal atual do cliente; nos pedidos Entregue e Cancelado, o telefone não é exibido. Essa restrição limita a exposição dos demais dados pessoais registrados na compra, e a decisão de não preservar o telefone no pedido é justificada na Seção 4.4.7.

<!-- orientador: revisar -->
Além da atualização feita pelo produtor, o próprio comprador pode confirmar o recebimento de um pedido. Na página "Meus pedidos", os pedidos com o status Pronto para retirada apresentam o botão "Confirmar recebimento", que abre uma janela de diálogo na qual o cliente confirma a retirada do pedido na feira; com a confirmação, o pedido passa ao status Entregue. A operação é oferecida por um serviço próprio da API, distinto daquele utilizado pelo produtor para atualizar o status, e é permitida somente ao usuário que realizou o pedido. Isso inclui o produtor que tenha comprado de outra loja, uma vez que, conforme a Seção 3.2.5.1, o produtor também atua como cliente da plataforma. A API recusa a confirmação de pedidos em qualquer outro status, com a mensagem "Somente pedidos prontos para retirada podem ter o recebimento confirmado.", e trata o pedido de outro cliente como inexistente, sem revelar sua existência. A confirmação é imediata e não altera o estoque, cuja baixa já ocorreu na geração do pedido. Ela também não pode ser desfeita, pois Entregue é um estado final, do qual o pedido não sai, tanto para o cliente quanto para o produtor. Assim como as demais mudanças de status, a operação é executada dentro de uma transação, com o bloqueio do registro do pedido.

<!-- orientador: revisar -->
A possibilidade de o produtor marcar o pedido como Entregue pelo quadro de pedidos foi mantida, de modo que a retirada pode ser registrada por qualquer uma das partes. Com isso, o encerramento do pedido não depende exclusivamente da atualização feita pelo produtor. Após a confirmação, aplicam-se as regras já descritas para os pedidos entregues: os itens passam a poder ser avaliados, conforme a Seção 4.4.6, e o telefone do cliente deixa de ser exibido ao produtor, conforme a Seção 4.4.7. Por decisão de projeto, o sistema não registra qual das partes confirmou a entrega nem armazena, em campo próprio, a data em que ela ocorreu, pois o pedido guarda apenas o seu status atual, sem as transições anteriores; o registro do histórico de mudanças de status é tratado como trabalho futuro na Seção 5.2.

<!-- orientador: revisar -->
### 4.4.3 Imagens dos Produtos

Cada produto pode reunir de zero a cinco imagens, armazenadas na entidade Imagem com sua ordem de exibição e um indicador de imagem principal. A principal representa o produto no catálogo, enquanto a página de detalhe apresenta uma galeria com todas as fotos, começando pela principal. Uma restrição no banco de dados garante que exista no máximo uma imagem principal por produto, e a API promove automaticamente a imagem seguinte, pela ordem de exibição, quando a principal é excluída, de modo que o catálogo nunca fique sem foto enquanto houver imagens cadastradas. A primeira imagem enviada torna-se a principal automaticamente, e a definição de outra imagem como principal desmarca a anterior. O fluxo de envio e de exclusão é apresentado na Figura 12.

**Figura 12** - Diagrama de Sequência VI - Imagens do Produto

[INSERIR IMAGEM: docs/diagramas/fig11-seq-imagens-produto.png]

Fonte: Confeccionado pelo autor (2026).

Somente o produtor responsável pelo produto, ou o administrador, pode enviar, ordenar, definir a principal ou excluir imagens. No envio, o *backend* aceita apenas arquivos nos formatos JPG (extensão usual do formato JPEG), PNG ou WEBP com até 5 MB, conferindo tanto a extensão quanto o conteúdo do arquivo, e armazena cada imagem com um nome gerado aleatoriamente, o que evita conflitos entre arquivos e não expõe o nome original enviado pelo usuário (RNF13). Uma imagem já enviada não é substituída: para trocá-la, o produtor a exclui e envia outra, e o arquivo excluído é removido do armazenamento. O limite de cinco imagens é verificado com o produto bloqueado, para que envios simultâneos não o ultrapassem.

Para padronizar a apresentação dos produtos, cujos cartões no catálogo utilizam proporção quadrada, a interface oferece um editor opcional de enquadramento. Nele, o produtor posiciona a área de recorte e ajusta o zoom entre uma e três vezes; o recorte quadrado é então gerado no próprio navegador, por meio do elemento Canvas do HTML (WHATWG, 2026), que permite desenhar e exportar imagens por programação. O arquivo resultante é salvo no formato WEBP ou, quando o navegador não oferece esse formato, em JPEG, com lado máximo de 1200 pixels, o que também reduz o tamanho dos arquivos enviados. O recorte no navegador é apenas uma facilidade de uso: as validações de formato, tamanho e permissão permanecem no *backend*.

<!-- orientador: revisar -->
### 4.4.4 Telefones, Foto de Perfil e Imagem da Loja

<!-- orientador: revisar -->
Na versão inicial do sistema, cada usuário possuía um único telefone, armazenado diretamente em seu cadastro e restrito ao formato de celular. Para permitir que o usuário informe mais de um contato e indique a natureza de cada número, essa estrutura foi substituída pelas entidades Telefone e Tipo_Telefone, descritas na Seção 3.2.3. Cada usuário, seja cliente ou produtor, pode cadastrar quantos telefones desejar, classificados como Celular, Fixo ou Comercial, e exatamente um deles é indicado como principal. No cadastro, o usuário informa um telefone e o seu tipo, que se torna o principal. Na página de perfil, somente o próprio usuário pode adicionar novos telefones, editar o número e o tipo dos existentes, excluí-los e definir qual é o principal; a definição de um novo telefone principal desmarca automaticamente o anterior. Para assegurar que o usuário mantenha sempre um meio de contato, a API recusa a exclusão do último telefone e a exclusão do telefone principal, exigindo, neste último caso, que outro telefone seja definido como principal antes da exclusão. Essas operações são executadas dentro de uma transação, com o bloqueio do registro do usuário, de modo que requisições simultâneas não resultem em um usuário sem telefone ou com mais de um telefone principal.

<!-- orientador: revisar -->
O número é validado no *backend* de acordo com o tipo, considerando somente os dígitos e incluindo o DDD: o celular deve possuir onze dígitos, o telefone fixo, dez, e o telefone comercial, dez ou onze, uma vez que pode corresponder tanto a uma linha fixa quanto a uma linha móvel. Quando o tipo de um telefone é alterado, o número é validado novamente segundo o novo tipo. O número é armazenado como texto, somente com dígitos, e não há restrição de unicidade, de modo que o mesmo número pode estar cadastrado para usuários diferentes. Os tipos de telefone são fixos, não podem ser cadastrados pelos usuários e são disponibilizados por uma consulta pública da API, necessária ao formulário de cadastro, que é preenchido sem autenticação. O administrador pode consultar e corrigir os telefones dos usuários pela área administrativa, sujeito às mesmas regras de no mínimo um telefone e de exatamente um telefone principal.

<!-- orientador: revisar -->
A introdução da nova estrutura exigiu a migração dos dados existentes, isto é, a transferência das informações já gravadas para as novas tabelas, realizada por meio do mecanismo de migrações do Django (DJANGO SOFTWARE FOUNDATION, 2026a). O telefone que cada usuário possuía foi copiado para a entidade Telefone como telefone principal, classificado como Celular quando possuía onze dígitos e como Fixo quando possuía dez. Os valores fora desse padrão foram registrados como Celular e podem ser listados por um comando administrativo, para correção posterior, e os valores vazios não geraram registros. Concluída a cópia, a coluna de telefone do cadastro do usuário foi removida. Essa migração integrou o histórico de migrações posteriormente consolidado, conforme descrito na Seção 4.6, e os dados por ela transferidos permanecem nos bancos de dados em que foi aplicada. Por consequência, contas antigas que não possuíam telefone, assim como contas de superusuário criadas pela linha de comando do Django, podem permanecer sem nenhum telefone. Nessas contas, o primeiro telefone cadastrado torna-se automaticamente o principal, e a página de perfil exibe um aviso solicitando o cadastro enquanto não houver telefone; a ausência de telefone não impede o acesso ao sistema nem a realização de compras.

<!-- orientador: revisar -->
Complementarmente, o sistema permite que cada usuário possua uma foto de perfil e que cada loja possua uma imagem de apresentação, ambas opcionais e únicas. A foto de perfil é enviada, trocada ou removida pelo próprio usuário na página de perfil e é exibida somente a ele, nessa página e no menu da conta; ela não aparece em avaliações, em pedidos nem na área do produtor, o que limita a exposição de um dado pessoal (RNF12). Quando o usuário não possui foto, a interface apresenta as iniciais do seu nome. A imagem da loja pode ser escolhida já no cadastro da loja, conforme descrito na Seção 3.2.5.2.3, ou enviada posteriormente na tela Dados da loja (Seção 4.5.14), e somente o proprietário pode enviá-la, trocá-la ou removê-la. Ela é exibida nessa tela, onde é gerenciada, e na página de detalhe do produto, junto ao nome da loja, apenas como identificação; os cartões do catálogo continuam a apresentar a imagem principal do produto. Quando a loja não possui imagem, a interface apresenta a inicial do nome da loja.

<!-- orientador: revisar -->
Ambas as imagens seguem as mesmas validações adotadas para as imagens dos produtos (Seção 4.4.3): o *backend* aceita apenas arquivos JPG, PNG ou WEBP com até 5 MB, conferindo tanto a extensão quanto o conteúdo do arquivo, e armazena cada um com um nome gerado aleatoriamente. Quando o envio é recusado, a imagem atual é mantida. Diferentemente das imagens dos produtos, o envio de uma nova imagem substitui a anterior, e a remoção pode ser feita sem o envio de outra, mediante confirmação em uma janela de diálogo. O arquivo substituído ou removido é excluído do armazenamento somente após a confirmação da transação no banco de dados, isto é, depois que a alteração foi efetivamente gravada, o que evita apagar um arquivo ainda referenciado caso a gravação falhe. Valores antigos de imagem da loja que não seguem o padrão de nome gerado pelo sistema são exibidos como ausência de imagem e não são apagados. A foto de perfil e a imagem da loja não fazem parte do *snapshot* do pedido (Seção 4.4.7), de modo que sua troca ou remoção não altera os pedidos já realizados. Os arquivos são armazenados no disco local durante o desenvolvimento e no Supabase Storage, serviço de armazenamento de arquivos em nuvem (SUPABASE, 2026b), no ambiente de produção.

<!-- orientador: revisar -->
### 4.4.5 Favoritos

A funcionalidade de favoritos permite que qualquer usuário autenticado, seja cliente ou produtor, marque produtos de interesse para consultá-los posteriormente. Os favoritos são persistidos no servidor e vinculados ao usuário autenticado, o que os mantém disponíveis em diferentes dispositivos e sessões. A lista de favoritos é privada, acessível apenas pelo próprio usuário, e apresenta primeiro os produtos favoritados mais recentemente. Um mesmo produto não pode ser favoritado mais de uma vez pelo mesmo usuário, regra garantida tanto pela validação da API quanto por uma restrição de unicidade no banco de dados. Os produtos que se tornam inativos, que ficam sem estoque ou cuja loja é desativada permanecem na lista de favoritos para consulta, mas não podem ser adicionados ao carrinho enquanto estiverem indisponíveis.

<!-- orientador: revisar -->
### 4.4.6 Avaliações de Produtos

As avaliações permitem que os compradores registrem sua opinião sobre os produtos adquiridos, contribuindo para a escolha de outros consumidores. Para garantir que somente produtos efetivamente comprados sejam avaliados, a avaliação é feita sobre um item de pedido, e não diretamente sobre o produto. Somente o usuário autenticado que realizou o pedido pode avaliar seus itens, e somente quando o pedido estiver com o status Entregue. Cada item de pedido pode ser avaliado uma única vez, regra reforçada por uma restrição de unicidade no banco de dados; caso o mesmo produto tenha sido comprado em pedidos diferentes, cada item entregue pode receber sua própria avaliação. A avaliação possui uma nota inteira de um a cinco e um comentário opcional de até quinhentos caracteres. O produto avaliado e o autor da avaliação são definidos pelo *backend* a partir do item e do usuário autenticado, e não a partir de dados enviados pela interface. O item de pedido cujo produto foi excluído e que ainda não havia sido avaliado não pode mais ser avaliado. O fluxo é apresentado na Figura 13.

**Figura 13** - Diagrama de Sequência VII - Avaliação de Item Entregue

[INSERIR IMAGEM: docs/diagramas/fig12-seq-avaliacao.png]

Fonte: Confeccionado pelo autor (2026).

Na interface, a página de pedidos exibe o botão "Avaliar" nos itens de pedidos entregues que ainda não foram avaliados. O botão abre uma janela de diálogo para o registro da nota e do comentário, desenvolvida com atenção a recursos de acessibilidade, e, após o envio, o item passa a exibir a indicação "Avaliado". As avaliações são públicas: qualquer visitante pode consultá-las na página de detalhe do produto, junto com a média das notas, calculada apenas para exibição. Para preservar a privacidade do avaliador, a API retorna somente o primeiro nome e a inicial do sobrenome, sem expor o nome completo.

Depois de enviada, a avaliação não pode ser editada nem removida pelo autor. A remoção é reservada ao administrador, como forma de moderação, por meio da área administrativa, na qual as avaliações podem ser consultadas e excluídas, mas não criadas nem editadas. Após a remoção de uma avaliação pelo administrador, o item de pedido correspondente pode ser avaliado novamente.

<!-- orientador: revisar -->
### 4.4.7 Preservação do Histórico de Pedidos

O histórico de pedidos constitui um registro das transações realizadas entre clientes e produtores e, por isso, deve permanecer consistente mesmo que os cadastros sejam alterados ao longo do tempo. Para isso, o sistema adota o registro de uma cópia dos dados no momento da compra, denominada *snapshot*. Os dados do cliente são preservados na entidade Pedido_Cliente, e os dados dos itens, como o nome do produto, a quantidade, o valor unitário, o desconto e o subtotal, são preservados na entidade Pedido_Produto. Assim, alterações posteriores no perfil do cliente ou no cadastro e no preço dos produtos não modificam os pedidos já realizados.

<!-- orientador: revisar -->
Por decisão de projeto, o telefone constitui uma exceção a esse princípio e não integra o *snapshot* do cliente. Diferentemente do nome, do CPF, do e-mail, da data de nascimento e do gênero, que continuam preservados em Pedido_Cliente, o telefone tem no sistema uma finalidade exclusivamente operacional: permitir que o produtor entre em contato com o cliente para organizar a retirada dos produtos na feira. Para essa finalidade, somente o número atual é útil, pois um número registrado no momento da compra e posteriormente substituído pelo cliente não permitiria o contato. Por essa razão, nos pedidos em aberto, com o status Pendente, Em preparo ou Pronto para retirada, o produtor visualiza o telefone principal atual do cliente, consultado em seu cadastro no momento da exibição, de modo que a troca do telefone principal no perfil altera o contato apresentado nesses pedidos; o telefone permanece visível nesses pedidos mesmo que a conta do cliente tenha sido desativada. Nos pedidos Entregue e Cancelado, nos quais a retirada já foi concluída ou não ocorrerá mais, o telefone não é exibido. Nas contas sem telefone cadastrado, descritas na Seção 4.4.4, o produtor não visualiza nenhum telefone.

<!-- orientador: revisar -->
Essa decisão também se relaciona à proteção de dados pessoais. A Lei Geral de Proteção de Dados Pessoais (LGPD) estabelece, entre seus princípios, o da necessidade, que orienta a limitação do tratamento de dados pessoais ao mínimo necessário para a realização de suas finalidades (BRASIL, 2018, art. 6º, III), prática também referida como minimização de dados (UNIÃO EUROPEIA, 2016, art. 5º). Ao não copiar o telefone em cada pedido e ao deixar de exibi-lo quando o contato para a retirada não é mais necessário, o sistema reduz a quantidade de cópias desse dado e o período em que ele fica exposto ao produtor, sem prejuízo para o histórico comercial, que permanece íntegro quanto aos produtos, aos valores e à identificação do comprador (RNF12). Em contrapartida, o pedido deixa de registrar o telefone utilizado no momento da compra, limitação discutida na Seção 5.1.

Conforme descrito nas Seções 3.2.3 e 3.2.4, o vínculo entre o pedido e o cliente que o realizou é registrado na própria entidade Pedido_Cliente, e não diretamente na entidade Pedido. Essa organização concentra em um único lugar a identificação do comprador e os dados utilizados na compra, evitando que a mesma informação seja mantida em duas entidades.

<!-- orientador: revisar -->
Complementarmente, o sistema impede a exclusão de registros dos quais o histórico depende. Um usuário que possua pedidos e um produtor cuja loja tenha recebido pedidos não podem ser excluídos: a tentativa de exclusão pela área administrativa é recusada, e são exibidos os pedidos que a impedem. A loja não possui operação própria de exclusão, nem na área administrativa nem na API, e a API também não oferece a exclusão de usuários nem de produtos. Para encerrar o acesso de um usuário, o administrador o desativa, mantendo a conta; para encerrar a atividade de uma loja, utiliza-se a desativação, descrita na Seção 4.5.14. Os pedidos, por sua vez, ficam disponíveis na área administrativa apenas para consulta, sem a possibilidade de inclusão, edição ou exclusão, e a alteração de status ocorre exclusivamente pela API, respeitando o fluxo descrito na Seção 4.4.2. Caso um produto venha a ser excluído, os itens de pedido e as avaliações correspondentes são preservados, apenas sem o vínculo com o produto, conforme a Seção 3.2.4 (RNF08).

<!-- orientador: revisar -->
No caso dos produtores, a proteção é mais ampla: enquanto possuir loja, o produtor não pode ser excluído, tenha ou não pedidos associados, pois a referência da loja ao seu proprietário utiliza a regra de exclusão restritiva descrita na Seção 3.2.4. Dessa forma, a loja e os seus produtos nunca são removidos em cascata junto com o usuário. O encerramento da atividade do produtor ocorre por meio de exclusão lógica, isto é, pela marcação do registro como inativo em vez de sua remoção física do banco de dados: a loja é desativada e, quando necessário, o administrador inativa o usuário, preservando o histórico de pedidos, a loja e os produtos.

<!-- orientador: revisar -->
### 4.4.8 Redefinição de Senha

<!-- orientador: revisar -->
As senhas dos usuários são armazenadas pelo mecanismo padrão do Django, que guarda apenas o resultado do algoritmo de derivação de chaves PBKDF2, e não a senha em si (MORIARTY; KALISKI; RUSCH, 2017; DJANGO SOFTWARE FOUNDATION, 2026b). No cadastro e na troca de senha, a senha precisa ter no mínimo oito caracteres e passar pelos validadores do Django, que recusam senhas muito semelhantes aos dados do usuário, senhas comuns e senhas apenas numéricas (RNF06). Como o acesso ao sistema depende de CPF e senha, um usuário que esquece a senha ficaria impedido de utilizar a plataforma sem um meio de recuperá-la. Para atender a essa necessidade, foi implementado um fluxo de redefinição de senha baseado no envio de um *link*, isto é, de um endereço de acesso, para o e-mail cadastrado na conta. Na tela de login, a opção "Esqueci minha senha" conduz a uma tela na qual o usuário informa esse e-mail. A API responde sempre com a mesma mensagem, "Se houver uma conta com este e-mail, enviaremos um link para redefinir a senha.", exista ou não uma conta associada ao endereço informado. Essa resposta neutra impede que a funcionalidade seja utilizada para descobrir quais e-mails estão cadastrados na plataforma, prática conhecida como enumeração de contas (OWASP FOUNDATION, 2026). O e-mail é comparado sem diferenciar letras maiúsculas e minúsculas, e contas inativas não recebem o *link*, embora a resposta permaneça a mesma. O fluxo completo é apresentado na Figura 14.

**Figura 14** - Diagrama de Sequência VIII - Redefinição de Senha

[INSERIR IMAGEM: docs/diagramas/fig13-seq-redefinicao-senha.png]

Fonte: Confeccionado pelo autor (2026).

Quando existe uma conta ativa com o e-mail informado, o *backend* gera um código aleatório e registra, na tabela redefinicao_senha, somente o *hash* desse código, conforme descrito na Seção 3.2.4, junto com a data de expiração. O código em si é enviado apenas no *link* do e-mail. Cada *link* vale por trinta minutos e pode ser utilizado uma única vez, condição registrada pelo preenchimento da data de utilização. Ao solicitar um novo *link*, os anteriores que ainda não foram utilizados são invalidados, de modo que apenas o mais recente permanece válido. No *link*, o código é posicionado no fragmento do endereço, a parte que sucede o caractere "#" e que o navegador não envia ao servidor nas requisições (BERNERS-LEE; FIELDING; MASINTER, 2005). Ao abrir a tela de redefinição, a interface lê o código e o remove imediatamente da barra de endereços e do histórico de navegação, mantendo-o apenas na memória da própria tela, o que reduz o risco de exposição do código em registros de acesso, no histórico do navegador ou no compartilhamento acidental do endereço.

Na tela de redefinição, o usuário informa a nova senha e sua confirmação. A nova senha é submetida às mesmas validações aplicadas no cadastro: deve possuir no mínimo oito caracteres, atender aos critérios de segurança de senha do *backend* e coincidir com a confirmação. Um *link* expirado, já utilizado, invalidado ou inexistente é recusado com a mensagem "Este link de redefinição é inválido ou expirou. Solicite um novo.", e a interface oferece a opção de solicitar um novo *link*; a mesma mensagem é apresentada quando a conta foi desativada, para não revelar o estado da conta. A marcação do *link* como utilizado e a gravação da nova senha ocorrem em uma única transação, e a marcação só é efetivada se o *link* ainda estiver pendente e dentro do prazo, o que impede que duas tentativas simultâneas utilizem o mesmo *link*. Concluída a troca, os demais *links* pendentes do usuário também são invalidados. O usuário não é autenticado automaticamente: a interface encerra a sessão local que eventualmente exista no navegador, apresenta a mensagem "Senha redefinida. Entre com a nova senha." e o encaminha à tela de login, exigindo que a nova senha seja efetivamente informada para o acesso.

Os dois serviços da API envolvidos no fluxo, o de solicitação e o de confirmação, são públicos, pois são utilizados por quem não consegue se autenticar. Para limitar o uso abusivo, como o envio massivo de e-mails ou tentativas sucessivas de adivinhar códigos, o *backend* restringe a quantidade de requisições por endereço IP (*Internet Protocol*) de origem: até cinco solicitações de *link* e até dez tentativas de confirmação por hora (RNF11). Ao exceder esses limites, a API recusa a requisição com a mensagem "Muitas solicitações. Tente novamente mais tarde.".

O envio do e-mail utiliza o recurso nativo do Django. Em ambiente de desenvolvimento, a mensagem é apenas exibida no console do servidor, enquanto, em produção, é enviada por um servidor SMTP (*Simple Mail Transfer Protocol*), protocolo padrão de envio de mensagens eletrônicas (KLENSIN, 2008), configurado por variáveis de ambiente, de modo que as credenciais de acesso não ficam registradas no código-fonte. O e-mail é enviado somente após a gravação da solicitação no banco de dados e, em caso de falha no envio, o erro é registrado no servidor, sem alteração da resposta neutra apresentada ao usuário. Cabe destacar que esse e-mail constitui uma mensagem transacional, isto é, uma resposta direta a uma ação iniciada pelo próprio usuário e necessária para concluí-la. Ele não se confunde com as notificações ativas tratadas na Seção 5.2, como os avisos de mudança de status dos pedidos ou de estoque baixo, que seriam enviadas por iniciativa do sistema e permanecem como trabalho futuro. A verificação desse fluxo, por testes automatizados e por validação manual em ambiente real, é descrita na Seção 4.7.

<!-- orientador: revisar -->
## 4.5 Interfaces do Sistema

Esta seção apresenta as principais telas do Agro Store. Para cada tela, são descritos o objetivo e o perfil de usuário a que se destina, os requisitos funcionais atendidos, os elementos apresentados na figura correspondente e as decisões técnicas adotadas. Antes das telas, cabe descrever os elementos comuns a toda a interface.

A interface utiliza o Bootstrap como base visual, com uma identidade em tons de verde, associada ao contexto rural: a cor primária, aplicada a botões, *links* e destaques, é o verde #2E8B57, o fundo padrão é o verde claro #E8F5E9 e o texto padrão é o verde escuro #1B5E35. Em todas as telas, um cabeçalho apresenta a marca Agro Store, que conduz ao catálogo; um campo de busca de produtos, cujo filtro é aplicado no próprio navegador; os atalhos para os favoritos e para o carrinho, com contadores; e o menu da conta, que exibe a foto de perfil ou as iniciais do usuário e reúne os itens "Meu perfil", "Minha loja", exibido somente a quem possui loja, "Meus pedidos" e "Sair". Ao visitante, o cabeçalho apresenta o botão "Entrar". As mensagens de sucesso, de aviso e de erro são exibidas em notificações no canto superior direito da tela, e as ações que exigem confirmação, como cancelar pedidos ou remover imagens, utilizam uma janela de diálogo padronizada. As telas que exigem autenticação, como o carrinho, os favoritos, os pedidos e o perfil, exibem ao visitante um cartão com o botão "Entrar", que conduz ao login e retorna à tela de origem após a autenticação.

<!-- orientador: revisar -->
### 4.5.1 Login

A tela de login permite que qualquer usuário cadastrado, seja cliente, produtor ou administrador, acesse a área autenticada da plataforma. Atende ao requisito RF02. A Figura 15 apresenta a tela de login.

**Figura 15** - Tela de login

[INSERIR IMAGEM: docs/telas/tela-01-login.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 15, a região à esquerda apresenta um painel de destaque com a mensagem "Bem-vindo à Agro Store", oculto em telas de celular. À direita, um cartão reúne as abas "Entrar" e "Criar conta"; na aba "Entrar", o usuário informa o CPF e a senha, cujo campo possui o botão "Mostrar/Ocultar", e dispõe do *link* "Esqueci minha senha", que conduz à recuperação de senha (Seção 4.5.3). Durante o envio, o botão apresenta a indicação "Entrando...", e os erros são exibidos em notificações; sem resposta do servidor, a tela informa que não foi possível conectar. Quanto às decisões técnicas, após o login os tokens e os dados do usuário são guardados no navegador, e o usuário é conduzido à tela que tentava acessar ou, na ausência dela, ao catálogo; somente endereços internos da própria aplicação são aceitos como destino desse retorno, o que evita o redirecionamento para sítios externos.

<!-- orientador: revisar -->
### 4.5.2 Cadastro de Cliente

A aba "Criar conta" permite que o visitante crie sua conta de cliente. Atende aos requisitos RF01 e RF06. A Figura 16 apresenta a tela de cadastro de cliente.

**Figura 16** - Tela de cadastro de cliente

[INSERIR IMAGEM: docs/telas/tela-02-cadastro.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 16, o formulário solicita o nome completo, o CPF, com máscara de preenchimento, o tipo e o número do telefone, o e-mail, a data de nascimento, o gênero, a senha e sua confirmação. Os tipos de telefone e as opções de gênero são carregados da API ao abrir a aba, com o tipo Celular pré-selecionado; as opções de gênero são, por padrão, Masculino, Feminino e Prefiro não informar, seguidas das demais cadastradas pelo administrador. Se alguma das consultas falhar, a tela exibe um alerta com a opção "Tentar novamente", e o botão "Criar conta" fica desabilitado até que os tipos de telefone e as opções de gênero estejam disponíveis. Quanto às decisões técnicas, a interface realiza validações locais, como os campos obrigatórios, a quantidade de dígitos do telefone conforme o tipo, o tamanho mínimo da senha e a igualdade da confirmação, apenas para orientar o usuário; a validade do CPF e a idade mínima são verificadas somente pelo *backend*, que é a camada responsável pela validação final (RNF10). Concluído o cadastro, a sessão é iniciada automaticamente.

<!-- orientador: revisar -->
### 4.5.3 Recuperação de Senha

A recuperação de senha é composta por duas telas públicas, destinadas ao usuário que esqueceu sua senha. Atende ao requisito RF03. A Figura 17 apresenta a tela de solicitação de redefinição de senha.

**Figura 17** - Tela de solicitação de redefinição de senha

[INSERIR IMAGEM: docs/telas/tela-03-esqueci-senha.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 17, o usuário informa o e-mail da conta, validado localmente quanto ao preenchimento e ao formato, e envia a solicitação; o botão apresenta a indicação "Enviando..." durante o processamento. Após o envio, a tela exibe a mensagem neutra devolvida pela API, com a recomendação de verificar a caixa de *spam*, e o botão "Usar outro e-mail"; quando o limite de solicitações é excedido, é exibido um aviso específico. O *link* "Voltar para o login" permanece disponível. A Figura 18 apresenta a tela de cadastro da nova senha, aberta a partir do *link* recebido por e-mail.

**Figura 18** - Tela de cadastro da nova senha

[INSERIR IMAGEM: docs/telas/tela-05-redefinir-senha.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 18, o usuário informa a nova senha e a confirmação, ambas com o botão "Mostrar/Ocultar"; os erros devolvidos pela API aparecem abaixo dos campos. Quando o *link* é inválido ou expirou, a tela exibe a mensagem correspondente e o botão "Solicitar novo link". Quanto às decisões técnicas, a tela lê o código do fragmento do endereço e o remove imediatamente, conforme a Seção 4.4.8; após a troca, encerra a sessão local que eventualmente exista e conduz o usuário à tela de login.

<!-- orientador: revisar -->
### 4.5.4 Catálogo de Produtos

O catálogo é a vitrine pública da plataforma, acessível a visitantes e a usuários autenticados. Atende aos requisitos RF07, RF21 e RF24. A Figura 19 apresenta o catálogo de produtos.

**Figura 19** - Catálogo de produtos

[INSERIR IMAGEM: docs/telas/tela-06-catalogo.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 19, a parte superior apresenta um *banner* com a informação de retirada na feira. Abaixo, encontram-se os filtros por categoria, com a opção "Todos" e as categorias ativas, e a ordenação por relevância, menor preço, maior preço ou produtos com desconto. A área principal apresenta a grade de cartões de produto, com nove itens por página e paginação. Cada cartão exibe a imagem principal, a loja, o nome, a descrição, o preço, o preço original riscado e o selo de desconto, quando houver, além de um ícone de coração para favoritar; na ausência de imagem, o cartão apresenta a indicação "Sem foto". Durante o carregamento, são exibidos cartões de espaço reservado, e, quando nenhum produto atende aos filtros, a tela apresenta a mensagem "Nenhum produto encontrado." com a opção de limpar os filtros. Quanto às decisões técnicas, a API devolve somente os produtos disponíveis, conforme a Seção 4.4.1, e a busca, o filtro por categoria, a ordenação e a paginação são aplicados no navegador sobre a lista recebida, com seus parâmetros registrados no endereço da página, o que permite compartilhar ou recarregar uma consulta. Ao tentar favoritar sem estar autenticado, o visitante é conduzido ao login.

<!-- orientador: revisar -->
### 4.5.5 Detalhe do Produto

A página de detalhe apresenta as informações completas de um produto e é pública, embora a inclusão no carrinho e o favorito exijam autenticação. Atende aos requisitos RF08, RF16, RF21 e RF22. A Figura 20 apresenta o detalhe do produto.

**Figura 20** - Detalhe do produto

[INSERIR IMAGEM: docs/telas/tela-07-detalhe-produto.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 20, a região à esquerda apresenta a galeria de imagens, começando pela principal. À direita, são exibidos a loja, com sua imagem ou a inicial do nome, sem *link*, o nome do produto, a média e a quantidade de avaliações, com atalho para a seção correspondente, o preço com desconto, a disponibilidade, por exemplo "Disponível: 18 em estoque" ou "Sem estoque", o seletor de quantidade, limitado ao estoque, e os botões "Adicionar ao carrinho" e "Favoritar", seguidos do texto de retirada e da descrição. Quando o produto está sem estoque ou sem preço vigente, a quantidade e o botão de compra ficam desabilitados, e o *backend* também recusa a compra. A Figura 21 apresenta a seção de avaliações da mesma página.

**Figura 21** - Avaliações no detalhe do produto

[INSERIR IMAGEM: docs/telas/tela-08-detalhe-produto-avaliacoes.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 21, cada avaliação apresenta a nota, em estrelas, o nome abreviado do avaliador e o comentário; quando não há avaliações, é exibida a mensagem "Este produto ainda não possui avaliações.". Quanto às decisões técnicas, a média das notas é calculada no navegador apenas para exibição, e o nome do avaliador já chega abreviado da API (RNF12). A imagem da loja é obtida em uma consulta separada, e, caso essa consulta falhe, a página continua funcional, exibindo a inicial do nome da loja. Produto inativo ou de loja inativa não é exibido, e a página informa que o produto não foi encontrado ou está indisponível.

<!-- orientador: revisar -->
### 4.5.6 Carrinho

O carrinho reúne os produtos escolhidos pelo cliente autenticado antes da finalização. Atende aos requisitos RF16, RF17 e RF24. A Figura 22 apresenta o carrinho.

**Figura 22** - Carrinho

[INSERIR IMAGEM: docs/telas/tela-10-carrinho.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 22, a região principal apresenta os itens agrupados por loja. Cada item possui uma caixa de seleção, uma miniatura neutra, o nome com *link* para o produto, o preço unitário com desconto, o seletor de quantidade, o subtotal e o botão de remover. Itens que não podem ser finalizados recebem uma indicação de situação, como "Indisponível", para produto ou loja inativos, "Sem estoque" ou "Disponível novamente", quando a quantidade foi reduzida a zero e o estoque voltou, caso em que o cliente precisa aumentar a quantidade; esses itens ficam com a seleção desabilitada, e a tela informa quantos itens não entram no pedido. A região lateral apresenta o resumo, com os itens selecionados, o subtotal, os descontos e o total; quando há itens de mais de uma loja, o resumo lista o valor por loja e informa que será gerado um pedido para cada uma. Abaixo, encontram-se o texto de retirada na feira, o botão "Finalizar pedido" e o *link* "Continuar comprando". Quanto às decisões técnicas, os totais exibidos são calculados no navegador, mas o *backend* recalcula todos os valores com o preço vigente na finalização (RNF10); somente os itens selecionados são enviados, e, após a finalização, o cliente é conduzido à página de pedidos. Como o *backend* guarda um carrinho por loja, a interface agrega esses carrinhos em uma única tela.

<!-- orientador: revisar -->
### 4.5.7 Favoritos

A tela de favoritos lista os produtos marcados pelo usuário autenticado, seja cliente ou produtor. Atende ao requisito RF21. A Figura 23 apresenta a tela de favoritos.

**Figura 23** - Favoritos

[INSERIR IMAGEM: docs/telas/tela-11-favoritos.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 23, os produtos favoritados são apresentados do mais recente para o mais antigo, com o mesmo cartão utilizado no catálogo; o ícone de coração remove o favorito, e o cartão conduz ao detalhe do produto. Produtos inativos, sem estoque ou de loja inativa permanecem na lista com as indicações "Produto inativo", "Sem estoque" ou "Produto indisponível". Quando a lista está vazia, a tela apresenta a mensagem "Nenhum favorito ainda" e o botão "Explorar produtos". Quanto às decisões técnicas, a lista é carregada uma vez por sessão, aproveitando a consulta já realizada pelo cabeçalho para o contador, e a compra de um favorito ocorre sempre pela página de detalhe, que bloqueia o que não está disponível.

<!-- orientador: revisar -->
### 4.5.8 Meus Pedidos

A página "Meus pedidos" permite ao comprador acompanhar os pedidos que realizou e executar as ações permitidas em cada um. Atende aos requisitos RF18, RF22 e RF24. A Figura 24 apresenta a página de pedidos.

**Figura 24** - Meus pedidos

[INSERIR IMAGEM: docs/telas/tela-12-pedidos.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 24, o topo apresenta o texto de retirada na feira e o filtro por status, com a opção "Todos" e os cinco status, cada um com a respectiva contagem. Os pedidos são listados do mais recente para o mais antigo; cada pedido apresenta o número, a data, a loja, o selo de status, a tabela de itens, com produto, quantidade e subtotal, e o resumo de valores, com o valor bruto, o desconto e o total. Conforme o status, são oferecidas as ações "Cancelar pedido", somente para pedidos Pendente, e "Confirmar recebimento", somente para pedidos Pronto para retirada. A Figura 25 apresenta a janela de confirmação de recebimento.

**Figura 25** - Janela de confirmação de recebimento

[INSERIR IMAGEM: docs/telas/tela-15-pedidos-confirmar-recebimento.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 25, a janela informa que o pedido passará ao status Entregue e que a ação não pode ser desfeita, com os botões "Confirmar recebimento" e "Voltar". Após a confirmação, os itens do pedido passam a exibir o botão "Avaliar". A Figura 26 apresenta a janela de avaliação de produto.

**Figura 26** - Janela de avaliação de produto

[INSERIR IMAGEM: docs/telas/tela-13-pedidos-avaliar.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 26, a janela apresenta a seleção da nota, de uma a cinco estrelas e obrigatória, o campo de comentário opcional, limitado a quinhentos caracteres, e o aviso de que a avaliação não poderá ser editada nem removida. Os itens já avaliados exibem as estrelas atribuídas, a indicação "Avaliado" e o *link* "Ver no produto", e os itens cujo produto foi excluído exibem a indicação "Produto não está mais disponível". Quanto às decisões técnicas, cada ação atualiza o pedido na lista com a resposta da API, sem recarregar a página, e o cancelamento informa ao cliente que os produtos voltam ao estoque e que o pedido permanece no histórico. O telefone do cliente não é exibido nesta página, e todas as regras são validadas pelo *backend*.

<!-- orientador: revisar -->
### 4.5.9 Perfil do Usuário

A página de perfil reúne os dados da conta de qualquer usuário autenticado. Atende aos requisitos RF04, RF05 e RF06. A Figura 27 apresenta a página de perfil.

**Figura 27** - Perfil do usuário

[INSERIR IMAGEM: docs/telas/tela-16-perfil.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 27, o primeiro bloco apresenta a foto de perfil ou as iniciais, com as opções de escolher, salvar, cancelar e remover a imagem, esta última mediante confirmação, além do nome, do e-mail e de um selo que indica o papel "Produtor rural" ou "Cliente". O segundo bloco trata da loja: para quem possui loja, apresenta um resumo e o botão "Gerenciar minha loja"; para o produtor sem loja, apresenta o convite "Gostaria de abrir uma loja?" com o botão "Criar minha loja"; e, para quem não é produtor, apresenta apenas a orientação de procurar a organização da feira para solicitar a habilitação, sem a opção de criar loja. O terceiro bloco apresenta as informações pessoais, com o botão "Editar" para alterar nome, e-mail, data de nascimento e gênero; o CPF é exibido somente para leitura. A Figura 28 apresenta o bloco de telefones.

**Figura 28** - Telefones do perfil

[INSERIR IMAGEM: docs/telas/tela-17-perfil-telefones.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 28, cada telefone é listado com seu tipo e, quando for o caso, com o selo "Principal", acompanhado das ações "Editar", "Definir como principal" e "Excluir"; o botão "Adicionar telefone" abre o formulário com o tipo e o número, com máscara. Quanto às decisões técnicas, a interface antecipa as regras da Seção 4.4.4: a exclusão é bloqueada, com texto explicativo, quando se trata do único telefone ou do telefone principal, e as contas sem telefone exibem um aviso solicitando o cadastro. Os erros de validação aparecem junto a cada campo, e as alterações bem-sucedidas atualizam imediatamente os dados da sessão, de modo que a foto exibida no menu da conta acompanha a troca.

<!-- orientador: revisar -->
### 4.5.10 Cadastro da Loja

A tela de cadastro da loja é destinada exclusivamente ao produtor que ainda não possui loja; o produtor que já possui loja é conduzido à sua área. Atende ao requisito RF09. A Figura 29 apresenta a tela de cadastro da loja.

**Figura 29** - Cadastro da loja

[INSERIR IMAGEM: docs/telas/tela-18-criar-loja.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 29, o formulário solicita o nome, a descrição e o CNPJ, com máscara e exigência de quatorze dígitos, além da imagem da loja, opcional, apresentada em uma prévia com a opção "Descartar escolha". Os botões "Cancelar" e "Criar loja" encerram o formulário. Quanto às decisões técnicas, o formulário é enviado como JSON quando não há imagem e no formato próprio para arquivos quando há; se a imagem for recusada, a loja não é criada, o arquivo é descartado da prévia e a mensagem é exibida no próprio campo. A regra de uma loja por produtor é validada pelo *backend*, conforme a Seção 3.2.5.2.3. Após o cadastro, o produtor recebe a notificação "Loja criada! Agora cadastre seus produtos." e é conduzido à área do produtor.

<!-- orientador: revisar -->
### 4.5.11 Área do Produtor e Painel

A área do produtor reúne as funcionalidades de gestão da loja e é acessível somente a usuários com papel de produtor. Atende aos requisitos RF15 e RF20. A Figura 30 apresenta o painel do produtor.

**Figura 30** - Painel do produtor

[INSERIR IMAGEM: docs/telas/tela-20-painel-produtor.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 30, a parte superior, comum a todas as abas da área, apresenta o título "Área do produtor", o nome da loja com o selo de loja ativa ou inativa, o botão "Novo produto" e cinco indicadores: produtos ativos, produtos inativos, pedidos pendentes, pedidos em andamento, que somam os pedidos Em preparo e Pronto para retirada, e vendas do mês. Abaixo, a navegação por abas dá acesso ao Painel, aos Pedidos, aos Produtos e à aba Minha loja. A aba Painel apresenta os cartões "Vendas do mês", "Pedidos no mês" e "Ticket médio", o gráfico de barras "Vendas dos últimos 7 dias" e a lista "Produtos mais vendidos", com os cinco primeiros por quantidade e o total em reais; um produto excluído aparece como "(produto removido)". Quanto às decisões técnicas, os indicadores são calculados no navegador a partir dos pedidos da loja, considerando somente os pedidos não cancelados, agrupados pela data de criação, e têm caráter exclusivamente informativo, sem substituir relatórios gerenciais. O acesso às rotas da área é verificado a cada navegação, e o produtor sem loja vê apenas o cartão "Você ainda não possui uma loja", com o botão "Criar minha loja".

<!-- orientador: revisar -->
### 4.5.12 Quadro de Pedidos do Produtor

O quadro de pedidos permite ao produtor acompanhar e atualizar os pedidos recebidos pela sua loja. Atende ao requisito RF19. O quadro segue o estilo *kanban*, método de organização visual do trabalho em colunas que representam as etapas de um processo (ANDERSON, 2010). A Figura 31 apresenta o quadro de pedidos do produtor.

**Figura 31** - Quadro de pedidos do produtor

[INSERIR IMAGEM: docs/telas/tela-21-pedidos-kanban.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 31, o quadro apresenta uma coluna para cada status, Pendente, Em preparo, Pronto para retirada e Entregue, e uma seção recolhível com os pedidos cancelados. Cada cartão apresenta o número e a data do pedido, o nome do cliente, o telefone do cliente, quando a API o envia, com *link* para ligação, os itens, o total e as ações permitidas: "Iniciar preparo" nos pedidos Pendente, "Marcar como pronto" nos pedidos Em preparo e "Confirmar entrega" nos pedidos Pronto para retirada, além da ação de cancelar nos pedidos Pendente e Em preparo, mediante confirmação. O botão "Atualizar pedidos" recarrega os dados da área. Quanto às decisões técnicas, a interface oferece somente o próximo passo do fluxo descrito na Seção 4.4.2, sem retorno de status, mas a validação das transições é feita pelo *backend*; o telefone é exibido apenas nos pedidos em aberto, conforme a Seção 4.4.7, e, após um cancelamento, a lista de produtos é recarregada, pois o estoque foi restaurado.

<!-- orientador: revisar -->
### 4.5.13 Produtos da Loja

A aba Produtos permite ao produtor cadastrar e manter os produtos, os preços e as imagens da sua loja. Atende aos requisitos RF11, RF12, RF13, RF14 e RF15. A Figura 32 apresenta a lista de produtos da loja.

**Figura 32** - Produtos da loja

[INSERIR IMAGEM: docs/telas/tela-23-produtos-loja.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 32, uma tabela ordenada por nome apresenta a miniatura, o nome, o SKU, a categoria, o estoque, o preço bruto, o desconto, o preço líquido e o status de cada produto, com as ações "Editar" e "Desativar" ou "Reativar". Filtros com contagem separam os produtos ativos e inativos, e um aviso resume os produtos ativos com estoque baixo ou sem estoque, que recebem os indicadores "Estoque baixo" ou "Sem estoque" e "Fora do catálogo". A desativação é confirmada em uma janela de diálogo, que informa que o produto deixará o catálogo e que os pedidos serão preservados, e a reativação é imediata. Os produtos não são excluídos: por decisão de projeto, a desativação substitui a exclusão, retirando o produto do catálogo sem desfazer seu vínculo com os itens de pedidos e com as avaliações e permitindo sua reativação posterior. A Figura 33 apresenta o formulário de cadastro de produto.

**Figura 33** - Formulário de cadastro de produto

[INSERIR IMAGEM: docs/telas/tela-24-produto-formulario-novo.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 33, o formulário lateral solicita o nome, a categoria, entre as categorias ativas, o estoque e a descrição; o bloco de imagens admite até cinco arquivos, cujas miniaturas permitem remover, mover para a esquerda ou para a direita, definir como principal e ajustar o enquadramento; e o bloco de preço solicita o preço de venda e o desconto em percentual, com a prévia do preço final ao cliente. Na edição, o campo de preço passa a indicar um novo preço de venda, que, se deixado em branco, mantém o preço atual, e é exibida a opção "Produto disponível para compra". A Figura 34 apresenta o editor de enquadramento da imagem.

**Figura 34** - Editor de enquadramento da imagem

[INSERIR IMAGEM: docs/telas/tela-26-produto-editor-enquadramento.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 34, o editor permite posicionar a área de recorte por arraste ou pelas setas do teclado, ajustar o zoom e centralizar a imagem, conforme descrito na Seção 4.4.3. Quanto às decisões técnicas, o salvamento ocorre em etapas: primeiro, o produto é criado ou alterado; em seguida, é registrado o preço, sempre no cadastro e, na edição, somente quando o preço ou o desconto mudam, o que preserva o histórico de preços; por fim, as imagens são sincronizadas, com a remoção das marcadas, o envio das novas, a definição da principal e a reordenação. Uma falha no envio das imagens não desfaz o cadastro do produto e é informada em um aviso. O SKU é gerado pelo *backend* e apenas exibido. Como a sugestão de categorias não possui interface (RF14), o produtor utiliza somente as categorias ativas já existentes.

<!-- orientador: revisar -->
### 4.5.14 Dados da Loja

A tela Dados da loja, acessada pela aba Minha loja, permite ao proprietário manter as informações da sua loja. Atende ao requisito RF10. A Figura 35 apresenta a tela de dados da loja.

**Figura 35** - Dados da loja

[INSERIR IMAGEM: docs/telas/tela-27-dados-loja.png]

Fonte: Confeccionado pelo autor (2026).

Na Figura 35, o primeiro bloco apresenta o nome, obrigatório, a descrição e o CNPJ, este somente para leitura, com os botões "Descartar alterações" e "Salvar alterações", habilitados apenas quando há mudanças. O segundo bloco permite escolher, trocar, salvar e remover a imagem da loja, esta última mediante confirmação. O terceiro bloco apresenta o botão "Ver minha vitrine", que conduz à página pública da loja, ainda não construída (Seção 5.1). O quarto bloco apresenta a situação da loja e o botão "Desativar loja", mediante confirmação; com a loja inativa, a tela informa que ela não aceita novas compras. Quanto às decisões técnicas, a desativação preserva os produtos e os pedidos, e a loja inativa continua editável pelo proprietário, inclusive quanto à imagem, que não é apagada pela desativação.

<!-- orientador: revisar -->
## 4.6 Implantação

O Agro Store foi preparado para dois ambientes de execução: o de desenvolvimento, utilizado na construção e nos testes do sistema, e o de produção, no qual a plataforma é disponibilizada aos usuários. A diferença entre os ambientes é controlada exclusivamente por variáveis de ambiente, de modo que o mesmo código é executado nos dois casos e nenhuma credencial é registrada no código-fonte (RNF14). Em desenvolvimento, as variáveis são lidas de um arquivo local, criado a partir de um modelo versionado que contém apenas nomes e valores de exemplo. O Quadro 12 apresenta a configuração de cada componente nos dois ambientes.

**Quadro 12** - Configuração dos ambientes de desenvolvimento e produção

| Componente | Desenvolvimento | Produção |
| --- | --- | --- |
| Interface web | Servidor local do Vite, que encaminha as requisições de /api e /media ao *backend* | Vercel, configurada como aplicação de página única, com reescrita das rotas para a página inicial e endereço da API definido nas variáveis VITE_API_URL e VITE_BACKEND_URL |
| API | Servidor de desenvolvimento do Django, executado localmente | Render |
| Banco de dados | SQLite, quando a variável DATABASE_URL está vazia | PostgreSQL hospedado no Supabase, definido pela variável DATABASE_URL |
| Arquivos de imagem | Disco local do *backend* | Supabase Storage, definido pelas variáveis do armazenamento |
| E-mail | Exibição das mensagens no console do servidor | Servidor SMTP, definido pelas variáveis de e-mail |
| Configuração | Arquivo local criado a partir do modelo versionado | Variáveis de ambiente de cada serviço |

Fonte: Confeccionado pelo autor (2026).

Em desenvolvimento, um único comando inicia a API e a interface em conjunto. Como o servidor da interface encaminha ao *backend* as requisições da API e dos arquivos de mídia, a aplicação é acessada por uma única origem, sem depender de um endereço fixo da API. Em produção, a interface publicada na Vercel é configurada para que qualquer rota da aplicação seja atendida pela página inicial, uma vez que a navegação entre as telas é feita no navegador; o endereço da API é informado à interface pelas variáveis de ambiente. O *backend* executado no Render conecta-se ao PostgreSQL do Supabase e grava as imagens no Supabase Storage. As origens autorizadas a chamar a API são definidas por uma variável de CORS (*Cross-Origin Resource Sharing*), mecanismo pelo qual o navegador permite que uma página consuma uma API publicada em outro endereço. Outras variáveis definem o endereço da interface, utilizado no *link* do e-mail de redefinição de senha, e a quantidade de *proxies* reversos à frente do *backend*, necessária para que o limite de requisições considere o endereço real do usuário.

<!-- orientador: revisar -->
A estrutura do banco de dados é criada e atualizada por meio das migrações do Django, arquivos que descrevem, em ordem, as alterações a serem aplicadas ao esquema do banco de dados a cada evolução das classes de modelo (DJANGO SOFTWARE FOUNDATION, 2026a). Ao longo do desenvolvimento, foram acumuladas trinta e sete migrações nas sete aplicações de domínio do *backend*: usuarios, lojas, produtos, carrinhos, pedidos, favoritos e avaliacoes. Parte delas alterava dados já existentes, como a transferência do vínculo do cliente para a entidade Pedido_Cliente, a reorganização dos telefones, descrita na Seção 4.4.4, e a cópia da imagem registrada no antigo campo de imagem do produto para a entidade Imagem. Essas migrações de dados foram separadas das que alteravam a estrutura, por compatibilidade com o PostgreSQL, e algumas possuíam verificações que interrompiam a aplicação caso encontrassem dados incompatíveis.

<!-- orientador: revisar -->
Concluída essa evolução, o histórico foi consolidado, isto é, as migrações de cada aplicação foram substituídas por uma única migração inicial, gerada a partir das classes de modelo vigentes, que cria diretamente o mesmo esquema produzido pelo histórico anterior, sem alterá-lo. Os dados fixos dos quais o sistema depende, a saber, as opções de gênero padrão (M Masculino, F Feminino e I Prefiro não informar) e os tipos de telefone (Celular, Fixo e Comercial), passaram a ser carregados por uma única migração de dados iniciais. Essa migração é idempotente, ou seja, sua execução repetida produz o mesmo resultado, sem duplicar registros, e renomeia a opção de código I de "Indefinido" para "Prefiro não informar" somente quando o nome ainda corresponde ao anterior, preservando eventuais renomeações realizadas pelo administrador, conforme descrito na Seção 3.2.3. As migrações de transição foram removidas junto com o histórico, pois já haviam cumprido o seu papel: os bancos de dados que passaram por elas mantêm os dados transferidos, e uma nova instalação passa a ser criada diretamente no esquema final, em menos etapas e sem depender de transformações de dados que não se aplicam a um banco vazio.

<!-- orientador: revisar -->
Após a consolidação, os bancos de dados locais de desenvolvimento, em SQLite e em PostgreSQL executado em contêiner, isto é, em um ambiente de execução isolado do restante do sistema operacional, foram recriados a partir do esquema consolidado e recarregados com os dados de uma cópia de segurança do banco de dados de produção, datada de 6 de novembro de 2026. A conferência da quantidade de registros de cada tabela não apontou diferenças, e a comparação estrutural do esquema apontou somente diferenças nos nomes de restrições e de sequências gerados automaticamente, sendo as sequências os objetos do PostgreSQL que fornecem os valores das chaves primárias. O banco de dados de produção, hospedado no Supabase, não foi recriado. Como o Django registra no próprio banco de dados as migrações já aplicadas, esse registro precisa ser conciliado com o histórico consolidado, procedimento planejado como etapa posterior que exige cópia de segurança prévia e é tratado como procedimento controlado, cujo estado é discutido na Seção 5.1.

<!-- orientador: revisar -->
## 4.7 Testes e Verificação

As regras de negócio descritas neste capítulo foram verificadas por meio de testes automatizados do *backend*, que simulam as requisições à API e conferem as respostas e os dados gravados no banco de dados. Após a consolidação das migrações descrita na Seção 4.6, a suíte completa, executada com o comando `python manage.py test` na pasta do *backend*, reunia 399 testes automatizados, todos aprovados, sem falhas nem erros, tanto com o banco de dados SQLite quanto com o PostgreSQL. Entre eles, quatro testes verificam a migração de dados iniciais: a existência dos gêneros e dos tipos de telefone padrão no banco de dados migrado, a ausência de registros duplicados quando a carga é executada novamente, a renomeação da opção "Indefinido" para "Prefiro não informar" e a preservação de um nome de gênero alterado pelo administrador. Os testes que verificavam as migrações de transição, como a cópia dos telefones antigos e a migração das imagens dos produtos, foram removidos junto com essas migrações. O Quadro 13 apresenta a distribuição dos testes por área.

<!-- autor: informar a data da execução da suíte de 399 testes e, se desejar, o tempo de execução em cada banco de dados -->

<!-- orientador: revisar -->
**Quadro 13** - Testes automatizados do backend por área

| Área | O que é verificado | Nº de testes |
| --- | --- | --- |
| Cadastro e perfil | Cadastro público de cliente (CPF, e-mail, idade mínima, senha, sem campos de privilégio, retorno dos tokens JWT) e atualização do perfil sem alterar CPF e papéis | 14 |
| Gêneros (RN-024) | Consulta pública das opções, ordem de exibição, recusa de código inexistente, vazio ou nulo no cadastro e no perfil e aceitação de opções criadas pelo administrador | 12 |
| Foto de perfil (RN-018) | Envio, troca e remoção; validação de formato, tamanho e conteúdo; foto não exposta a terceiros | 20 |
| Redefinição de senha (RN-020) | Resposta neutra, token armazenado como *hash*, validade de 30 minutos, uso único, invalidação de *links* anteriores, limite por origem e conta inativa | 32 |
| Telefones (RN-021) | Tipos, validação de dígitos por tipo, principal único, mínimo de um telefone, conta legada, área administrativa, listagem dos telefones fora do padrão e existência dos tipos padrão | 72 |
| Lojas e imagem da loja | Uma loja por produtor (RN-013), edição somente pelo proprietário e imagem da loja (RN-018) | 42 |
| Produtos: categorias e permissões | Categoria única e ativa, sugestão pelo produtor, regras do administrador e cadastro somente por produtor | 23 |
| Produtos: estoque (RN-017) | Estoque não negativo, produto com estoque zerado fora do catálogo e estoque baixo | 15 |
| Produtos: imagens (RN-016) | Limite de cinco imagens, imagem principal única, ordem e validação de arquivo | 19 |
| Carrinho | Adição, soma de quantidade, remoção, quantidade inválida, produto ou loja inativos, estoque e isolamento entre usuários | 24 |
| Pedidos: finalização, status, visibilidade e integridade (RN-011, RN-019, RN-022) | Um pedido por loja, *snapshots*, inclusive do nome do gênero vigente na compra, restrições do banco de dados sobre a quantidade e os valores dos itens, baixa e restauração de estoque, ajuste dos carrinhos de outros clientes, fluxo de status, cancelamento, confirmação de recebimento, visibilidade por perfil, bloqueio de exclusão com pedidos e item preservado com produto excluído | 66 |
| Telefone do cliente nos pedidos (RN-021) | O produtor vê o telefone somente nos pedidos em aberto, telefone fora do *snapshot* e conta sem telefone | 12 |
| Favoritos | Favoritar sem duplicar, vínculo ao usuário autenticado e listagem | 8 |
| Avaliações (RN-010) | Somente o dono do pedido avalia, somente pedido Entregue, uma por item, nota de 1 a 5, comentário de até 500 caracteres, nome abreviado e produto excluído | 26 |
| Migração de dados iniciais | Carga dos gêneros e dos tipos de telefone padrão, ausência de duplicidade na reexecução, renomeação da opção "Indefinido" e preservação do nome alterado pelo administrador | 4 |
| Esquema do banco de dados | Aderência ao modelo lógico (docs/modelo-logico.sql) | 10 |
| Total | — | 399 |

Fonte: Confeccionado pelo autor (2026).

A autenticação por JWT é verificada principalmente de forma indireta, por meio dos testes de autenticação e permissões dos demais endpoints, que conferem a recusa das requisições sem token ou de usuários sem permissão. Não há testes automatizados da interface: a verificação do *frontend* foi realizada manualmente no navegador e pela geração da versão de produção da interface. Complementarmente, as telas relacionadas ao controle de estoque foram inspecionadas visualmente nas larguras de 375 e 1280 pixels, representativas de *smartphones* e de computadores de mesa, respectivamente, em atenção ao requisito de responsividade (RNF05).

<!-- orientador: revisar -->
Além dos testes automatizados, o fluxo de redefinição de senha foi validado manualmente em ambiente real em 16 de outubro de 2026. Nessa validação, o *backend* foi executado com o banco de dados PostgreSQL hospedado no Supabase e com envio efetivo de e-mails por meio do servidor SMTP do Gmail, na porta 587 e com criptografia TLS (*Transport Layer Security*), protocolo que protege a comunicação entre a aplicação e o servidor de e-mail (RESCORLA, 2018), configurado por variáveis de ambiente; o *frontend* foi executado localmente. A solicitação de redefinição obteve a resposta neutra prevista, com código HTTP 200, que indica sucesso no processamento da requisição (FIELDING; NOTTINGHAM; RESCHKE, 2022), e gerou um registro de redefinição com expiração exatamente trinta minutos após sua criação e data de utilização ainda não preenchida. Verificou-se também que a nova solicitação invalidou uma solicitação anterior da mesma conta, conforme a regra descrita na Seção 4.4.8. O e-mail foi recebido na caixa de entrada do destinatário e, a partir do *link* recebido, a nova senha foi cadastrada com sucesso pela tela de redefinição. A recusa de um *link* já utilizado e o acesso com a nova senha não foram repetidos manualmente nessa validação, permanecendo verificados pelos testes automatizados do *backend*.

<!-- autor: registrar aqui, se desejar, as validações manuais das telas no navegador (avaliações, foto de perfil, imagem da loja, recuperação de senha); não há testes de usabilidade com usuários a relatar -->

<!-- orientador: revisar -->
# 5 CONSIDERAÇÕES FINAIS

Este trabalho teve como objetivo geral desenvolver uma plataforma digital para intermediar pedidos entre consumidores e produtores rurais da Feira do Produtor Rural Willi Dummer, em Camaquã/RS, com cadastro de produtos, realização de pedidos e acompanhamento do status de cada venda, perfis distintos para produtor, cliente e administrador e retirada dos pedidos na própria feira. Esse objetivo foi alcançado com a entrega de um MVP funcional, composto por uma API REST em Django REST Framework e por uma interface web em Vue.js, cujas funcionalidades foram descritas no Capítulo 4.

Os objetivos específicos foram cumpridos da seguinte forma. A pesquisa bibliográfica sobre agricultura familiar, feiras de produtores rurais, plataformas digitais B2C e tecnologias de desenvolvimento web foi apresentada no Capítulo 2. O levantamento dos requisitos, descrito na Seção 3.1, resultou em vinte e quatro requisitos funcionais e dezesseis requisitos não funcionais, apresentados nos Quadros 1 e 2. A modelagem do banco de dados, com o diagrama entidade-relacionamento e o modelo lógico, foi apresentada nas Seções 3.2.2 a 3.2.4, com dezoito entidades. Os diagramas UML de casos de uso, de sequência e de atividades foram apresentados na Seção 3.2.5 e complementados, na Seção 4.4, pelo diagrama de estados do pedido e por três diagramas de sequência adicionais. A API REST foi desenvolvida conforme as Seções 4.1, 4.3 e 4.4, com cinquenta e nove combinações de método e endereço, e o *frontend*, com as interfaces para os usuários, foi apresentado na Seção 4.5.

O Quadro 14 relaciona cada requisito funcional à forma como foi atendido e à seção em que é descrito.

**Quadro 14** - Conformidade dos requisitos funcionais

| Requisito | Como foi atendido | Seção |
| --- | --- | --- |
| RF01 | Endpoint público de cadastro, com validações no *backend*, telefone principal e retorno dos tokens; aba "Criar conta" | 3.2.5.2.1; 4.5.2 |
| RF02 | Login por CPF e senha com tokens JWT e renovação automática pelo módulo de comunicação da interface | 3.2.5.2.2; 4.1; 4.5.1 |
| RF03 | Fluxo de solicitação e confirmação por *link* de uso único, com resposta neutra e limites por origem | 4.4.8; 4.5.3 |
| RF04 | Edição do perfil com as validações do cadastro; CPF e papéis protegidos; *snapshot* preservado nos pedidos | 4.4.7; 4.5.9 |
| RF05 | Foto de perfil opcional, visível só ao usuário, com validação de arquivo | 4.4.4; 4.5.9 |
| RF06 | Entidades Telefone e Tipo_Telefone, validação por tipo e principal único, gerenciados no perfil | 4.4.4; 4.5.9 |
| RF07 | Listagem pública de produtos disponíveis, com filtro, busca, ordenação e paginação na interface | 3.2.5.2.5; 4.5.4 |
| RF08 | Página de detalhe com galeria, loja, preço, disponibilidade e avaliações | 4.5.5 |
| RF09 | Cadastro de loja por produtor, com unicidade garantida na API e no banco | 3.2.5.2.3; 4.5.10 |
| RF10 | Edição, imagem e desativação da loja pelo proprietário, sem exclusão | 4.4.7; 4.5.14 |
| RF11 | Cadastro, edição, desativação e reativação de produtos, com SKU automático | 3.2.5.2.4; 4.5.13 |
| RF12 | Registro de preços com encerramento automático da vigência anterior | 3.2.5.2.4; 4.5.13 |
| RF13 | Até cinco imagens por produto, imagem principal única e editor de enquadramento | 4.4.3; 4.5.13 |
| RF14 | Listagem de categorias ativas na interface; sugestão e gestão disponíveis somente pela API, sem interface no MVP | 4.3; 5.1 |
| RF15 | Retirada do catálogo dos produtos sem estoque e indicador de estoque baixo | 4.4.1; 4.5.13 |
| RF16 | Carrinho persistido no servidor, com limite de estoque e ajuste automático | 4.4.1; 4.5.6 |
| RF17 | Finalização transacional com um pedido por loja, *snapshot*, baixa de estoque e ajuste de carrinhos | 3.2.5.3.1; 4.4.2 |
| RF18 | Página "Meus pedidos" com filtro, cancelamento e confirmação de recebimento | 4.4.2; 4.5.8 |
| RF19 | Quadro *kanban* com avanço e cancelamento conforme o fluxo e telefone apenas nos pedidos em aberto | 4.4.2; 4.5.12 |
| RF20 | Painel com indicadores calculados na interface a partir dos pedidos não cancelados | 4.5.11 |
| RF21 | Favoritos privados, sem duplicidade, inclusive para produtores | 4.4.5; 4.5.7 |
| RF22 | Avaliação por item de pedido entregue, pública e com nome abreviado | 4.4.6; 4.5.5; 4.5.8 |
| RF23 | Área administrativa do Django para moderação, consulta de pedidos, telefones, desativação de usuários e concessão do papel de produtor | 3.2.5.1; 4.4.6; 4.4.7 |
| RF24 | Informação fixa de retirada exibida no catálogo, no carrinho, no detalhe do produto e nos pedidos | 4.4.2; 4.5.4; 4.5.6 |

Fonte: Confeccionado pelo autor (2026).

O Quadro 15 apresenta a mesma relação para os requisitos não funcionais.

**Quadro 15** - Conformidade dos requisitos não funcionais

| Requisito | Como foi atendido | Seção |
| --- | --- | --- |
| RNF01 | API REST com JSON sob o prefixo /api/v1/ | 4.3 |
| RNF02 | Autenticação JWT com validades de 120 minutos e de um dia e permissão padrão restritiva | 4.1 |
| RNF03 | Permissões por perfil e consultas limitadas aos recursos do usuário | 4.1; 4.3 |
| RNF04 | Monorepo com SPA e API independentes, comunicando-se por HTTP | 4.1 |
| RNF05 | Interface responsiva com Bootstrap; inspeção visual restrita às telas de estoque | 4.5; 4.7 |
| RNF06 | Mecanismo de senhas padrão do Django com PBKDF2 e validadores | 4.4.8 |
| RNF07 | Restrições de unicidade e chaves estrangeiras no banco, complementadas pela API | 3.2.4 |
| RNF08 | Exclusão restritiva, *snapshot* e desativação no lugar da exclusão | 4.4.7 |
| RNF09 | Transações com bloqueio de linhas; verificação no PostgreSQL de produção pendente | 4.4.1; 5.1 |
| RNF10 | Validação final de todas as regras críticas no *backend* | 4; 4.5 |
| RNF11 | *Hash* SHA-256 do código, limites por origem e código no fragmento do endereço | 4.4.8 |
| RNF12 | Telefone fora do *snapshot*, nome abreviado e foto restrita ao usuário | 4.4.4; 4.4.7 |
| RNF13 | Validação de formato, tamanho e conteúdo, nome aleatório e armazenamento no Supabase Storage | 4.4.3; 4.4.4 |
| RNF14 | Variáveis de ambiente, SQLite em desenvolvimento e PostgreSQL em produção | 4.6 |
| RNF15 | Aplicações de domínio independentes no *backend* | 4.1 |
| RNF16 | Mensagens da API e da interface em português do Brasil | 4.3 |

Fonte: Confeccionado pelo autor (2026).

Do ponto de vista técnico, destacam-se as decisões que asseguram a consistência dos dados em um ambiente com vários usuários: a validação das regras no servidor, o controle de concorrência na baixa de estoque, a separação dos pedidos por loja e a preservação do histórico por meio de *snapshots* e de exclusão restritiva. Do ponto de vista do contexto da feira, a plataforma permite que os produtores divulguem seus produtos e organizem antecipadamente os pedidos, mantendo a retirada presencial, que preserva a dinâmica existente. As limitações identificadas e as possibilidades de evolução são apresentadas nas seções a seguir.

<!-- orientador: revisar -->
## 5.1 Limitações

O escopo do MVP não contempla pagamento online, entrega em domicílio nem cálculo de frete: o pedido é uma reserva para retirada presencial, e o pagamento ocorre fora da plataforma. Da mesma forma, o dia, o horário e o local da feira são uma informação fixa da interface, que não pode ser alterada pelo administrador e não restringe a criação de pedidos com base nesse período.

O controle de estoque implementado atende às necessidades do MVP, mas apresenta limitações que podem orientar trabalhos futuros, no âmbito de um controle de estoque mais avançado. A sinalização de estoque baixo é apenas visual e depende do acesso do produtor à plataforma. O limite de cinco unidades é único para todos os produtos e poderia passar a ser configurável por produto, considerando as diferentes unidades de venda e o giro de cada item. Quando a quantidade de um item do carrinho é reduzida sem chegar a zero, o cliente não recebe um aviso específico. Esse aviso exigiria armazenar a quantidade escolhida originalmente.

No ciclo de pedidos, o cancelamento não registra uma justificativa, e o cliente não é notificado ativamente quando o produtor altera o status ou cancela um pedido; a informação fica disponível apenas na página de pedidos. O sistema também não mantém um histórico das mudanças de status: o pedido registra somente o seu status atual, sem identificar o autor de cada alteração nem o momento em que ela ocorreu. Por essa razão, quando um pedido chega ao status Entregue, não é possível saber se a retirada foi registrada pelo produtor ou confirmada pelo cliente. Além disso, como Entregue é um estado final, uma confirmação de recebimento feita por engano, pelo cliente ou pelo produtor, não pode ser revertida pela plataforma.

Nas avaliações, não há edição pelo autor: uma avaliação enviada só pode ser removida pelo administrador, como moderação. Além disso, embora as avaliações de produtos desativados ou de lojas desativadas continuem disponíveis na API, elas não são exibidas na interface, pois a página de detalhe desses produtos deixa de ficar acessível.

Quanto aos dados pessoais, a preservação do histórico impede a exclusão de usuários que possuam pedidos, e o *snapshot* mantém dados como nome, CPF, e-mail, data de nascimento e gênero registrados em cada pedido. O telefone, por decisão de projeto descrita na Seção 4.4.7, não é copiado para o pedido e é exibido ao produtor apenas nos pedidos em aberto, o que reduz a exposição desse dado, mas não resolve a questão para os demais dados preservados. O sistema ainda não dispõe de um procedimento de anonimização desses dados, que seria necessário para atender a solicitações de eliminação de dados pessoais previstas na LGPD (BRASIL, 2018, art. 18, VI) sem comprometer a integridade do histórico de vendas.

Quanto aos telefones, descritos na Seção 4.4.4, a validação considera apenas a quantidade de dígitos de acordo com o tipo, sem verificar se o DDD corresponde a um código de área existente nem se o número de celular inicia pelo nono dígito, de modo que números com formato válido, mas inexistentes, são aceitos. A exigência de ao menos um telefone por usuário é garantida pela API e pela área administrativa, e não por uma restrição do banco de dados, o que admite as contas sem telefone mencionadas na Seção 4.4.4; nos pedidos dessas contas, o produtor não dispõe de um telefone para contato. Como o telefone não integra o *snapshot*, o pedido não registra o número utilizado no momento da compra, e os telefones migrados com formato fora do padrão dependem de correção manual. Por fim, o telefone do produtor não é exibido ao cliente, e a forma de contato com a loja ainda não foi definida.

Na redefinição de senha, descrita na Seção 4.4.8, as sessões já abertas antes da troca não são encerradas: os tokens JWT emitidos anteriormente continuam válidos até expirarem pelo prazo normal, de até cento e vinte minutos para o token de acesso e de um dia para o token de renovação. Assim, se a senha tiver sido redefinida por suspeita de acesso indevido, uma sessão já aberta por terceiros não é interrompida de imediato. Além disso, o usuário não recebe um aviso por e-mail informando que a senha foi alterada; o envio do e-mail de redefinição ocorre durante o próprio processamento da solicitação, o que pode aumentar o tempo de resposta quando o servidor de e-mail estiver lento e tornar a resposta de um e-mail cadastrado mais demorada que a de um e-mail inexistente; e os registros de solicitações expiradas ou já utilizadas não são removidos periodicamente. O limite de requisições por origem é mantido na memória de cada processo do servidor, de modo que, com mais de um processo, cada um conta separadamente, e a contagem é reiniciada quando o servidor é reiniciado.

Quanto às imagens descritas na Seção 4.4.4, a página pública da loja ainda não foi construída: o endereço correspondente exibe apenas a mensagem "Em breve", embora seja acessado pelo nome da loja na página de pedidos e pelo botão "Ver minha vitrine". Quando existir, a imagem da loja também será exibida nela. Além disso, a versão atual apresenta três limitações. Primeiro, embora a foto de perfil seja exibida apenas ao próprio usuário na interface, o arquivo fica acessível a quem conhecer o seu endereço; o nome gerado aleatoriamente torna esse endereço difícil de descobrir, mas não constitui um controle de acesso. Segundo, como o arquivo é gravado no armazenamento antes da confirmação da transação no banco de dados, uma falha nessa gravação pode deixar um arquivo sem referência no armazenamento, denominado arquivo órfão, que ocupa espaço sem ser utilizado; situação semelhante ocorre quando a remoção do arquivo anterior falha, caso em que o erro é apenas registrado no servidor. Terceiro, a troca dessas imagens pela área administrativa não aplica as mesmas validações de formato e de tamanho adotadas no envio pelo usuário.

Algumas funcionalidades disponíveis na API ainda não possuem interface. A sugestão de categorias pelo produtor e a gestão de categorias pelo administrador são realizadas somente pela API (RF14), e a tela de dados da loja não oferece a reativação de uma loja desativada, embora a API a permita. A habilitação de produtores depende do contato presencial com a organização da feira e da concessão manual do papel pelo administrador, sem solicitação pelo sistema.

A API também apresenta limitações de validação e de contrato identificadas durante a documentação. O CNPJ é verificado quanto à unicidade e ao tamanho, mas não quanto aos dígitos verificadores. Algumas rotas respondem com erro interno do servidor, em vez de uma mensagem de validação, quando recebem identificadores não numéricos, como a atualização de itens do carrinho e de status de pedidos, e quando o status do pedido é informado por nome, e não por seu identificador. A listagem de avaliações é pública, mas a consulta individual de uma avaliação exige autenticação, embora apresente o mesmo conteúdo. As listagens não são paginadas, o que pode afetar o desempenho com grandes volumes de dados.

<!-- orientador: revisar -->
Quanto ao banco de dados, o banco implementado ainda não reproduz todas as restrições de integridade do modelo lógico apresentado na Seção 3.2.4: as ações de exclusão restritiva de quatro relações, as restrições de verificação de estoque, de preço, dos valores do carrinho e do pedido, de nota e de comentário, a unicidade da ordem das imagens, os nomes de quatro restrições e a obrigatoriedade das colunas sku e codigo_barras, uma vez que, no banco implementado, a primeira aceita valor nulo e a segunda é obrigatória, ao contrário do modelo-alvo. Essas regras são garantidas hoje pela camada de aplicação. Entre as restrições de verificação de valores, somente as dos itens de pedido já existem no banco de dados: quantidade positiva e valor unitário, valor do desconto e subtotal não negativos. Além disso, o desenvolvimento foi realizado predominantemente com o banco de dados SQLite; após a consolidação das migrações descrita na Seção 4.6, a suíte de testes automatizados foi executada também com o PostgreSQL, em ambiente local. A consolidação foi validada nos bancos de dados locais, recriados a partir do esquema consolidado e recarregados com os dados de uma cópia de segurança da produção, datada de 6 de novembro de 2026. Nessa cópia, todas as migrações anteriores à consolidação estavam aplicadas, exceto a antiga normalização das opções de gênero, e a comparação estrutural com o esquema consolidado não apontou diferenças além dos nomes de restrições e de sequências gerados automaticamente. Conforme essa cópia, o esquema do banco de dados de produção, hospedado no Supabase, é equivalente ao consolidado; esse banco, porém, não foi recriado e mantém o registro das migrações aplicadas segundo o histórico anterior. Resta apenas conciliar esse registro com o histórico consolidado, etapa planejada e ainda não executada até a redação desta seção. Como a normalização do gênero não chegou a ser aplicada em produção, a opção de código I ainda se chama "Indefinido" nesse banco e deverá ser renomeada para "Prefiro não informar" pela migração de dados iniciais, descrita na Seção 4.6, no momento da conciliação. Por fim, o comportamento do bloqueio por linha descrito na Seção 4.4.1 ainda precisa ser verificado no PostgreSQL de produção, e não há testes automatizados da interface.

<!-- autor: após a conciliação do registro de migrations no Supabase (DB-023), atualizar o parágrafo acima com a data e o resultado; até lá, manter a conciliação como etapa planejada -->
<!-- orientador: revisar o parágrafo acima, atualizado após a consolidação das migrations (DB-022) -->

<!-- orientador: revisar -->
## 5.2 Trabalhos Futuros

A partir das limitações identificadas e do escopo definido para o MVP, as seguintes evoluções podem ser exploradas em trabalhos futuros:

- Fluxo de habilitação de produtores, no qual o usuário solicitaria o papel de produtor e a criação de sua loja pelo próprio sistema, e o administrador aprovaria a solicitação. No MVP, o papel de produtor é concedido pelo administrador após contato presencial com a organização da feira;

- Interface para a sugestão de categorias pelo produtor e para a gestão de categorias pelo administrador, hoje disponíveis somente pela API, e para a reativação de lojas;

- Edição, pelo administrador, do dia, do horário e do local de retirada da feira, hoje fixos na interface;

- Agrupamento, em uma única compra, dos pedidos gerados para diferentes lojas em uma mesma finalização, permitindo ao cliente consultar a compra como um todo, e padronização do carrinho em um único carrinho por cliente;

- Histórico das mudanças de status de cada pedido, com o registro de quem realizou cada alteração e de quando ela ocorreu, o que permitiria identificar, entre outras informações, se a entrega foi registrada pelo produtor ou confirmada pelo cliente e a data da retirada;

- Página pública da loja, com a apresentação da loja, de sua imagem e de seus produtos, acessível também a partir do nome da loja na página de detalhe do produto;

- Moderação, pelo administrador, das imagens das lojas e das fotos de perfil, com as mesmas validações aplicadas ao envio pelo usuário, e separação da imagem da loja em logotipo e imagem de capa;

- Edição das avaliações pelo autor e exibição das avaliações de produtos desativados;

- Procedimento de anonimização de dados pessoais, em conformidade com a LGPD;

- Validação mais rigorosa dos dados, com a verificação dos dígitos verificadores do CNPJ e do DDD e do nono dígito dos números de celular, e tratamento padronizado de identificadores inválidos nas rotas da API;

- Definição dos dados de contato e da cidade da loja, permitindo ao cliente contatar o produtor, uma vez que, no MVP, o telefone do produtor não é exibido ao cliente;

- Evoluções da segurança da conta: envio assíncrono do e-mail de redefinição de senha, isto é, realizado em segundo plano, sem que a resposta ao usuário dependa da conclusão do envio; encerramento imediato das sessões JWT abertas após a troca de senha; envio de um e-mail de aviso informando que a senha foi alterada; troca de senha pela página de perfil, mediante a informação da senha atual; remoção periódica dos registros de redefinição expirados ou já utilizados; e limite de requisições compartilhado entre os processos do servidor;

<!-- orientador: revisar -->
- Alinhamento do banco de dados implementado ao modelo lógico, levando para o banco as restrições hoje garantidas pela camada de aplicação, o que exige verificar antes os dados que violariam cada restrição;

- Verificação do controle de concorrência no PostgreSQL do ambiente de produção e criação de testes automatizados da interface;

- Paginação das listagens da API;

- Pagamento online e integração com meios de pagamento;

- Entrega em domicílio, como alternativa à retirada na feira;

- Notificações ativas, por e-mail ou notificação *push*, para mudanças de status dos pedidos e para o estoque baixo;

- Controle avançado de estoque, com limite de estoque baixo configurável por produto;

- Aplicativo para dispositivos móveis, para o qual já foi elaborado um guia visual preliminar que reproduz as cores e os componentes da interface web, além de relatórios avançados de vendas e de comunicação direta entre cliente e produtor por meio de *chat*.

# 6 CRONOGRAMA

<!-- orientador: revisar -->
O Quadro 16 apresenta o cronograma das atividades do trabalho, realizadas de fevereiro a outubro de 2026, com as atividades finais previstas para os meses seguintes:

1.  Construção da Proposta de TCC;

2.  Pesquisa Bibliográfica para levantamento de sistemas semelhantes, bem como construção do referencial teórico;

3.  Levantamento dos requisitos funcionais e não-funcionais;

4.  Construção dos diagramas;

5.  Modelagem do banco de dados;

6.  Seminário de andamento;

7.  Desenvolvimento dos códigos;

8.  Análise dos Resultados e Conclusão;

9.  Entrega e Defesa do TCC.

<!-- orientador: revisar -->
**Quadro 16** - Cronograma de atividades

| Atividades | FEV | MAR | ABR | MAI | JUN | JUL | AGO | SET | OUT | NOV | DEZ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | X | X | | | | | | | | | |
| 2 | | X | X | X | | | | | | | |
| 3 | | | X | X | X | | | | | | |
| 4 | | | X | X | X | | | | | | |
| 5 | | | | X | X | | | | | | |
| 6 | | | | | | X | | | | | |
| 7 | | | | | | | X | X | X | | |
| 8 | | | | | | | X | X | X | X | |
| 9 | | | | | | | | | | X | X |

Fonte: Confeccionado pelo autor (2026).

<!-- autor: o desenvolvimento (atividade 7) foi ajustado para agosto a outubro, conforme o realizado; conferir as demais marcações -->

**REFERÊNCIAS**

<!-- orientador: revisar -->
<!-- autor: conferir todas as referências, em especial a edição e o ano dos livros (ANDERSON, RIES, SILBERSCHATZ, STALLINGS) e as datas de acesso das páginas online -->

ANDERSON, David J. **Kanban**: successful evolutionary change for your technology business. Sequim: Blue Hole Press, 2010.

ANTUNES, M. **API RESTful**: conceito, princípios e como criar. 2019. Disponível em: https://www.hostgator.com.br/blog/api-restful. Acesso em: 11 abr. 2026.

BERNERS-LEE, T.; FIELDING, R.; MASINTER, L. **Uniform Resource Identifier (URI)**: generic syntax. RFC 3986. [S. l.]: IETF, jan. 2005. Disponível em: https://www.rfc-editor.org/rfc/rfc3986. Acesso em: 20 out. 2026.

BOOTSTRAP. **Bootstrap documentation**. [S. l.], 2026. Disponível em: https://getbootstrap.com/. Acesso em: 20 out. 2026.

BRASIL. Lei nº 11.326, de 24 de julho de 2006. Estabelece as diretrizes para a formulação da Política Nacional da Agricultura Familiar e Empreendimentos Familiares Rurais. **Diário Oficial da União**, Brasília, DF, 25 jul. 2006. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11326.htm. Acesso em: 06 abr. 2026.

BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). **Diário Oficial da União**, Brasília, DF, 15 ago. 2018. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm. Acesso em: 20 out. 2026.

CHEN, Peter Pin-Shan. The entity-relationship model: toward a unified view of data. **ACM Transactions on Database Systems**, v. 1, n. 1, p. 9-36, mar. 1976.

CHRISTIE, T. **Django REST Framework documentation**. 2024. Disponível em: https://www.django-rest-framework.org/. Acesso em: 11 abr. 2026.

DJANGO SOFTWARE FOUNDATION. **Django documentation**. 2024. Disponível em: https://docs.djangoproject.com/. Acesso em: 11 abr. 2026.

DJANGO SOFTWARE FOUNDATION. **Migrations**. [S. l.], 2026a. Disponível em: https://docs.djangoproject.com/en/stable/topics/migrations/. Acesso em: 20 out. 2026.

DJANGO SOFTWARE FOUNDATION. **Password management in Django**. [S. l.], 2026b. Disponível em: https://docs.djangoproject.com/en/stable/topics/auth/passwords/. Acesso em: 20 out. 2026.

FIELDING, Roy Thomas. **Architectural styles and the design of network-based software architectures**. 2000. Tese (Doutorado em Information and Computer Science) – University of California, Irvine, 2000.

FIELDING, R.; NOTTINGHAM, M.; RESCHKE, J. **HTTP semantics**. RFC 9110. [S. l.]: IETF, jun. 2022. Disponível em: https://www.rfc-editor.org/rfc/rfc9110. Acesso em: 20 out. 2026.

GAMMA, E. et al. **Padrões de projeto**: soluções reutilizáveis de software orientado a objetos. Porto Alegre: Bookman, 2000.

IBM. **JSON Web Token (JWT)**. IBM Documentation, 2024. Disponível em: https://www.ibm.com/docs/pt-br/cics-ts/6.x?topic=cics-json-web-token-jwt. Acesso em: 12 abr. 2026.

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Censo Agropecuário 2017**: resultados definitivos. Rio de Janeiro: IBGE, 2019. Disponível em: https://www.ibge.gov.br/estatisticas/economicas/agricultura-e-pecuaria/21814-2017-censo-agropecuario.html. Acesso em: 06 abr. 2026.

JAZZBAND. **Simple JWT**: a JSON Web Token authentication plugin for the Django REST Framework. [S. l.], 2026. Disponível em: https://django-rest-framework-simplejwt.readthedocs.io/. Acesso em: 20 out. 2026.

JONES, M.; BRADLEY, J.; SAKIMURA, N. **JSON Web Token (JWT)**. RFC 7519. [S. l.]: IETF, maio 2015. Disponível em: https://www.rfc-editor.org/rfc/rfc7519. Acesso em: 20 out. 2026.

KLENSIN, J. **Simple Mail Transfer Protocol**. RFC 5321. [S. l.]: IETF, out. 2008. Disponível em: https://www.rfc-editor.org/rfc/rfc5321. Acesso em: 20 out. 2026.

MERMAID. **Mermaid**: diagramming and charting tool. [S. l.], 2026. Disponível em: https://mermaid.js.org/. Acesso em: 20 out. 2026.

MORIARTY, K.; KALISKI, B.; RUSCH, A. **PKCS #5**: password-based cryptography specification version 2.1. RFC 8018. [S. l.]: IETF, jan. 2017. Disponível em: https://www.rfc-editor.org/rfc/rfc8018. Acesso em: 20 out. 2026.

NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. **FIPS PUB 180-4**: Secure Hash Standard (SHS). Gaithersburg: NIST, 2015. DOI: 10.6028/NIST.FIPS.180-4.

NODE.JS. **Node.js documentation**. [S. l.], 2026. Disponível em: https://nodejs.org/. Acesso em: 20 out. 2026.

OBJECT MANAGEMENT GROUP. **OMG Unified Modeling Language (OMG UML)**: version 2.5.1. [S. l.]: OMG, dez. 2017. Disponível em: https://www.omg.org/spec/UML/2.5.1. Acesso em: 20 out. 2026.

OWASP FOUNDATION. **Forgot password cheat sheet**. [S. l.], 2026. Disponível em: https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html. Acesso em: 20 out. 2026.

PINIA. **Pinia documentation**. [S. l.], 2026. Disponível em: https://pinia.vuejs.org/. Acesso em: 20 out. 2026.

PYTHON SOFTWARE FOUNDATION. **Python documentation**. 2024. Disponível em: https://docs.python.org/. Acesso em: 11 abr. 2026.

RAMOS, Vinícius. **O que é o Django REST Framework (DRF)?** Python Academy, 27 ago. 2024. Disponível em: https://pythonacademy.com.br/blog/o-que-e-o-django-rest-framework. Acesso em: 11 abr. 2026.

RENDER. **Render documentation**. [S. l.], 2026. Disponível em: https://render.com/docs. Acesso em: 20 out. 2026.

RESCORLA, E. **The Transport Layer Security (TLS) Protocol Version 1.3**. RFC 8446. [S. l.]: IETF, ago. 2018. Disponível em: https://www.rfc-editor.org/rfc/rfc8446. Acesso em: 20 out. 2026.

RIES, Eric. **A startup enxuta**. São Paulo: Leya, 2012.

SÁ, L. **JSON**: guia completo. 2023. Disponível em: https://www.hostgator.com.br/blog/json-guia-completo. Acesso em: 12 abr. 2026.

SEBRAE RS. **Marketplace**: o que é e como funciona. Porto Alegre, 27 ago. 2024. Disponível em: https://digital.sebraers.com.br/blog/marketing-e-vendas/marketplace-o-que-e-e-como-funciona/. Acesso em: 06 abr. 2026.

SILBERSCHATZ, Abraham; GALVIN, Peter Baer; GAGNE, Greg. **Fundamentos de sistemas operacionais**. 9. ed. Rio de Janeiro: LTC, 2015.

SILVA, Kathrein. **Feira do Produtor Rural Willi Dummer acontece neste sábado (20)**. Clic Camaquã, Camaquã, 17 set. 2025. Disponível em: https://www.cliccamaqua.com.br/noticias/feira-do-produtor-rural-willi-dummer-acontece-neste-sabado-20/. Acesso em: 06 abr. 2026.

SQLITE. **About SQLite**. [S. l.], 2026a. Disponível em: https://www.sqlite.org/about.html. Acesso em: 20 out. 2026.

SQLITE. **File locking and concurrency in SQLite version 3**. [S. l.], 2026b. Disponível em: https://www.sqlite.org/lockingv3.html. Acesso em: 20 out. 2026.

STALLINGS, William. **Criptografia e segurança de redes**: princípios e práticas. 6. ed. São Paulo: Pearson, 2015.

STRONG BUSINESS SCHOOL. **O que é B2C (Business to Consumer)?** [S. l.], [2026?]. Disponível em: https://strong.com.br/glossario/o-que-e-b2c-business-to-consumer/. Acesso em: 13 jun. 2026.

SUPABASE. **Database**. [S. l.], 2026a. Disponível em: https://supabase.com/docs/guides/database. Acesso em: 20 out. 2026.

SUPABASE. **Storage**. [S. l.], 2026b. Disponível em: https://supabase.com/docs/guides/storage. Acesso em: 20 out. 2026.

THE POSTGRESQL GLOBAL DEVELOPMENT GROUP. **PostgreSQL documentation**. 2024. Disponível em: https://www.postgresql.org/docs/. Acesso em: 11 abr. 2026.

THE POSTGRESQL GLOBAL DEVELOPMENT GROUP. **PostgreSQL documentation**: explicit locking. [S. l.], 2026. Disponível em: https://www.postgresql.org/docs/current/explicit-locking.html. Acesso em: 20 out. 2026.

TIOBE SOFTWARE. **TIOBE Index**. [S. l.], 2026. Disponível em: https://www.tiobe.com/tiobe-index/. Acesso em: 20 out. 2026.

UNIÃO EUROPEIA. Regulamento (UE) 2016/679 do Parlamento Europeu e do Conselho, de 27 de abril de 2016. Relativo à proteção das pessoas singulares no que diz respeito ao tratamento de dados pessoais e à livre circulação desses dados. **Jornal Oficial da União Europeia**, L 119, 4 maio 2016.

VERCEL. **Vercel documentation**. [S. l.], 2026. Disponível em: https://vercel.com/docs. Acesso em: 20 out. 2026.

VITE. **Vite documentation**. [S. l.], 2026. Disponível em: https://vite.dev/. Acesso em: 20 out. 2026.

VUE ROUTER. **Vue Router documentation**. [S. l.], 2026. Disponível em: https://router.vuejs.org/. Acesso em: 20 out. 2026.

VUE.JS. **Vue.js documentation**. 2024. Disponível em: https://vuejs.org/. Acesso em: 11 abr. 2026.

WHATWG. **HTML Living Standard**: the canvas element. [S. l.], 2026. Disponível em: https://html.spec.whatwg.org/multipage/canvas.html. Acesso em: 20 out. 2026.

YASAR, Kinza. **What is web application (web apps) and its benefits?** TechTarget, 25 nov. 2024. Disponível em: https://www.techtarget.com/searchsoftwarequality/definition/Web-application-Web-app. Acesso em: 11 abr. 2026.
