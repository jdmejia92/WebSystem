from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class UsersForm(FlaskForm):
    users = EmailField(u"Usuario", validators=[DataRequired(message="Debe colocar el usuario")])
    password = PasswordField(u"Contraseña", validators=[DataRequired(message="Debe colocar la contraseña")])
    aceptar = SubmitField("Aceptar")