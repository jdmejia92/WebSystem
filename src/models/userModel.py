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
        if query:
            for item in query:
                result = UserEditData(
                    id=item.id,
                    email=item.email,
                    password=item.password,
                    priority=item.priority,
                    created_by=item.created_by
                )
                result = result.all_to_JSON()
                results.append(result)
            return results, 200
        return {"Message": "No users found"}, 400

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
                created_by=query.created_by
            )
            result = result.all_to_JSON()
            results.append(result)
            return results, 200
        return {"Message": "No user found"}, 400

    @classmethod
    def addUser(self, created_by, email=None, password=None, priority="user"):
        if User.query.filter_by(email=email).first():
            return {"message": "User already exists"}, 400
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
                created_by=created_by.id
            )
            db.session.add(new_user)
            db.session.commit()
            return {"id": id}, 200

    @classmethod
    def deleteUser(self, id):
        query = User.query.filter_by(id=id).scalar()
        if query:
            delete = User.query.filter(User.id == id).delete()
            if delete == 1:
                db.session.commit()
                return {"id": query.id}, 200
            return {"Message": "No user deleted"}, 400
        return {"Message": "No user found"}, 400

    @classmethod
    def updateUser(self, id, email, password, priority):
        query = User.query.filter_by(id=id).scalar()
        if query:
            if priority == "admin":
                priority = str(1)
            else:
                priority = str(2)
            result = User.query.filter(User.id == id).update(
                {
                    "email": email,
                    "password": generate_password_hash(password),
                    "priority": priority,
                }
            )
            if result == 1:
                db.session.commit()
                return {"id": query.id}, 200
            else:
                return {"message": "No user updated"}, 400
        return {"Message": "No user found"}, 400

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
                created_by="System"
            )
            db.session.add(new_user)
            db.session.commit()

    @classmethod
    def getUserEmail(self, execution, model):
        if model == "execution":
            for item in execution:
                query = User.query.filter_by(id=item["user"]).scalar()
                if query:
                    user = {"user": str(query.email)}
                    item.update(user)
                query_checked = User.query.filter_by(id=item["user_checked"]).scalar()
                if query_checked:
                    user = {"user_checked": str(query_checked.email)}
                    item.update(user)
            return execution
        else:
            for item in execution:
                query = User.query.filter_by(id=item["created_by"]).scalar()
                if query:
                    result = {"created_by": item["created_by"]} if query == None else {"created_by": str(query.email)}
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
