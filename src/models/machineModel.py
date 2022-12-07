from src import db
from src.database.db import Machines, Pings
from flask import jsonify
from src.utils.Machine import MachineEditData
import uuid
from pythonping import ping


class MachineManager:
    @classmethod
    def getMachines(self):
        results = []
        query = Machines.query.all()
        if query:
            for item in query:
                machine = MachineEditData(id=item.id, machine=item.machine)
                machine = machine.to_JSON_machines()
                results.append(machine)
            return results, 200
        return {"Message": "No machines found"}, 400

    @classmethod
    def getMachine(self, id):
        results = []
        query = Machines.query.filter_by(id=id).scalar()
        if query:
            machine = MachineEditData(
                id=query.id, machine=query.machine, user_id=query.created_by
            )
            machine = machine.to_JSON_machine()
            results.append(machine)
            return results, 200
        return {"Message": "No machine found"}, 400

    @classmethod
    def addMachine(self, user_id, machine):
        query = Machines.query.filter_by(machine=machine).scalar()
        if query:
            return {"message": "Machine already registered"}, 400
        else:
            id = uuid.uuid4()
            new_machine = Machines(id=id, machine=machine, created_by=user_id)
            db.session.add(new_machine)
            db.session.commit()
            return {"id": id}, 200

    @classmethod
    def deleteMachine(self, id):
        query = Machines.query.filter_by(id=id).scalar()
        if query:
            delete = Machines.query.filter(Machines.id == id).delete()
            if delete == 1:
                db.session.commit()
                return {"id": query.id}, 200
            return {"Message": "No machine deleted"}, 400
        return {"Message": "No machine found"}, 400

    @classmethod
    def updateMachine(self, id, machine):
        query = Machines.query.filter_by(id=id).scalar()
        if query:
            result = Machines.query.filter(Machines.id == id).update(
                {
                    "machine": machine,
                }
            )
            if result == 1:
                db.session.commit()
                return {"id": query.id}, 200
            return {"Message": "No machine updated"}, 400
        return {"Message": "No machine deleted"}, 400


class PingsManager:
    @classmethod
    def ping(self):
        machines = MachineManager.getMachines()
        if machines:
            pings_list = []
            for machine in machines:
                pings = ping(machine["machine"], verbose=True)
                pings_dict = {
                    machine["machine"]: "timed out"
                    if pings.rtt_avg_ms == 2000
                    else pings.rtt_avg_ms
                }
                pings_list.append(pings_dict)
            return pings_list, 200
        return {"Message": "No machines found"}, 400
