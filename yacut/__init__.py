from os.path import abspath

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config


app = Flask(
    __name__,
    template_folder=abspath('./html/templates'),
    static_url_path='',
    static_folder=abspath('./html/static')
)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import api_views, error_handlers, views
