from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import LinkForm
from .models import URLMap

MAX = 62 ** 6
RADIX = 62
DIGITS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_unique_short_id(link):
    def to_duosexagesimal(number):
        '''0-9a-zA-Z reprentation, but reversed (smallest place goes first).
        Comes with padding for result to be six-digit-long.'''
        result = []
        while number:
            result.append(DIGITS[number % RADIX])
            number = number // RADIX
        return ''.join(result) + '0' * (6 - len(result))

    link_hash = hash(link)
    recent = URLMap.query.order_by(URLMap.id.desc()).first()
    id = recent.id if recent else 1
    while True:
        id = (link_hash * id + 1) % MAX
        short = to_duosexagesimal(id)
        if URLMap.query.filter(URLMap.short == short).first():
            continue
        return short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    relation = None
    if form.validate_on_submit():
        original = form.original_link.data
        custom = form.custom_id.data
        if not custom:
            relation = URLMap(
                original=original,
                short=get_unique_short_id(original)
            )
        elif URLMap.query.filter_by(short=custom).first() is None:
            relation = URLMap(original=original, short=custom)
        else:
            flash(f'Имя {custom} уже занято!', category='error')
        if relation:
            db.session.add(relation)
            db.session.commit()
            flash(
                url_for("redirect_", short=relation.short, _external=True),
                category='success'
            )
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirect_(short):
    relation = URLMap.query.filter(URLMap.short == short).first()
    if not relation:
        abort(404)
    return redirect(relation.original)
