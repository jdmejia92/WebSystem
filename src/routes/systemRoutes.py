from flask import jsonify, request, Blueprint
from src.form.form import MachineForm
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
        return jsonify({"message": str(ex)}), 500


@system.route("/add", methods=["POST"])
@auth.login_required
def addMachine():
    try:
        form = MachineForm.from_json(request.json, skip_unknown_keys=False)
        if form.validate:
            add = MachineManager.addMachine(
                machine=form.data["ipv4"], user_id=auth.current_user().id
            )
            return add
        return jsonify(form.errors), 400
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@system.route("/delete/<id>", methods=["DELETE"])
@auth.login_required
def deleteMachine(id):
    try:
        delete = MachineManager.deleteMachine(id)
        return delete
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
