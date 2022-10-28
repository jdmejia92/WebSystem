import email
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired("Debe ingresar un correo electrónico")])
    password = PasswordField('password', validators=[DataRequired("Debe ingresar una contraseña")])
    remember = BooleanField('remember')

class SignupForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired("Debe ingresar un correo electrónico")])
    password = PasswordField('password', validators=[DataRequired("Debe ingresar una contraseña")])
    priority = SelectField('prioridad', validators=[DataRequired("Debe escoger un de las opciones")], choices=[(0, "User"), (1, "Admin")])