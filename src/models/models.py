from flask_login import UserMixin
from src.utils.Users import UserEditData
from src import db


class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    priority = db.Column(db.String(20), nullable=False)


class UserManager:
    @classmethod
    def getUsers(self):
        results = []
        query = User.query.all()
        for user in query:
            result = UserEditData(
                id=user.id,
                email=user.email,
                password=user.password,
                priority=user.priority,
            )
            result = result.all_to_JSON()
            results.append(result)
        return results

