from src import db
from src.utils.Execution import ExecutionEditData
from src.database.db import Execution


def firstQuery(user, action, checked=None, machine=None):
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


class ExecutionManager:
    @classmethod
    def getExecutions(self):
        executions = []
        query = Execution.query.all()
        if query:
            for item in query:
                result = ExecutionEditData(
                    id=item.id,
                    user_id=item.user_id,
                    user_checked_id=item.user_id_checked,
                    machine_id=item.machine_id,
                    action_id=item.action_id,
                    datetime=item.datetime,
                )
                result = result.to_JSON()
                executions.append(result)
            return executions
        return 400

    @classmethod
    def getExecution(self, id):
        execution = []
        query = Execution.query.filter_by(id=id).scalar()
        if query:
            result = ExecutionEditData(
                id=query.id,
                user_id=query.user_id,
                user_checked_id=query.user_id_checked,
                machine_id=query.machine_id,
                action_id=query.action_id,
                datetime=query.datetime,
            )
            result = result.to_JSON()
            execution.append(result)
            return execution
        return 400

    @classmethod
    def queryUsers(self, user, current_action):
        query = Execution.query.filter(Execution.id == 1).first()
        if query:
            last_check = Execution.query.order_by(Execution.id.desc()).first()
            new_id = last_check.id + 1
            new_query = Execution(id=new_id, user_id=user.id, action_id=current_action)
            db.session.add(new_query)
            db.session.commit()
            return {"consult_id": new_id}
        else:
            consult = firstQuery(user=user, action=current_action)
            return consult

    @classmethod
    def queryUser(self, user, user_check, current_action):
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

    @classmethod
    def addUser(self, user, user_add, current_action):
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

    @classmethod
    def deleteUser(self, user, user_deleted, current_action):
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

    @classmethod
    def updateUser(self, user, user_updated, current_action):
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
