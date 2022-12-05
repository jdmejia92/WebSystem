from src.database.db import Action
from src.models.userModel import UserManager


class ExecutionEditData:
    def __init__(
        self, id, user_id, user_checked_id, machine_id, action_id, datetime
    ):
        self.id = id
        self.user_id = user_id
        self.user_checked_id = user_checked_id
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
            "user_checked_id": self.user_checked_id,
            "machine_id": self.machine,
            "action": ExecutionEditData.getAction(self.action_id),
            "datetime": self.datetime,
        }
