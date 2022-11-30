from src import db
from sqlalchemy.sql import func


class Execution(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    user_id_checked = db.Column(db.String(36))
    machine_id = db.Column(db.String(36), db.ForeignKey("machines.id"))
    action_id = db.Column(db.Integer(), db.ForeignKey("action.id"))
    datetime = db.Column(db.DateTime(), nullable=False, server_default=func.now())


class Action(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    action = db.Column(db.String(20), unique=True)


def firstQuery(user, action, checked=None, machine=None):
    try:
        id = 1
        new_query = Execution(
            id=id,
            user_id=user.id,
            action_id=action,
            user_id_checked=checked,
            machine_id=machine,
        )
        db.session.add(new_query)
        db.session.commit()
        return {"id": id}
    except Exception as ex:
        return {"message": str(ex)}


class ExecutionManager:
    @classmethod
    def queryUsers(self, user, current_action):
        try:
            query = Execution.query.filter(Execution.id == 1).first()
            if query:
                last_check = Execution.query.order_by(Execution.id.desc()).first()
                new_id = last_check.id + 1
                new_query = Execution(
                    id=new_id, user_id=user.id, action_id=current_action
                )
                db.session.add(new_query)
                db.session.commit()
                return {"consult_id": new_id}
            else:
                consult = firstQuery(user=user, action=current_action)
                return consult
        except Exception as ex:
            return {"message": str(ex)}

    @classmethod
    def queryUser(self, user, user_check, current_action):
        try:
            query = Execution.query.filter(Execution.id == 1).first()
            if query:
                last_check = Execution.query.order_by(Execution.id.desc()).first()
                new_id = last_check.id + 1
                new_query = Execution(
                    id=new_id,
                    user_id=user.id,
                    action_id=current_action,
                    user_id_checked=user_check,
                )
                db.session.add(new_query)
                db.session.commit()
                return {"consult_number": new_id}
            else:
                consult = firstQuery(user=user, action=current_action, checked=user_check)
                return consult
        except Exception as ex:
            return {"message": str(ex)}

    @classmethod
    def addUser(self, user, user_add, current_action):
        try:
            query = Execution.query.filter(Execution.id == 1).first()
            if query:
                last_check = Execution.query.order_by(Execution.id.desc()).first()
                new_id = last_check.id + 1
                new_query = Execution(
                    id=new_id,
                    user_id=user.id,
                    action_id=current_action,
                    user_id_checked=user_add,
                )
                db.session.add(new_query)
                db.session.commit()
                return {"consult_number": new_id}
            else:
                consult = firstQuery(user=user, action=current_action, checked=user_add)
                return consult
        except Exception as ex:
            return {"message": str(ex)}

    @classmethod
    def deleteUser(self, user, user_deleted, current_action):
        try:
            query = Execution.query.filter(Execution.id == 1).first()
            if query:
                last_check = Execution.query.order_by(Execution.id.desc()).first()
                new_id = last_check.id + 1
                new_query = Execution(
                    id=new_id,
                    user_id=user.id,
                    action_id=current_action,
                    user_id_checked=user_deleted,
                )
                db.session.add(new_query)
                db.session.commit()
                return {"consult_number": new_id}
            else:
                consult = firstQuery(user=user, action=current_action, checked=user_deleted)
                return consult
        except Exception as ex:
            return {"message": str(ex)}


    @classmethod
    def updateUser(self, user, user_updated, current_action):
        try:
            query = Execution.query.filter(Execution.id == 1).first()
            if query:
                last_check = Execution.query.order_by(Execution.id.desc()).first()
                new_id = last_check.id + 1
                new_query = Execution(
                    id=new_id,
                    user_id=user.id,
                    action_id=current_action,
                    user_id_checked=user_updated,
                )
                db.session.add(new_query)
                db.session.commit()
                return {"consult_number": new_id}
            else:
                consult = firstQuery(user=user, action=current_action, checked=user_updated)
                return consult
        except Exception as ex:
            return {"message": str(ex)}
