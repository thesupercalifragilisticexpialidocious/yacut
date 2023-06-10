from datetime import datetime
from random import choices

from . import db
from settings import (ALLOWED_CHARACTERS, CYCLE_DURATION,
                      DEFAULT_LENGTH, MAX_LENGTH, URL_LIMIT)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(URL_LIMIT))
    short = db.Column(db.String(MAX_LENGTH), index=True, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def get_by_short(cls, string):
        return cls.query.filter(cls.short == string).first()

    @staticmethod
    def generate_unique_short_id():
        for _ in range(CYCLE_DURATION):
            short = ''.join(choices(ALLOWED_CHARACTERS, k=DEFAULT_LENGTH))
            if URLMap.get_by_short(short):
                continue
            return short
        raise StopIteration(
            'Не удается найти незанятый короткий идентификатор.'
        )

    @classmethod
    def save(cls, original, short=None):
        instance = URLMap(
            original=original,
            short=short if short else cls.generate_unique_short_id()
        )
        db.session.add(instance)
        db.session.commit()
        return instance
