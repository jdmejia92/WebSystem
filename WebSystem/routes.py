from WebSystem import app, db
from .form import UserForm
from .models import create_table, User
from flask import jsonify, request, render_template, flash, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/api/v01/login")
def login():
    form = UserForm()
    return render_template("login.html", form=form)

@app.route("/api/v01/login", methods=['POST'])
def login_post():
    create_table()
    form = UserForm(request.form)    
    if form.validate():
        email = form.email.data
        password = form.password.data
        remember = True if form.remember.data else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Usuario y/o contraseña invalido')
            return redirect(url_for('login'))

        return redirect(url_for('system'))
    else:
        flash(form.errors)
        return redirect(url_for('login'))

@app.route("/api/v01/signup", methods=['GET', 'POST'])
def signup():
    form = UserForm(request.form)
    if request.method == 'GET':
        return 

@app.route("/api/v01/system", methods=['GET'])
def system():
    return render_template("pings.html")
