from re import compile

from flask import jsonify, request, url_for

from . import app, db
from .exceptions import InvalidAPIUsage
from .forms import SHORT_MASK
from .models import MAX_LENGTH, URLMap
from .views import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    relation = URLMap.query.filter_by(short=short_id).first()
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
        relation = URLMap(
            original=original,
            short=get_unique_short_id(original)
        )
    elif (not compile(SHORT_MASK).match(data['custom_id']) or
          len(data['custom_id']) > MAX_LENGTH):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    elif URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
    else:
        relation = URLMap(original=original, short=data['custom_id'])
    db.session.add(relation)
    db.session.commit()
    return jsonify({
        'url': relation.original,
        'short_link': url_for('redirect_', short=relation.short, _external=True)
    }), 201
