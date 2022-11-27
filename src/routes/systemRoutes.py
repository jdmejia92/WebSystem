from flask import jsonify, request, Blueprint

system = Blueprint("system", __name__)


@system.route("/")
def start():
    return "Success"
