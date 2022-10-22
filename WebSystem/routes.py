#from flask_login import LoginManager
from WebSystem import app
from flask import render_template, jsonify, request, url_for, redirect
#from WebSystem.models import DataProcess

route_db = app.config['ROUTE_BBDD']
#login_manager = LoginManager(app)
#data_manager =

@app.route("/")
def start():
    return render_template("base.html")

@app.route("/api/v01/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(request.form)
        return "Access Granted"
    else:
        print(request.form)
        return redirect(url_for("start"))