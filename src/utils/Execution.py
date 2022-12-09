from src.database.db import Action


class ExecutionEditData:
    def __init__(self, id, user_id, user_id_target, machine_id, action_id, datetime):
        self.id = id
        self.user_id = user_id
        self.user_id_target = user_id_target
        self.machine = machine_id
        self.action_id = action_id
        self.datetime = datetime

    def getAction(action):
        result = Action.query.filter_by(id=action).scalar()
        return result.action

    def to_JSON(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "user_checked": self.user_id_target,
            "machine_id": self.machine,
            "action": ExecutionEditData.getAction(self.action_id),
            "datetime": self.datetime,
        }
