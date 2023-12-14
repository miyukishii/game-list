# Arquvio para configurações do banco de dados
import os
# com um valor string que será usado para encriptar os dados da sessão.
SECRET_KEY = 'jogoteca'

# Conectando ao banco de dados
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = 'localhost',
        database = 'jogoteca'
    )

UPLOADS_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
