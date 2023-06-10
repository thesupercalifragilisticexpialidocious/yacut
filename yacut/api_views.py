from flask import jsonify, request, url_for

from . import app
from .exceptions import InvalidAPIUsage
from .models import URLMap
from settings import ALLOWED_CHARACTERS, MAX_LENGTH, REDIRECT_VIEW


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

    original = data['url']
    if 'custom_id' not in data or not data['custom_id']:
        relation = URLMap.save(original)

    elif (not all(char in ALLOWED_CHARACTERS for char in data['custom_id']) or
          len(data['custom_id']) > MAX_LENGTH):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    elif URLMap.get_by_short(data['custom_id']) is not None:
        raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
    else:
        relation = URLMap.save(original=original, short=data['custom_id'])

    return jsonify({
        'url': relation.original,
        'short_link': url_for(
            REDIRECT_VIEW,
            short=relation.short,
            _external=True
        )
    }), 201
