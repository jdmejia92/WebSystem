from flask import jsonify, request, Blueprint
from src.form.form import MachineForm
from src.models.userModel import auth, UserManager
from src.models.machineModel import MachineManager, PingsManager
from src.models.executionModel import ExecutionManager

system = Blueprint("system", __name__)


@system.route("/")
@auth.login_required
def getMachines():
    try:
        machines = MachineManager.getMachines()
        if machines[1] == 400:
            return jsonify(machines[0]), 400
        return machines[0]
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@system.route("/<id>")
@auth.login_required
def getMachine(id):
    try:
        machine = MachineManager.getMachine(id)
        if machine[1] == 400:
            return jsonify(machine[0]), 400
        email = UserManager.getUserEmail(machine, model="system")
        return email
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@system.route("/add", methods=["POST"])
@auth.login_required
def addMachine():
    try:
        form = MachineForm.from_json(request.json, skip_unknown_keys=False)
        if form.validate():
            add = MachineManager.addMachine(
                machine=form.data["machine"], user_id=auth.current_user().id
            )
            if add[1] == 400:
                return jsonify(add[0]), 400
            ExecutionManager.queryMachine(user=auth.current_user(), machine_id=add[0]["id"], current_action=4)
            return jsonify(add[0])
        return jsonify(form.errors), 400
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@system.route("/delete/<id>", methods=["DELETE"])
@auth.login_required
def deleteMachine(id):
    try:
        delete = MachineManager.deleteMachine(id)
        if delete[1] == 400:
            return jsonify(delete[0])
        ExecutionManager.queryMachine(user=auth.current_user(), machine_id=delete[0]["id"], current_action=5)
        return jsonify(delete[0])
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@system.route("/update/<id>", methods=["PUT"])
@auth.login_required()
def updateMachine(id):
    try:
        form = MachineForm.from_json(request.json, skip_unknown_keys=False)
        if form.validate():
            updating = MachineManager.updateMachine(
                id=id,
                machine=form.data["machine"],
            )
            if updating[1] == 400:
                return jsonify(updating[0])
            return updating[0]
        else:
            return jsonify({"message": str(form.errors)}), 400
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@system.route("/ping")
@auth.login_required()
def ping():
    try:
        pings = PingsManager.ping()
        if pings[1] == 400:
            return jsonify(pings[0])
        return jsonify(pings[0])
    except Exception as ex:
        return jsonify({"Message": str(ex)})
