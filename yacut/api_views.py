from flask import jsonify, request, url_for

from . import app
from .exceptions import InvalidAPIUsage
from .models import URLMap
from settings import REDIRECT_VIEW


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    relation = URLMap.get_by_short(short_id)
    if relation is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': relation.original}), 200


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage(r'"url" является обязательным полем!')
    try:
        relation = URLMap.save(data.get('url'), data.get('custom_id'))
    except ValueError as e:
        raise InvalidAPIUsage(str(e))
    return jsonify({
        'url': relation.original,  # relation once
        'short_link': url_for(
            REDIRECT_VIEW,
            short=relation.short,  # relation twice
            _external=True
        )
    }), 201
