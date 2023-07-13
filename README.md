# ratingsUnB
Repositório para projeto individual da disciplina de Banco de Dados - 2023.1 - Universidade de Brasília

## Tecnologias utilizadas

-Para implementação do BackEnd e FrontEnd foi utilizado o framework Flask para a linguagem Python.
-Como SGBD foi utilizado o PostgreSQL.

## Como rodar?

  Primeiramente é necessário instalar o postgresql em sua máquina e configurá-lo criando um database com nome de 'ratingsunb_db' e um usuário com todos os privilégios nesse database. Depois exporte o seu usuário e senha do database com ```export DB_USERNAME=<nome_de_usuario>``` e sua senha com ```export DB_PASSWORD=<senha_de_usuario>```.
  Depois instale o python, o flask e as dependencias flask-session e psycopg2. Após isso rode o arquivo init_db.py para criar as tabelas do banco de dados com o script SQL presente nesse arquivo. Após isso, basta inicar a aplicação com ```flask run```. 
