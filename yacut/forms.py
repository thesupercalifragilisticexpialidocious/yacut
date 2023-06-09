from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .models import MAX_LENGTH

SHORT_MASK = r'^[a-zA-Z0-9]+$'


class LinkForm(FlaskForm):
    original_link = URLField(
        'Введите ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 2048)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, MAX_LENGTH), Regexp(SHORT_MASK), Optional()]
    )
    submit = SubmitField('Создать')
