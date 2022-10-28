from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
db = SQLAlchemy(app)
admin = Admin(app)

login_manager = LoginManager(app)
login_manager.login_view = 'system'
#login_manager.init_app()

import WebSystem.routes
from WebSystem.models import User, Pings

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_email):
    return User.query.get(user_email)
