class EditPingData:
    def __init__(self, id, ping, date, machine, ping_from):
        self.id = id
        self.ping = ping
        self.date = date
        self.machine = machine
        self.ping_from = ping_from

    def all_Json(self):
        return {
            "id": self.id,
            "ping": self.ping,
            "date": self.date,
            "machine": self.machine,
            "ping_from": self.ping_from
        }
