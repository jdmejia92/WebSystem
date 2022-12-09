from flask import jsonify, Blueprint
from src.models.pingModel import PingsManager
from src.models.machineModel import MachineManager
from src.models.userModel import auth, UserManager

pings_route = Blueprint("ping", __name__)

@pings_route.route("/")
@auth.login_required()
def ping():
    try:
        query = PingsManager.ping()
        if query[1] == 400:
            return jsonify(query[0]), 400
        for machine in query[0]:
            id = MachineManager.getMachineId(machine["machine"])
            if id[1] == 400:
                return jsonify(id[0]), 400
            PingsManager.addPings(pings=query[0], user=auth.current_user(), machine=id[0])
        return jsonify(query[0])
    except Exception as ex:
        return jsonify({"Message": str(ex)}), 500

@pings_route.route("/pings")
@auth.login_required()
def pings():
    try:
        query = PingsManager.getPings()
        if query[1] == 400:
            return jsonify(query[0]), 400
        for machine in query[0]:
            IP_check = MachineManager.getMachineIP(machine["machine"])
            machine.update({"machine": str(IP_check[0])})
            ping_from = UserManager.getUserEmail(execution=machine, model="ping_from")
            if ping_from[1] == 400:
                return jsonify(ping_from[0]), 400
            machine.update({"ping_from": str(ping_from[0])})
        return jsonify(query[0])
    except Exception as ex:
        return jsonify({"Message": str(ex)}), 500
