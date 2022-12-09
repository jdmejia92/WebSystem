from flask import jsonify, request, Blueprint
from src.models.userModel import auth, UserManager
from src.models.executionModel import ExecutionManager

execution = Blueprint("execution", __name__)

@execution.route("/")
@auth.login_required(role=1)
def getExecutions():
    try:
        result = ExecutionManager.getExecutions()
        if result[1] == 400:
            return jsonify(result[0]), 400
        for item in result[0]:
            email = UserManager.getUserEmail(execution=item, model="execution")
            if len(email) == 1:
                item.update({"user": email["user"]})
            else:
                item.update({"user": email["user"]})
                item.update({"user_checked": email["user_checked"]})
        return jsonify(result[0])
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@execution.route("/<id>")
@auth.login_required(role=1)
def getExecution(id):
    try:
        result = ExecutionManager.getExecution(id)
        if result[1] == 400:
            return jsonify(result[0]), 400
        for item in result[0]:
            email = UserManager.getUserEmail(execution=item, model="execution")
            if len(email) == 1:
                item.update({"user": email["user"]})
            else:
                item.update({"user": email["user"]})
                item.update({"user_checked": email["user_checked"]})
        return jsonify(result[0])
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500