from src import db, app


def create_database():
    try:
        from src.models.userModel import User, Priority
        from src.models.machineModel import Machines

        with app.app_context():
            db.create_all()
            query = Priority.query.first()
            if query == None:
                user = Priority(priority="user")
                admin = Priority(priority="admin")
                db.session.add(admin)
                db.session.add(user)
                db.session.commit()
    except Exception as ex:
        raise ex
