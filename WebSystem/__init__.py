from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
db.init_app(app)

import WebSystem.routes