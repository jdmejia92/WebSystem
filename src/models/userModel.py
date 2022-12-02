from src.database.db import User
from src.utils.Users import UserEditData
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask import jsonify
from src import db
from src.models.executionModel import ExecutionManager


auth = HTTPBasicAuth()


class UserManager:
    @classmethod
    def getUsers(self, user):
        try:
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
            consult = ExecutionManager.queryUsers(user=user, current_action=1)
            results.append(consult)
            return jsonify(results)
        except Exception as ex:
            return jsonify({"message": str(ex)}), 500

    @classmethod
    def getUser(self, id, user):
        try:
            results = []
            query = User.query.filter_by(id=id).scalar()
            result = UserEditData(
                id=query.id,
                email=query.email,
                password=query.password,
                priority=query.priority,
            )
            result = result.all_to_JSON()
            results.append(result)
            consult = ExecutionManager.queryUser(
                user=user, user_check=query.id, current_action=2
            )
            results.append(consult)
            return jsonify(results)
        except Exception as ex:
            return jsonify({"message": str(ex)}), 500

    @classmethod
    def addUser(self, user, email=None, password=None, priority="user"):
        try:
            if User.query.filter_by(email=email).first():
                return jsonify({"message": "User already exists"}), 400
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
            consult = ExecutionManager.addUser(user=user, user_add=id, current_action=3)
            return jsonify({"id": id} | consult)
        except Exception as ex:
            return jsonify({"message": ex}), 500

    @classmethod
    def deleteUser(self, id, user):
        try:
            query = User.query.filter_by(id=id).scalar()
            if query:
                db.session.delete(query)
                db.session.commit()
                consult = ExecutionManager.deleteUser(
                    user=user, user_deleted=query.id, current_action=4
                )
                return jsonify({"id": query.id} | consult)
            return jsonify({"message": "No user deleted"}), 400
        except Exception as ex:
            return jsonify({"message": str(ex)}), 500

    @classmethod
    def updateUser(self, user, id, email, password, priority):
        try:
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
                    consult = ExecutionManager.updateUser(
                        user=user, user_updated=query.id, current_action=5
                    )
                    db.session.commit()
                    return jsonify({"id": query.id} | consult)
                else:
                    return jsonify({"message": "No user updated"}), 400
            return jsonify({"message": "No user found to update"}), 400
        except Exception as ex:
            return jsonify({"message": str(ex)}), 500

    @classmethod
    def login(self, email, password):
        try:
            query = User.query.filter_by(email=email).scalar()
            if query:
                if check_password_hash(query.password, password):
                    return query
        except Exception as ex:
            return jsonify({"message": str(ex)})

    @classmethod
    def firstUser(self):
        try:
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
        except Exception as ex:
            print(str(ex))


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
