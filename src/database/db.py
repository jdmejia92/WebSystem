from src import db, app


def create_database():
    try:
        from src.models.models import User

        with app.app_context():
            db.create_all()
    except Exception as ex:
        raise ex
