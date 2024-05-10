# criar os formulários do nosso site
from flask_wtf import FlaskForm  # para importar a estrutura para criação de formulário
from wtforms import StringField, PasswordField, SubmitField , FileField # importa os campos de texto, senha, também o botão submit e o campo de arquivo
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError  # DataRequired = campo obrigatório # EqualTo = verifica se um campo é igual a outro Ex: senha e confirmação de senha # ValidationError = retorna uma msg de erro caso ocorra
from fakepinterest.models import Usuario


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])  # label/rótulo "E-mail"
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmar = SubmitField("Fazer Login")

    def validate_email(self, email):  # o nome tem que ser validate_email porque queremos validar o atributo 'email' da classe 'FormCriarConta'
        usuario = Usuario.query.filter_by(email=email.data).first() # vai verificar na tabela Usuario do banco de dados se existe algum e-mail igual ao e-mail que foi preenchido no FormCriarConta e vai retornar uma lista de um item na variável 'usuario'
        if not usuario:  # se a variável usuario NÃO recebeu a lista com um item
            raise ValidationError("Usuário inexistente, crie uma conta")


class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Nome de usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmar = SubmitField("Criar Conta")

    def validate_email(self, email):  # o nome tem que ser validate_email porque queremos validar o atributo 'email' da classe 'FormCriarConta'
        usuario = Usuario.query.filter_by(email=email.data).first() # vai verificar na tabela Usuario do banco de dados se existe algum e-mail igual ao e-mail que foi preenchido no FormCriarConta e vai retornar uma lista de um item na variável 'usuario'
        if usuario:  # se a variável usuario recebeu a lista com um item
            raise ValidationError("E-mail já cadastrado, faça login para continuar")


class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botao_confirmar = SubmitField("Enviar")