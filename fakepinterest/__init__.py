# __init__ é onde o aplicativo é criado, é onde o banco de dados é criado
from flask import Flask     # Flask com 'F' maiúsculo, é o que vai criar o nosso site
from flask_sqlalchemy import SQLAlchemy  # para criar nosso banco de dados
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

# o flask sugere que sempre, a primeira coisa é criar o 'app'
app = Flask(__name__)  # app nada mais é, que o nosso site, nossa aplicação

"""
Condição para ambiente online e ambiente local: 
"""
# if os.getenv("DEBUG") == 0:  # significa que não está em um ambiente de debug OBS: necessário criar a variável de ambiente DEBUG com valor 0 lá no sistema do render
#     link_banco = os.getenv("DATABASE_URL")  # o link será esse, significa que está no ambiente online
# else:
#     link_banco = "sqlite:///comunidade.db"  # utiliza o banco de dados local, offline

"""
PARA CRIAR AS TABELAS DO BANCO DE DADOS LÁ NO BANCO POSTEGRESQL DO RENDER, 'DESCOMENTAR' ESSA LINHA: (Rodar o criar_banco.py uma vez e comentar a linha novamente):
"""
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://db_fakepinterest_n275_user:jwZE8sKVIyy5S2IkgM0Mv4Pt7v2G6aI2@dpg-cov5rfnjbltc73d8do50-a.oregon-postgres.render.com/db_fakepinterest_n275"  # External Database URL

""" Configuração para uso do banco de dados online postgresql do render: """
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")  # Internal Database URL

""" Configuração ara uso do banco de dados local sqlite: """
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"  # configuração para uso do banco local

app.config["SECRET_KEY"] = "204fd3b542111b5941ee62257eef7ec1" # nosso aplicativo vai usar a chave de segurança como referência pra garantir a segurança do app
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"  # define onde as fotos serão armazenadas

#app.config["UPLOAD_FOLDER"] = "/fotos_posts"  # para armazenar as fotos na pasta criada dentro do render


database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"  # definir aonde um usuário será direcionado se ele NÃO estiver logado

# As importações de outros arquivos do nosso projeto para dentro do __init__ devem ocorrer daqui para baixo
from fakepinterest import routes_or_views