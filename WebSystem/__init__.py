from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'app.system'
login_manager.init_app(app)

import WebSystem.routes
from WebSystem.models import User, Pings

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_email):
    return User.query.get(user_email)
