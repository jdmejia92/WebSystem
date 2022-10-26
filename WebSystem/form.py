from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

class UserForm(FlaskForm):
    email = EmailField('Correo electrónico', validators=[DataRequired(), Email(), EqualTo()])
    password = PasswordField('Contraseña', validators=[DataRequired(), EqualTo()])
    remember = BooleanField('Recuerdame')