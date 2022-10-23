from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class UsersForm(FlaskForm):
    users = EmailField(u"Usuario", validators=[DataRequired(message="Debe colocar el usuario"), EqualTo("confirm")], render_kw={"placeholder": "Usuario", "class": "fadeIn second"})
    password = PasswordField(u"Contraseña", validators=[DataRequired(message="Debe colocar la contraseña"), EqualTo("confirm")], render_kw={"placeholder": "Contraseña", "class": "fadeIn third"})
    login = SubmitField(u"Aceptar", render_kw={"placeholder": "Log In", "class": "fadeIn fourth"})
