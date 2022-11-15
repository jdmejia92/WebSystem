from src import db

def create_database():
    try:
        from src.models.models import User
        db.create_all()
    except Exception as ex:
        raise ex
