# marketplace_fome_zero
O repositório possui arquivos e script para construir um painel de estratégia da empresa
# 1 - Problema de negócio

#### Contexto do problema
Parabéns! Você acaba de ser contratado como Cientista de Dados da empresa
Fome Zero, e a sua principal tarefa nesse momento é ajudar o CEO Kleiton Guerra
a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer
utilizando dados!
A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.
#### O Desafio
O CEO Guerra também foi recém contratado e precisa entender melhor o negócio
para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a
Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da
empresa e que sejam gerados dashboards, a partir dessas análises, para responder
às seguintes perguntas:
#### Visão Geral
1. Restaurantes cadastrados.
2. Países registrados.
3. Cidades registradas.
4. Total de avaliações.
5. Total de tipos de culinária registrados.
#### Visão cidades
1. Top 10 cidades com mais restaurantes na base de dados.
2. Cidades com restaurantes com média de avaliação acima de 4.
3. Cidades com restaurantes com média de avaliação abaixo de 2,5.
4. Top 10 cidades com mais restaurantes cim tipos culinários distintos.
#### Visão países
1. Quantidade de restaurantes registrados por país.
2. Quantidade de cidades registrados por país.
3. Média de avaliação feita por país.
4. Média de preço de um prato para duas pessoas por país.
#### Visão restaurantes
1. Os Melhores restaurantes dos principais tipos de culinária.
2. Os 10 melhores restaurantes com maior avaliação.
3. Os 10 melhores tipos de culinária.
4. Os 10 piores tipos de culinária.

Seu trabalho é utilizar os dados que a empresa Fome Zero possui e responder as
perguntas feitas do CEO e criar o dashboard solicitado.

# 2 - Premissas do negócio
1. Marketplace foi o modelo de negócio assumido
2. As 4 principais visões do negócio foram: Visão geral, Visão cidade, visão países e visão resturantes.
3. A análise foi realizada com base no número de pedidos contido na base de dados.

# 3 - Estratégia da solução
O painel estratégico foi desenvolvido utilizando as métricas que refletem as 4 principais
visões do modelo de negócio da empresa:
1. Visão geral
2. Visão cidades
3. Visão países
4. Visão restaurantes
Cada visão é representada pelo seguinte conjunto de métricas.
## 1. Visão geral
a - Restaurantes cadastrados.
b - Países registrados.
c - Cidades registradas.
d - Total de avaliações.
e - Total de tipos de culinária registrados.

## 2. Visão cidades
a - Top 10 cidades com mais restaurantes na base de dados.
b - Cidades com restaurantes com média de avaliação acima de 4.
c - Cidades com restaurantes com média de avaliação abaixo de 2,5.
d - Top 10 cidades com mais restaurantes cim tipos culinários distintos.

## 3. Visão países
a - Quantidade de restaurantes registrados por país.
b - Quantidade de cidades registrados por país.
c - Média de avaliação feita por país.
d - Média de preço de um prato para duas pessoas por país.

## 4. Visão restaurante
a - Melhores restaurantes.
b - Restaurantes com maior avaliação.
c - Melhores tipos de culinária.
e - Piores tipos de culinária.

# 4 - Top 2 insight de dados
- A india possui maior número de restaurantes
- Filipinas é o pais com maior número de restaurantes com maiores taxas de avaliações

# 5 - O produto final do projeto
Painel online, hospedado em uma cloud e disponível para acesso em qualquer
dispositivo conectado à internet.
O painel pode ser acessado através desse link: https://project-marketplace-fome-zero.streamlit.app/

# 6 - Conclusão
O Objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas
métricas da melhor forma possivel para o CEO.

# 7 - Próximos passos
1. Verificar a possíbilidade de mais dados, para assim adicionar mais visões de negócio.
