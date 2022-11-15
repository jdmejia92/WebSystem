from src import app
from form.form import UserForm
from models import User
from flask import jsonify, request, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

user = Blueprint('user', __name__)

@user.route("/api/v01/login")
def login():
    
    return 

