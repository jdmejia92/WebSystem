

class MachineEditData:
    def __init__(self, id, machine, user_id):
        self.id = id
        self.machine = machine
        self.user_id = user_id


    def to_JSON(self):
        return {"id": self.id, "machine": self.machine, "user": self.user_id}
