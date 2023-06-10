from os import getenv
from string import ascii_letters, digits

MAX_LENGTH = 16
URL_LIMIT = 2048
DEFAULT_LENGTH = 6
ALLOWED_CHARACTERS = ascii_letters + digits
CYCLE_DURATION = len(ALLOWED_CHARACTERS) ** DEFAULT_LENGTH
REDIRECT_VIEW = 'redirect_'


class Config(object):
    SQLALCHEMY_DATABASE_URI = getenv(
        'DATABASE_URI',
        default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv('SECRET_KEY', default='MY_VERY_SECURE_KEY')
