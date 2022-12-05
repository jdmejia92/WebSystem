from src.form.form import UserForm
from src.models.userModel import UserManager, auth
from src.models.executionModel import ExecutionManager
from flask import jsonify, request, Blueprint, redirect, url_for


user = Blueprint("users", __name__)


@user.route("/", methods=["POST"])
def login():
    try:
        info = request.json
        query = UserManager.login(email=info["email"], password=info["password"])
        if query:
            return jsonify({"email": query.email, "password": info["password"]})
        return jsonify({"message": "User o password invalid"}), 403
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@user.route("/users", methods=["GET"])
@auth.login_required(role=1)
def getUsers():
    try:
        users = UserManager.getUsers()
        if users:
            ExecutionManager.queryUsers(user=auth.current_user(), current_action=1)
            return jsonify(users)
        return jsonify({"message": "no users found"}), 400
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@user.route("/user/<id>", methods=["GET"])
@auth.login_required(role=1)
def getUser(id):
    try:
        user = UserManager.getUser(id)
        if user:
            ExecutionManager.queryUser(user=auth.current_user(), user_check=id, current_action=2)
            return jsonify(user)
        return jsonify({"message": "no user found"}), 400
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@user.route("/add", methods=["POST"])
@auth.login_required(role=1)
def signUp():
    try:
        form = UserForm.from_json(request.json, skip_unknown_keys=False)
        if form.validate():
            id = UserManager.addUser(
                email=form.data["email"],
                password=form.data["password"],
                priority=form.data["priority"]
            )
            if id == 400:
                return jsonify({"message": "User already exists"})
            ExecutionManager.addUser(user=auth.current_user(), user_add=id["id"], current_action=3)
            return jsonify(id)
        return jsonify(form.errors), 400
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@user.route("/delete/<id>", methods=["DELETE"])
@auth.login_required(role=1)
def delete(id):
    try:
        deleting = UserManager.deleteUser(id, user=auth.current_user())
        if deleting == 400:
            return jsonify({"message": "No user deleted"})
        ExecutionManager.deleteUser(user=auth.current_user(), user_deleted=deleting["id"], current_action=4)
        return deleting
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@user.route("/update/<id>", methods=["PUT"])
@auth.login_required(role=1)
def update(id):
    try:
        form = UserForm.from_json(request.json, skip_unknown_keys=False)
        if form.validate():
            updating = UserManager.updateUser(
                id=id,
                email=form.data["email"],
                password=form.data["password"],
                priority=form.data["priority"]
            )
            if updating == 400:
                return jsonify({"message": "No user updated"})
            elif updating == 401:
                return jsonify({"message": "No user found"})
            ExecutionManager.updateUser(user=auth.current_user(), user_updated=updating["id"], current_action=5)
            return updating
        else:
            return jsonify({"message": str(form.errors)}), 400
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
