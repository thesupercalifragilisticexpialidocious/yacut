from datetime import datetime
from random import choices
from re import compile

from . import db
from settings import (ALLOWED_CHARACTERS, CYCLE_DURATION,
                      DEFAULT_LENGTH, MAX_LENGTH, SHORT_MASK, URL_LIMIT)

ITERATION_LIMIT_HIT = 'Не удается найти незанятый короткий идентификатор.'
LONG_URL_ERROR = 'Исходная ссылка слишком длинная.'
INVALID_CUSTOM_ERROR = 'Указано недопустимое имя для короткой ссылки'
OCCUPIED_SHORT_ERROR = 'Имя "{}" уже занято.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(URL_LIMIT))
    short = db.Column(db.String(MAX_LENGTH), index=True, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_by_short(short):
        return URLMap.query.filter(URLMap.short == short).first()

    @staticmethod
    def generate_unique_short_id():
        for _ in range(CYCLE_DURATION):
            short = ''.join(choices(ALLOWED_CHARACTERS, k=DEFAULT_LENGTH))
            if not URLMap.get_by_short(short):
                return short
        raise AttributeError(ITERATION_LIMIT_HIT)

    @staticmethod
    def save(original, short=None, validated=False):
        if not validated:
            if len(original) > URL_LIMIT:
                raise ValueError(LONG_URL_ERROR)
            if short:
                if len(short) > MAX_LENGTH:
                    raise ValueError(INVALID_CUSTOM_ERROR)
                if not compile(SHORT_MASK).match(short):
                    raise ValueError(INVALID_CUSTOM_ERROR)
                if URLMap.get_by_short(short) is not None:
                    raise ValueError(OCCUPIED_SHORT_ERROR.format(short))
        instance = URLMap(
            original=original,
            short=short if short else URLMap.generate_unique_short_id()
        )
        db.session.add(instance)
        db.session.commit()
        return instance
