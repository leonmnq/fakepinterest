# __init__ é onde o aplicativo é criado, é onde o banco de dados é criado
from flask import Flask     # Flask com 'F' maiúsculo, é o que vai criar o nosso site
from flask_sqlalchemy import SQLAlchemy  # para criar nosso banco de dados
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# o flask sugere que sempre, a primeira coisa é criar o 'app'
app = Flask(__name__)  # app nada mais é, que o nosso site, nossa aplicação
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"  # configuração para criação do banco
app.config["SECRET_KEY"] = "204fd3b542111b5941ee62257eef7ec1" # nosso aplicativo vai usar a chave de segurança como referência pra garantir a segurança do app
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"  # define onde as fotos serão armazenadas

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"  # definir aonde um usuário será direcionado se ele NÃO estiver logado

# as importações de outros arquivos do nosso projeto para dentro do __init__ devem ocorrer daqui para baixo
from fakepinterest import routes_or_views