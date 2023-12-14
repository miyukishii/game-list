import os
from flask import redirect, url_for
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, EmailField


class GameForm(FlaskForm):
    name = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=50)])
    category = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')
    
class UserForm(FlaskForm):
    email = EmailField('E-mail', [validators.DataRequired(), validators.Length(min=1, max=100), validators.Email()])
    password = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Entrar')


def redirect_to_home():
    return redirect(url_for('index'))


def get_cover(id):
    for filename in os.listdir(app.config['UPLOADS_PATH']):
        if f'cover-{id}' in filename:
            return filename
        
    return 'no-image.jpg'


def delete_cover(id):
    file = get_cover(id)
    if file != 'no-image.jpg':
        uploads_path = app.config['UPLOADS_PATH']
        os.remove(os.path.join(uploads_path, file))
