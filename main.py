# arquivo que vai executar nosso site, onde veremos ele funcionar
from fakepinterest import app

# Essa linha abaixo diz pra nosso código: se eu executar o arquivo main.py, é pra rodar o app.run(). Mas se esse
# main.py for importado de outro arquivo, NÃO é pra rodar o app.run()
if __name__ == "__main__":
    app.run(debug=False)   # Vai colocar nosso site no ar # debug=True - todas as alterações que fizermos no código,
    # serão automaticamente atualizadas no site no ar

