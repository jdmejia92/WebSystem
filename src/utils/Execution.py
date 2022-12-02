from src.database.db import Action, User


class ExecutionEditData:
    def __init__(self, id, user_id, user_checked_id, machine_id, action_id, datetime):
        self.id = id
        self.user_id = user_id
        self.user_checked_id = user_checked_id
        self.machine = machine_id
        self.action_id = action_id
        self.datetime = datetime

    def getAction(item):
        query = Action.query.filter_by(id=item).scalar()
        return query.action

    def getEmail(item):
        query = User.query.filter_by(id=item).scalar()
        return query.email

    def to_JSON(self):
        return {
            "id": self.id,
            "user": ExecutionEditData.getEmail(self.user_id),
            "user_checked_id": self.user_checked_id,
            "machine_id": self.machine,
            "action": ExecutionEditData.getAction(self.action_id),
            "datetime": self.datetime,
        }
