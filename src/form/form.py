from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms.fields import EmailField, PasswordField


class UserForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired(message="You must add an email")])
    password = PasswordField("password", validators=[DataRequired(message="You must add the password"), Length(min=6, max=10)])