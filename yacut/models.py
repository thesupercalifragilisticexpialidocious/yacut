from datetime import datetime

from . import db

MAX_LENGTH = 16


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(2048))
    short = db.Column(db.String(MAX_LENGTH), index=True, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
