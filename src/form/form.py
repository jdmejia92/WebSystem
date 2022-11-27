from flask_wtf import FlaskForm
import wtforms_json
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.fields import EmailField, PasswordField, StringField

wtforms_json.init()


def priorityCheck(form, field):
    if field.data != "admin":
        if field.data != "user":
            raise ValidationError("Priority must be a valid value")


class UserForm(FlaskForm):
    email = EmailField(
        "email", validators=[DataRequired(message="You must add an email")]
    )
    password = PasswordField(
        "password",
        validators=[
            DataRequired(message="You must add the password"),
            Length(min=6, max=10),
        ],
    )
    priority = StringField(
        "priority",
        validators=[DataRequired(message="You must add a priority"), priorityCheck],
    )
