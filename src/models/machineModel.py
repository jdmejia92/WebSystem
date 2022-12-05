from src import db
from src.database.db import Machines
from flask import jsonify
from src.utils.Machine import MachineEditData
import uuid


class MachineManager:
    @classmethod
    def getMachines(self):
        results = []
        query = Machines.query.all()
        if query:
            for item in query:
                machine = MachineEditData(
                    id=item.id, machine=item.machine
                )
                machine = machine.to_JSON_machines()
                results.append(machine)
            return results
        return results

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
            return results
        return results

    @classmethod
    def addMachine(self, user_id, machine):
        query = Machines.query.filter_by(machine=machine).scalar()
        if query:
            return {"message": "Machine already registered"}
        else:
            id = uuid.uuid4()
            new_machine = Machines(id=id, machine=machine, created_by=user_id)
            db.session.add(new_machine)
            db.session.commit()
            return {"id": id}

    @classmethod
    def deleteMachine(self, id):
        query = Machines.query.filter_by(id=id).scalar()
        if query:
            db.session.delete(query)
            db.session.commit()
            return jsonify({"id": query.id})
        return {"message": "No user deleted"}
