from src.database.db import Priority


class UserEditData:
    def __init__(self, id=None, email=None, password=None, priority=None, created_by=None):
        self.id = id
        self.email = email
        self.password = password
        self.priority = priority
        self.created_by=created_by

    def getPriority(item):
        query = Priority.query.filter_by(id=item).scalar()
        return query.priority

    def all_to_JSON(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "priority": UserEditData.getPriority(self.priority),
            "created_by": self.created_by
        }
