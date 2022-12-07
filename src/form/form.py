from flask_wtf import FlaskForm
import wtforms_json
from wtforms.validators import DataRequired, Length, ValidationError, Regexp, IPAddress
from wtforms.fields import EmailField, PasswordField, StringField

wtforms_json.init()


def priorityCheck(form, field):
    if field.data != "admin":
        if field.data != "user":
            raise ValidationError("Priority must be a valid value")


class UserForm(FlaskForm):
    email = EmailField(
        "email",
        validators=[
            DataRequired(message="You must add an email"),
            Regexp(
                "^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$",
                message="Debes añadir un correo correcto",
            ),
        ],
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


class MachineForm(FlaskForm):
    machine = StringField(
        "machine",
        validators=[
            DataRequired(message="You must add a machine"),
            IPAddress(message="Debes añadir un IP correcto"),
        ],
    )
