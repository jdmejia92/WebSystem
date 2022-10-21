from flask_login import LoginManager
from WebSystem import app
from flask import render_template, jsonify, request
#from WebSystem.models import DataProcess

route_db = app.config['ROUTE_BBDD']
login_manager = LoginManager(app)
#data_manager =

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/api/v01/login")
def machines():
    return