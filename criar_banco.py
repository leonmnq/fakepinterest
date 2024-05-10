from fakepinterest import app, database  # importando app e database do __init__
from fakepinterest.models import Usuario, Foto  # importando as duas classes criadas em 'models'

with app.app_context():  # exigência das versões recentes do flask, criar o banco dentro de um contexto
    database.create_all()