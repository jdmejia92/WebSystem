class MachineEditData:
    def __init__(self, id, machine, user_id=None):
        self.id = id
        self.machine = machine
        self.user_id = user_id


    def to_JSON_machines(self):
        return {"id": self.id, "machine": self.machine}

    def to_JSON_machine(self):
        return {"id": self.id, "machine": self.machine, "created_by": self.user_id}
