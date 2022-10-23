from WebSystem import app
from flask_login import LoginManager
from config import SECRET_KEY
from flask import flash, render_template, jsonify, request, url_for, redirect
from WebSystem.models import DataManager, User
import random as rd

route_db = app.config['ROUTE_BBDD']
data_manager = DataManager(route_db)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager(app)

@app.route("/")
def start():
    return render_template('index.html')

@app.route("/api/v01/login/<user>/<password>", methods=['GET', 'POST'])
def login(user, password):
    global key
    key = rd.randrange(0,100)
    if request.method == 'GET':
        pings = data_manager.consult_ping()
        data = data_manager.user_information()
        for users in data:
            if users["User"] == user:
                user_check = users
        if user_check["User"] == user and str(user_check["Password"]) == password:
            return redirect("http://localhost:5000/api/v01/system/{}/{}/{}".format(user, password, key)) 
        else:
            return "Correo o contraseña errado"

@app.route("/api/v01/system/<user>/<password>/<int:key>", methods=['GET', 'POST', 'UPDATE'])
def pings(user, password, key):
    if request.method == 'GET':
        if key == key:
            return render_template('index.html')
