from src.database.db import User
from src.utils.Users import UserEditData
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from src import db


auth = HTTPBasicAuth()


class UserManager:
    @classmethod
    def getUsers(self):
        results = []
        query = User.query.all()
        for item in query:
            result = UserEditData(
                id=item.id,
                email=item.email,
                password=item.password,
                priority=item.priority,
            )
            result = result.all_to_JSON()
            results.append(result)
        return results


    @classmethod
    def getUser(self, id):
        results = []
        query = User.query.filter_by(id=id).scalar()
        if query:
            result = UserEditData(
                id=query.id,
                email=query.email,
                password=query.password,
                priority=query.priority,
            )
            result = result.all_to_JSON()
            results.append(result)
            return results

    @classmethod
    def addUser(self, email=None, password=None, priority="user"):
        if User.query.filter_by(email=email).first():
            return 400
        else:
            id = uuid.uuid4()
            if priority == "admin":
                priority = 1
            else:
                priority = 2
            new_user = User(
                id=id,
                email=email,
                password=generate_password_hash(password),
                priority=priority,
            )
            db.session.add(new_user)
            db.session.commit()
            return {"id": id}

    @classmethod
    def deleteUser(self, id, user):
        query = User.query.filter_by(id=id).scalar()
        if query:
            db.session.delete(query)
            db.session.commit()
            return {"id": query.id}
        return 400

    @classmethod
    def updateUser(self, id, email, password, priority):
        query = User.query.filter_by(id=id).scalar()
        if query:
            if priority == "admin":
                priority = str(1)
            else:
                priority = str(2)
            result = (
                db.session.query(User)
                .filter(User.id == id)
                .update(
                    {
                        "email": email,
                        "password": generate_password_hash(password),
                        "priority": priority,
                    },
                    synchronize_session="fetch",
                )
            )
            if result == 1:
                db.session.commit()
                return {"id": query.id}
            else:
                return 400
        return 401

    @classmethod
    def login(self, email, password):
        query = User.query.filter_by(email=email).scalar()
        if query:
            if check_password_hash(query.password, password):
                return query


    @classmethod
    def firstUser(self):
        query = User.query.all()
        id = uuid.uuid4()
        if query == []:
            new_user = User(
                id=id,
                email="admin@system.com",
                password=generate_password_hash("123456"),
                priority=1,
            )
            db.session.add(new_user)
            db.session.commit()

    @classmethod
    def getUserEmail(self, execution, model):
        if model == "execution":
            for item in execution:
                id = item["user"]
                query = User.query.filter_by(id=id).scalar()
                result = {"user": str(query.email)}
                item.update(result)
        elif model == "system":
            for item in execution:
                id = item["created_by"]
                query = User.query.filter_by(id=id).scalar()
                result = {"created_by": str(query.email)}
                item.update(result)
        return execution


@auth.verify_password
def verify_password(email, password):
    query = User.query.filter_by(email=email).scalar()
    if query:
        if check_password_hash(query.password, password):
            return query


@auth.get_user_roles
def get_user_roles(user):
    query = User.query.filter_by(email=user.email).scalar()
    if query:
        return query.priority
