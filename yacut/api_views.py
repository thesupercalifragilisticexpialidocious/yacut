from flask import jsonify, request, url_for

from . import app
from .exceptions import InvalidAPIUsage
from .models import URLMap
from settings import REDIRECT_VIEW

NO_BODY_WARNING = 'Отсутствует тело запроса'
URL_REQUIRED_WARNING = '"url" является обязательным полем!'
ID_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    relation = URLMap.get_by_short(short_id)
    if relation is None:
        raise InvalidAPIUsage(ID_NOT_FOUND, 404)
    return jsonify({'url': relation.original}), 200


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(NO_BODY_WARNING)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_REQUIRED_WARNING)
    try:
        return jsonify({
            'url': data['url'],
            'short_link': url_for(
                REDIRECT_VIEW,
                short=URLMap.save(
                    data.get('url'),
                    data.get('custom_id')
                ).short,
                _external=True
            )
        }), 201
    except ValueError as e:
        raise InvalidAPIUsage(str(e))
