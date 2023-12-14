# Arquivo para rotas
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Games
from helpers import *
import time


@app.route('/')
def index():
    list = Games.query.order_by(Games.id)
    if ('logged_user' in session):
        return render_template('index.html', title = 'JOGOS', games_list = list, button ={ "link": "/add-game", "title": "novo jogo" })
    else:
        return redirect('/login?next=/')


@app.route('/add-game')
def add_game():
    if ('logged_user' in session):
        form = GameForm()
        return render_template('add-game.html', title = 'Novo jogo', button ={ "link": "/", "title": "voltar"}, form=form )
    else:
        return redirect(url_for('login', next=url_for('add_game')))
    

@app.route('/create-game', methods=['POST',])
def create_game():
    form = GameForm(request.form)
    
    if not form.validate_on_submit():
        flash('Preencha os campos corretamentes')
    else:
        request_name = form.name.data
        request_category = form.category.data
        request_console = form.console.data
        file = request.files['image']
        uploads_path = app.config['UPLOADS_PATH']
        
        game = Games.query.filter_by(name=request_name).first()
        if (game):
            flash(f'{request_name} já consta na lista.')
        else:
            new_game = Games(name=request_name, category=request_category, console=request_console)
            db.session.add(new_game)
            db.session.commit()
            timestamp = time.time()
            delete_cover(new_game.id)
            file.save(f'{uploads_path}/cover-{new_game.id}-{timestamp}.jpg')
            flash(f'{request_name} foi adicionado com sucesso!')
            return redirect_to_home()


@app.route('/edit-game/<int:id>')
def edit_game(id):
    if ('logged_user' in session):
        game = Games.query.filter_by(id=id).first()
        form = GameForm()
        form.name.data = game.name
        form.category.data = game.category
        form.console.data = game.console
        cover = get_cover(id)
        return render_template('edit-game.html', title = 'Editar jogo', button ={ "link": "/", "title": "voltar", }, form=form, cover=cover, game_id=game.id)
    else:
        return redirect(url_for('login', next=url_for('edit_game')))
    

@app.route('/update-game', methods=['POST',])
def update_game():
    form = GameForm(request.form)
    
    if form.validate_on_submit():
        request_id = request.form['id']
        request_name = form.name.data
        request_category = form.category.data
        request_console = form.console.data
        
        edit_game = Games.query.filter_by(id=request_id).first()
        edit_game.name = request_name
        edit_game.category = request_category
        edit_game.console = request_console
        
        db.session.add(edit_game)
        db.session.commit()
        file = request.files['image']
        delete_cover(request_id)
        uploads_path = app.config['UPLOADS_PATH']
        timestamp = time.time()
        file.save(f'{uploads_path}/cover-{edit_game.id}-{timestamp}.jpg')
        flash(f'{request_name} foi editado com sucesso!')
        
    return redirect_to_home()


@app.route('/delete-game/<int:id>')
def delete_game(id):
    if ('logged_user' in session):
        Games.query.filter_by(id=id).delete()
        delete_cover(id)
        db.session.commit()
        flash('Jogo foi removido com sucesso!')
        return redirect_to_home()
    else:
        return redirect(url_for('login', next=url_for('edit_game')))
    

@app.route('/uploads/<filename>')
def image(filename):
    return send_from_directory('uploads', filename)

