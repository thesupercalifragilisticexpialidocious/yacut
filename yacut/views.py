from flask import abort, redirect, render_template, url_for

from . import app
from .forms import LinkForm
from .models import URLMap
from settings import REDIRECT_VIEW


@app.route('/<string:short>')
def redirect_(short):
    relation = URLMap.get_by_short(short)
    if not relation:
        abort(404)
    return redirect(relation.original)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    return render_template(
        'index.html',
        form=form,
        success_link=url_for(
            REDIRECT_VIEW,
            short=URLMap.save(
                original=form.original_link.data,
                short=form.custom_id.data
            ).short,
            _external=True
        ) if form.validate_on_submit() else None
    )
