from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config

db = SQLAlchemy()
SQL_URI = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
    user=config("PGSQL_USER"),
    pw=config("PGSQL_PASSWORD"),
    url=config("PGSQL_HOST"),
    db=config("PGSQL_DATABASE"),
)

app = Flask(__name__, instance_relative_config=True)
app.config["SQLALCHEMY_DATABASE_URI"] = SQL_URI
# app.config["SECRET_KEY"] = "MYPASSWORD15/*-?!$%&"
app.config["WTF_CSRF_ENABLED"] = False
db.init_app(app)


# Blueprint para usuarios
from src.routes.userRoutes import user as user_blueprint

app.register_blueprint(user_blueprint, url_prefix="/api/v01/users")

# Blueprint para el sistema
from src.routes.systemRoutes import system as system_blueprint

app.register_blueprint(system_blueprint, url_prefix="/api/v01/system")

# Crear tabla
from src.database.db import create_database

create_database()
