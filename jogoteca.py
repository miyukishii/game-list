# Arquivo para instanciação da aplicação
# Não é umm lib embutida do Python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

from views_game import *
from views_user import *

# Garante que toda vez que rode, vai realizar todas as importações corretamente.
if __name__ == '__main__':
    app.run(debug=True)
    # caso queiramos trocar a porta
    # app.run(host='0.0.0.0', port=8080)