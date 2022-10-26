from django.shortcuts import redirect
from WebSystem import app, db
from .form import UserForm
from .models import create_table, User
from flask import jsonify, request, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/api/v01/login", methods=['GET', 'POST'])
def login():
    create_table()
    form = UserForm(request.form)
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST" and form.validate():
        email = form.email.data
        password = form.password.data
        remember = True if form.remember.data else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Usuario y/o contraseña invalido')
        return redirect()