from WebSystem import app, db, admin
from .form import UserForm, SignupForm
from .models import User
from flask import jsonify, request, render_template, flash, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView

@app.route("/api/v01/login")
def login():
    form = UserForm()
    return render_template("login.html", form=form)

@app.route("/api/v01/login", methods=['POST'])
def login_post():
    form = UserForm(request.form)   
    if form.validate():
        remember = True if form.remember.data else False

        user = User.query.filter_by(email=form.email.data).first()
        print(user.priority)

        if not user or not check_password_hash(user.password, form.password.data):
            flash('Usuario y/o contraseña invalido')
            return redirect(url_for('login'))
        elif user.priority == "Admin" and check_password_hash(user.password, form.password.data):
            admin.add_view(ModelView(User, db.session))

        return redirect(url_for('system'))
    else:
        flash(form.errors)
        return redirect(url_for('login'))

@app.route("/api/v01/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'GET':
        return render_template("signup.html", form=form) 
    elif request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash("Usuario ya registrado")
            return redirect(url_for('signup'))
        
        new_user = User(email=form.email.data, password=generate_password_hash(form.password.data, method='sha256'), priority=form.priority.data)
        
        db.session.add(new_user)
        db.session.commit()

        return jsonify("Success")
    else:
        flash(form.errors)
        return render_template("signup.html", form=form)

@app.route("/api/v01/system", methods=['GET'])
def system():
    return jsonify("Success")