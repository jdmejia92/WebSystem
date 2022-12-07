from src.form.form import UserForm
from src.models.userModel import UserManager, auth
from src.models.executionModel import ExecutionManager
from flask import jsonify, request, Blueprint


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
        if users[1] == 400:
            return jsonify(users[0]), 400
        email = UserManager.getUserEmail(execution=users[0], model="user")
        return jsonify(email)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@user.route("/user/<id>", methods=["GET"])
@auth.login_required(role=1)
def getUser(id):
    try:
        user = UserManager.getUser(id)
        if user[1] == 400:
            return jsonify(user[0])
        email = UserManager.getUserEmail(execution=user[0], model="user")
        return jsonify(email)
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
                priority=form.data["priority"],
                created_by=auth.current_user()
            )
            if id[1] == 400:
                return jsonify(id[0]), 400
            ExecutionManager.queryUser(
                user=auth.current_user(), user_checked=id[0]["id"], current_action=1
            )
            return jsonify(id[0])
        return jsonify(form.errors), 400
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@user.route("/delete/<id>", methods=["DELETE"])
@auth.login_required(role=1)
def delete(id):
    try:
        deleting = UserManager.deleteUser(id)
        if deleting[1] == 400:
            return jsonify(deleting[0]), 400
        ExecutionManager.queryUser(
            user=auth.current_user(), user_checked=deleting[0]["id"], current_action=2
        )
        return jsonify(deleting[0])
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
                priority=form.data["priority"],
            )
            if updating[1] == 400:
                return jsonify(updating[0]), 400
            ExecutionManager.queryUser(
                user=auth.current_user(),
                user_checked=updating[0]["id"],
                current_action=3,
            )
            return jsonify(updating[0])
        else:
            return jsonify({"message": str(form.errors)}), 400
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
