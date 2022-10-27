from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired("Debe ingresar un correo electrónico")])
    password = PasswordField('password', validators=[DataRequired("Debe ingresar una contraseña")])
    remember = BooleanField('remember')