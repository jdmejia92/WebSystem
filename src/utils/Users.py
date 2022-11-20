class UserEditData():
    def __init__(self, id, email=None, password=None, priority=None):
        self.id = id
        self.email = email
        self.password = password
        self.priority = priority

    def all_to_JSON(self):
        return {"id": self.id, "email": self.email, "password": self.password, 'priority': self.priority}
