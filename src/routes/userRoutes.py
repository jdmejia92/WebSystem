from src.form.form import UserForm
from src.models.models import User, UserManager
from sqlalchemy import exc
from flask import jsonify, request, Blueprint, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from src import db

user = Blueprint("users", __name__)


@user.route("/", methods=["POST"])
def login():
    try:
        email = request.json["email"]
        password = request.json["password"]

        user_email = (
            User.query.filter_by(email=email)
            .with_entities(User.email, User.password)
            .scalar()
        )
        print(user_email)

        if user_email:
            return jsonify({"login": "success"})
        return jsonify({"message": "email or password invalid"})
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@user.route("/add", methods=["POST"])
def signUp():
    try:
        form = UserForm()
        email_request = request.json["email"]
        print(email_request)
        email = form.email.from_json(email_request)
        password = form.password(request.json["password"])
        priority = request.json["user"]

        user_email = User.query.filter_by(email=email).first()
        if email == user_email:
            return jsonify({"message": "The user already exists"})

        new_user = User(
            id=uuid.uuid4(),
            email=email,
            password=generate_password_hash(password),
            priority=priority,
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            return jsonify({"message": "User already exists"}), 400

        added_user = User.query.filter_by(email=email).first()

        if added_user.email == email:
            return jsonify({"message": "New user added"})
        return jsonify({"message": "No new user added"})

    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@user.route("/users")
def getUsers():
    try:
        users = UserManager.getUsers()
        if users:
            return jsonify(users)
        return jsonify({"message": "no users found"})
    except Exception as ex:
        return jsonify({"message": str(ex)})
