from WebSystem import app, db
from WebSystem.models import create_table
from flask import jsonify, request, render_template

@app.route("/api/v01/system", methods=['GET', 'POST', 'UPDATE'])
def pings():
    create_table()
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('password')