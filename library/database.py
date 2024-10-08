from library import db
from datetime import datetime


class DataBase(db.Model):
    __tablename__ = 'urls'  # Explicitly define table name

    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    hash_url = db.Column(db.String(8), nullable=False, unique=True)
    user_id = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)