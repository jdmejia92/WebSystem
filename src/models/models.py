from flask_login import UserMixin
from src import db

class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    priority = db.Column(db.String(20), nullable=False)

