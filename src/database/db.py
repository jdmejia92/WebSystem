from src import db, app
from sqlalchemy.sql import func


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    priority = db.Column(db.Integer, db.ForeignKey("priority.id"), nullable=False)


class Priority(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    priority = db.Column(db.String(20), nullable=False)


class Execution(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    user_id_checked = db.Column(db.String(36))
    machine_id = db.Column(db.String(36), db.ForeignKey("machines.id"))
    action_id = db.Column(db.Integer(), db.ForeignKey("action.id"))
    datetime = db.Column(db.DateTime(), nullable=False, server_default=func.now())


class Action(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    action = db.Column(db.String(50), unique=True)


class Machines(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    machine = db.Column(db.String(15), unique=True, nullable=False)
    created_by = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)


class Pings(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    ping = db.Column(db.Float(), nullable=False)
    date = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    ping_from = db.Column(db.String(36), db.ForeignKey("machines.id"), nullable=False)


def create_database():
    try:
        from src.models.userModel import UserManager

        with app.app_context():
            db.create_all()
            query = Priority.query.first()
            if query == None:
                user = Priority(priority="user")
                admin = Priority(priority="admin")
                db.session.add(admin)
                db.session.add(user)
                query_all_users = Action(action="Revisó a todos los usuarios")
                query_one_user = Action(action="Revisó un usuario")
                add_user = Action(action="Añadió un usuario")
                delete_user = Action(action="Borro un usuario")
                update_user = Action(action="Actualizó un usuario")
                db.session.add(query_all_users)
                db.session.add(query_one_user)
                db.session.add(add_user)
                db.session.add(delete_user)
                db.session.add(update_user)
                db.session.commit()
            UserManager.firstUser()
    except Exception as ex:
        raise ex
