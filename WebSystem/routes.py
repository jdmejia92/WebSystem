#from flask_login import LoginManager
from WebSystem.forms import UsersForm
from WebSystem import app
from flask import render_template, jsonify, request, url_for, redirect
#from WebSystem.models import DataProcess

route_db = app.config['ROUTE_BBDD']
#login_manager = LoginManager(app)
#data_manager =

@app.route("/", methods=["GET"])
def login():
    form = UsersForm()
    if request.method == "GET":
        return render_template("index.html", formulario=form)

@app.route("/api/v01/login", methods=["GET", "POST"])
def machines():
    if request.method == "POST":
        return render_template("system.html")
    else:
        print(request.form)
        return redirect(url_for("start"))