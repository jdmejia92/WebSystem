from flask import jsonify, request, Blueprint
from src.models.userModel import auth
from src.models.machineModel import MachineManager

system = Blueprint("system", __name__)


@system.route("/")
@auth.login_required
def getMachines():
    try:
        machines = MachineManager.getMachines()
        return machines
    except Exception as ex:
        return ({"message": str(ex)})

@system.route("/add", methods=["POST"])
@auth.login_required
def addMachine():
    try:
        data = request.json
        add = MachineManager.addMachine(machine=data["ipv4"], user_id=auth.current_user().id)
        return add
    except Exception as ex:
        return jsonify({"message": str(ex)})

@system.route("/delete/<id>", methods=["DELETE"])
@auth.login_required
def deleteMachine(id):
    try:
        delete = MachineManager.deleteMachine(id)
        return delete 
    except Exception as ex:
        return jsonify({"message": str(ex)})
