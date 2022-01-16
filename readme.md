<h1>Contextualização</h1>

O serviço desenvolvido é um controle de finanças pessoais, que possui gerenciamento (CRUD) de contas, receitas e despesas. Além disso, faz-se o uso de bancos relacionais para armazenar as informações.

<h2>Projeto PubFuture</h2>

Neste projeto, desenvolveu-se um serviço web de controle de finanças pessoais. Esse desenvolvimento faz parte do processo seletivo do programa PubFuture.

O gerenciamento de despesas e receitas está vinculado à conta, ou seja, no momento em que alguma despesa ou receita é gerenciada (criada, editada ou deletada), há influência diretamente no saldo da conta.

O projeto foi realizado em Python3.7 e requer a instalação de alguns pacotes. Não há necessidade de instalação de qualquer banco de dados, visto que se utilizou SQLite.

<h1>Como usar</h1>

Inicialmente, recomenda-se [criar um ambiente virtual de Python](https://docs.python.org/pt-br/3.7/library/venv.html), preferencialmente na versão 3.7 (versão utilizada no desenvolvimento).

Crie uma pasta e faça o clone deste repositório em seu local de desenvolvimento pelo comando:

````
git clone https://github.com/matheus-bona/desafiopubfuture.git
````

Ou faça o download manualmente em formato .zip e descompacte na pasta criada.

Após ter clonado/descompactado este repositório, com o ambiente virtual ativado, utilize o comando abaixo para a instalação dos pacotes:

````
pip install django==2.2.3 pytz==2019.1 sqlparse==0.3.0
````

Em sequência, para a migração dos modelos criados na base de dados, utilize o comando: 

````
python manage.py migrate
````
O próprio algoritmo cria a base de dados SQLite caso não for encontrada.

Por fim, para rodar a aplicação digite:
````
python manage.py runserver
````
Feito isso, a página se encontrará disponível no endereço 127.0.0.1:8000

Por meio do cabeçalho da página é possível ser redirecionado para Contas, Despesas e Receitas.

A ação de cadastrar, editar ou deletar uma despesa/receita influi diretamente no saldo da conta em questão.



