from src import db
from src.database.db import Machines, Pings
from src.utils.Pings import EditPingData
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
        if machines[1] == 400:
            return {"Message": "No machines found"}, 400
        pings_list = []
        query = Pings.query.filter(Pings.id == 1).first()
        print(query)
        for machine in machines[0]:
            pings = ping(machine["machine"], verbose=True)
            pings_dict = {
                "Machine": machine["machine"],
                "Ping": "No respond" if pings.rtt_avg_ms == 2000 else pings.rtt_avg_ms,
            }
            pings_list.append(pings_dict)
        return pings_list, 200

    @classmethod
    def addPings(self, pings, user):
        for ping in pings:
            query = Pings.query.filter(Pings.id == 1).first()
            if query == None:
                new_id = 1
            else:
                id = Pings.query.order_by(Pings.id.desc()).first()
                new_id = id.id + 1
            machine_id = Machines.query.filter_by(machine = ping["Machine"]).scalar()
            new_ping = Pings(id=new_id, ping=ping["Ping"], machine=machine_id.id, ping_from=user.id)
            db.session.add(new_ping)
            db.session.commit()

    @classmethod
    def getPings(self):
        query = Pings.query.all()
        if query:
            results = []
            for item in query:
                result = EditPingData(
                    id=item.id,
                    ping=item.ping,
                    date=item.date,
                    machine=item.machine,
                    ping_from=item.ping_from
                )
                result = result.all_Json()
                results.append(result)
            return results, 200
        return {"Message": "No pings found"}, 400

