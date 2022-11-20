from flask import jsonify, request, Blueprint
from flask_login import login_required

system = Blueprint('system', __name__)

@system.route('/')
def start():
    return "Success"