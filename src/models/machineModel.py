from src import db
from src.database.db import Machines
from flask import jsonify
from src.utils.Machine import MachineEditData
import uuid


class MachineManager:
    @classmethod
    def getMachines(self):
        try:
            results = []
            query = Machines.query.all()
            if query:
                for item in query:
                    machine = MachineEditData(
                        id=item.id, machine=item.machine, user_id=item.created_by
                    )
                    machine = machine.to_JSON()
                    results.append(machine)
                return results
            return jsonify({"message": "No machines found"})
        except Exception as ex:
            return jsonify({"message": str(ex)}), 500

    @classmethod
    def addMachine(self, user_id, machine):
        try:
            query = Machines.query.filter_by(machine=machine).scalar()
            if query:
                return jsonify({"message": "Machine already exists"})
            else:
                
                id = uuid.uuid4()
                new_machine = Machines(id=id, machine=machine, created_by=user_id)
                db.session.add(new_machine)
                db.session.commit()
                return jsonify({"id": id})
        except Exception as ex:
            return jsonify({"message": str(ex)})

    @classmethod
    def deleteMachine(self, id):
        try:
            query = Machines.query.filter_by(id=id).scalar()
            if query:
                db.session.delete(query)
                db.session.commit()
                return jsonify({"id": query.id})
            return jsonify({"message": "No user deleted"}), 400
        except Exception as ex:
            return jsonify({"message": str(ex)})
