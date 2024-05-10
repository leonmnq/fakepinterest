# criar as rotas do nosso site (os links)

from flask import render_template   # 'render_template' procura no nosso projeto uma pasta chamada 'templates' e vai carregar os arquivos que estiverem dentro dessa pasta
from flask import url_for   # permite você direcionar um cara para um link específico através do nome da função, ao invés de usar o texto dentro da rota
from flask import redirect  # importa o redirecionador
from fakepinterest import app  # importa o aplicativo criado dentro do __init__
from fakepinterest import database  # importa o banco de dados
from fakepinterest import bcrypt
from fakepinterest.models import Usuario, Foto
from flask_login import login_required  # pra exigir que tenha um login
from flask_login import login_user, logout_user, current_user  # current_user é o usuário que está logado
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto  # importando os formulários que criamos
import os
from werkzeug.utils import secure_filename  # vai transformar o nome da foto em um nome seguro


# colocar o site no ar
@app.route("/", methods=["GET", "POST"])  # decorator # "/" rota principal do nosso site, homepage  # methods=["GET", "POST"] é necessário sempre que você tem um formulário com método "POST" dentro da página html que você quer carregar
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():  # se todos os campos estão preenchidos e o usuário clicou no botão Login
        usuario = Usuario.query.filter_by(email=form_login.email.data).first() # vai verificar na tabela Usuario do banco de dados se existe algum e-mail igual ao e-mail que foi preenchido no FormCriarConta e vai retornar uma lista de um item na variável 'usuario'
        if usuario:  # se for encontrado esse email no banco de dados
            if bcrypt.check_password_hash(usuario.senha.encode('utf-8'), form_login.senha.data):  # compara a senha criptografada do bando de dados com a senha que o usuário acabou de digitar
            #if usuario.senha == form_login.senha.data:
                login_user(usuario)
                return redirect(url_for("perfil", id_usuario=usuario.id)) # redireciona para tela de perfil do usuário
        # else:  # criei esse else para usuário que não possui conta e tenta fazer login
        #     return redirect(url_for("criarconta"))
    return render_template("homepage.html", form=form_login)  # 'homepage.html' é o arquivo que queremos que o render_template carregue


@app.route("/criarconta", methods=["GET", "POST"])
def criar_conta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():  # se todos os campos estão preenchidos e o usuário clicou no botão Criar Conta
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')  # criptografa a senha
        #senha = form_criarconta.senha.data
        usuario = Usuario(
            username=form_criarconta.username.data,
            email=form_criarconta.email.data,
            senha=senha
        )
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)  # remember=True armazena nos cookies do navegador que o usuário está logado
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=form_criarconta)


@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])   # '<usuario>' assim, entre <>, sinaliza que 'usuario' é uma variável e não um texto
@login_required  # exige um login para acesso
def perfil(id_usuario):  # aqui também precisa passar a mesma variável 'usuario' como parâmetro da função
    if int(id_usuario) == int(current_user.id):  # se o usuário do parâmetro for o próprio usuário atual
        # o usuário tá vendo seu próprio perfil
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # salvar o arquivo na pasta fotos_post
            caminho = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                nome_seguro
            )  # "os.path.abspath(os.path.dirname(__file__))" retorna o caminho onde esse código está escrito
            arquivo.save(caminho)

            # registrar o nome desse arquivo no bando de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()

        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)  # 'usuario' em vermelho é a variável, 'usuario' em branco é o valor dessa variável, esse valor é o que vai aparecer na página html


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()  # pegando todas as fotos do banco de dados, da mais recente para mais antiga
    return render_template("feed.html", fotos=fotos)