### Librex Api Docs

Neste documento estarão contidas informações sobre as rotas da api, regras de negócio, comunicação e manipulação do banco de dados, entre outros. Estes, serão adicionados em breve, no entanto, abaixo encontra-se uma breve instrução de bibliotecas necessárias para o uso da api.

> AVISO: Este programa foi desenvolvido e testado no windows. Para usuários de MAC, podem haver diferenças e necessidade de alteração em comandos ou nos procedimentos de instalação.

---


#### Python

Toda a API foi desenvolvida com python e, portanto, é um pré-requisito tê-lo instalado. Para isso, basta executar o seguinte comando:

`winget search Python.Python`

Escolha a versão mais recente e instale com o comando

`winget install Python.Python.3.12 <- ou a versão mais recente, após o ponto`

ou se preferir, basta visitar o [site oficial do python](https://www.python.org/downloads).
Execute o arquivo de instalação e siga as instruções.

#### Flask

O flask é o framework utilizado na aplicação para possibilitar a comunicação entre o back-end e o front-end.

##### Instalação

Para instalar o framework, basta executar os seguintes comandos no seu console:

##### Flask
É necessário instalar o framework em si e, em seguida...
`C:\user> pip install flask`

##### Flask Cors
Instalar o Cors
`C:\user> pip -U install flask-cors`

#### MySQL connector
Este é necessário para a comunicação e manipulação no banco de dados.
`C:\user> pip install mysql-connector-python`

Recomendo utilizar o meu arquivo para trabalhar com o banco de dados. Basta clicar [aqui](https://github.com/abraaosantosdeveloper/programming-utils/blob/main/pythonUtilities/sql_connector_util.py)

##### Alguns requisitos extras
```
- Jwt para geração de tokens
- Fernet para encriptação
```
