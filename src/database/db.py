from src import db, app


def create_database():
    try:
        from src.models.userModel import User, Priority, UserManager
        from src.models.machineModel import Machines, Pings
        from src.models.executionModel import Execution, Action

        with app.app_context():
            db.create_all()
            query = Priority.query.first()
            if query == None:
                user = Priority(priority="user")
                admin = Priority(priority="admin")
                db.session.add(admin)
                db.session.add(user)
                query_all = Action(action="getAll")
                query_one = Action(action="getOne")
                add = Action(action="add")
                delete = Action(action="delete")
                update = Action(action="update")
                db.session.add(query_all)
                db.session.add(query_one)
                db.session.add(add)
                db.session.add(delete)
                db.session.add(update)
                db.session.commit()
            UserManager.firstUser()
    except Exception as ex:
        raise ex
