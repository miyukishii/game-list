# Não é umm lib embutida do Python
from flask import Flask, render_template, request, redirect, session, flash, url_for


class Game:
    def __init__(self, name, category, console):
        self.name = name.title()
        self.category = category
        self.console = console
        
game1 = Game('Tetris', 'Puzzle', 'Atari')
game2 = Game('Super Mario Bros', 'Family', 'Nintendo')
game3 = Game('God of War', 'Rock n Slash', 'PS2')
games = [game1, game2, game3]

class User:
    def __init__(self, name, email, password):
        self._name = name
        self.email = email
        self._password = password
    
    @property
    def name(self):
        return self._name
    
    def check_password(self, input_value):
        return self._password == input_value
        
user1 = User('Amanda', 'amanda@gmail.com', '1234')
user2 = User('Carlos', 'carlos@gamil.com', '4321')
user3 = User('Larissa', 'larissa@gmail.com', '9876')
authorized_users = [user1, user2, user3]

app = Flask(__name__)
# com um valor string que será usado para encriptar os dados da sessão.
app.secret_key = 'jogoteca'

def redirect_to_home():
    return redirect(url_for('index'))

@app.route('/login')
def login():
    if ('logged_user' in session):
        return redirect_to_home()
    else:
        next = request.args.get('next')
        return render_template('login.html', title = 'Faça seu login', logout=True, next=next)


@app.route('/authentication', methods=['POST',])
def authentication():
    email = request.form['email']
    password = request.form['password']
    
    founded_user = ''
    
    for user in authorized_users:
        if(user.email == email):
            founded_user = user

    next = request.form['next']
    if(founded_user and founded_user.check_password(password)):
        session['logged_user'] = email
        # flash nos permite mostrar mensagens curtas de forma eficiente na interface da nossa aplicação.
        flash(f'{founded_user.name} logado com sucesso!')
        if next == 'None':
            return redirect_to_home()
        else:
            return redirect(next)
    else:
        flash('Usuário não encontrado')
        if next == 'None':
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login', next=next))


@app.route('/')
def index():
    if ('logged_user' in session):
        return render_template('index.html', title = 'JOGOS', games_list = games, button ={ "link": "/add-game", "title": "novo jogo" })
    else:
        return redirect('/login?next=/')


@app.route('/add-game')
def add_game():
    if ('logged_user' in session):
        return render_template('add-game.html', title = 'Novo jogo', button ={ "link": "/", "title": "voltar" })
    else:
        return redirect(url_for('login', next=url_for('add_game')))
    

@app.route('/create-game', methods=['POST',])
def create_game():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    
    game = Game(name, category, console)
    games.append(game)
    flash(f'{game.name} foi adicionado com sucesso!')
    return redirect_to_home()


@app.route('/logout')
def logout():
    del session['logged_user']
    flash('Logout efetuado com sucesso')   
    
    return redirect(url_for('login'))
    

app.run(debug=True)
# caso queiramos trocar a porta
# app.run(host='0.0.0.0', port=8080)