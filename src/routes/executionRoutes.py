from flask import jsonify, request, Blueprint
from src.models.userModel import auth
from src.models.executionModel import ExecutionManager

execution = Blueprint("execution", __name__)

@execution.route("/")
@auth.login_required(role=1)
def getExecutions():
    try:
        result = ExecutionManager.getExecutions()
        if result == 400:
            return jsonify({"message": "No se encontraron acciones"}), 400
        return jsonify(result)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@execution.route("/<id>")
@auth.login_required(role=1)
def getExecution(id):
    try:
        result = ExecutionManager.getExecution(id)
        if result == 400:
            return jsonify({"message": "No se encontro la acción"}), 400
        return jsonify(result)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500