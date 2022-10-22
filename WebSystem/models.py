from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class DataManager():
    def __init__(self, file=":memory:"):
        self.data_origin = file
    pass


class User(UserMixin):
    def __init__(self, email, password, is_admin=False):
        return check_password_hash(self.password,password)