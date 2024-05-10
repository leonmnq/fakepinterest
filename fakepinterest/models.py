# criar a estrutura do banco de dados
from fakepinterest import database, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin  # UserMixin é quem diz qual a classe que vai gerenciar a estrutura de logins


@login_manager.user_loader  # decorator
def load_usuario(id_usuario):  # é obrigatório criar essa função sempre que você cria a estrutura de login
    return Usuario.query.get(int(id_usuario))  # retorna pra gente um usuário específico


class Usuario(database.Model, UserMixin):  # tanto a classe Usuario quanto a classe Foto são subclasses do database.Model  # classe que vai gerenciar 'UserMixin'
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True)  # vai ter uma relação com a classe 'Foto' # backref="usuario" é como se vc tivesse criando 'usuario = database.relationship()' na classe Foto # lazy=True é pra otimizar como você puxa informações do banco de dados


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")  # o que será armazenado no banco é o nome que a imagem tem dentro da pasta 'static'
    # data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())  #datetime.utcnow() é obsoleto
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now(timezone.utc))
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False )  # ChaveEstrangeira('tabela=usuario.coluna=id')