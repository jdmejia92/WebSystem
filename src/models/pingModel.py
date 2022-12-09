from src.models.machineModel import MachineManager
from src import db
from src.database.db import Pings
from src.utils.Pings import EditPingData
from pythonping import ping


class PingsManager:
    @classmethod
    def ping(self):
        machines = MachineManager.getMachines()
        if machines[1] == 400:
            return {"Message": "No machines found"}, 400
        pings_list = []
        query = Pings.query.filter(Pings.id == 1).first()
        for machine in machines[0]:
            pings = ping(machine["machine"], verbose=True)
            pings_dict = {
                "machine": machine["machine"],
                "ping": "No respond" if pings.rtt_avg_ms == 2000 else pings.rtt_avg_ms,
            }
            pings_list.append(pings_dict)
        return pings_list, 200

    @classmethod
    def addPings(self, pings, user, machine):
        for ping in pings:
            query = Pings.query.filter(Pings.id == 1).first()
            if query == None:
                new_id = 1
            else:
                id = Pings.query.order_by(Pings.id.desc()).first()
                new_id = id.id + 1
            if ping["machine"] == machine["machine"]:
                new_ping = Pings(id=new_id, ping=ping["ping"], machine=machine["id"], ping_from=user.id)
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