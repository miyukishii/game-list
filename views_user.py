# Arquivo para rotas de usuários
from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app
from models import Users
from helpers import *
from flask_bcrypt import check_password_hash


@app.route('/login')
def login():
    if ('logged_user' in session):
        return redirect_to_home()
    else:
        form = UserForm()
        next = request.args.get('next')
        return render_template('login.html', title = 'Faça seu login', logout=True, next=next, form=form)


@app.route('/authentication', methods=['POST',])
def authentication():
    form = UserForm(request.form)
    request_email = form.email.data
    password = form.password.data
    check_password = False
    user = Users.query.filter_by(email=request_email).first()
    
    if user:
        check_password = check_password_hash(user.password, password)
    
    next = request.form['next']
    if(user and check_password):
        session['logged_user'] = request_email
        # flash nos permite mostrar mensagens curtas de forma eficiente na interface da nossa aplicação.
        flash(f'{user.name} logado com sucesso!')
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


@app.route('/logout')
def logout():
    del session['logged_user']
    flash('Logout efetuado com sucesso')   
    
    return redirect(url_for('login'))
    
