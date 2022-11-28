from src.utils.Users import UserEditData
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask import jsonify
from src import db


auth = HTTPBasicAuth()


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    priority = db.Column(
        db.Integer, db.ForeignKey("priority.priority_id"), nullable=False
    )


class Priority(db.Model):
    priority_id = db.Column(db.Integer(), primary_key=True)
    priority = db.Column(db.String(20), nullable=False)


class UserManager:
    @classmethod
    def getUsers(self):
        try:
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
        except Exception as ex:
            return jsonify({"message": str(ex)}), 500

    @classmethod
    def getUser(self, id):
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
            return results
        except Exception as ex:
            return jsonify({"message": str(ex)}), 500

    @classmethod
    def addUser(self, email=None, password=None, priority="user"):
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
            return jsonify({"id": id})
        except Exception as ex:
            return jsonify({"message": ex}), 500

    @classmethod
    def deleteUser(self, id):
        try:
            query = User.query.filter_by(id=id).scalar()
            if query:
                db.session.delete(query)
                db.session.commit()
                return jsonify({"id": query.id})
            return jsonify({"message": "No user deleted"}), 400
        except Exception as ex:
            return jsonify({"message": str(ex)}), 500

    @classmethod
    def updateUser(self, id, email, password, priority):
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
                    db.session.commit()
                    return jsonify({"id": query.id})
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
