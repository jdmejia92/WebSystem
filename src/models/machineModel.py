from src import db
from src.database.db import Machines
from src.utils.Machine import MachineEditData
import uuid


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
        query = Machines.query.filter_by(id=id).scalar()
        if query:
            machine = MachineEditData(
                id=query.id, machine=query.machine, user_id=query.created_by
            )
            machine = machine.to_JSON_machine()
            return machine, 200
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

    @classmethod
    def getMachineId(self, machine):
        machine_id = Machines.query.filter_by(machine=machine).scalar()
        if machine_id:
            return {"id": machine_id.id, "machine": machine_id.machine}, 200
        return {"message": "No machine found"}, 400

    @classmethod
    def getMachineIP(self, id):
        machine_IP = Machines.query.filter_by(id=id).scalar()
        if machine_IP:
            return machine_IP.machine, 200
        return {"message": "No machine found"}, 400
