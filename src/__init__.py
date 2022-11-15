from .routes.routes import user as user_blueprint
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config

db = SQLAlchemy()
SQL_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=config(
    'PGSQL_USER'), pw=config('PGSQL_PASSWORD'), url=config('PGSQL_HOST'), db=config('PGSQL_DATABASE'))

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_URI

# Blueprint para usuarios
app.register_blueprint(user_blueprint, url_prefix='/api/v01/users')

# Activar base de datos
db.init_app(app)
