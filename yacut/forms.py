from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional,
                                Regexp, ValidationError)

from .models import URLMap
from settings import ALLOWED_CHARACTERS, MAX_LENGTH, URL_LIMIT

SHORT_MASK = f'^[{ALLOWED_CHARACTERS}]+$'
ORIGINAL_PROMPT = 'Введите ссылку'
ORIGINAL_WARNING = 'Обязательное поле'
CUSTOM_PROMPT = 'Ваш вариант короткой ссылки'
CUSTOM_WARNING = 'Имя {} уже занято!'
SUBMIT_LABEL = 'Создать'


class LinkForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_PROMPT,
        validators=[DataRequired(message=ORIGINAL_WARNING),
                    Length(1, URL_LIMIT)]
    )
    custom_id = StringField(
        CUSTOM_PROMPT,
        validators=[Optional(), Length(1, MAX_LENGTH), Regexp(SHORT_MASK)]
    )
    submit = SubmitField(SUBMIT_LABEL)

    def validate_custom_id(form, field):
        if URLMap.get_by_short(field.data):
            raise ValidationError(CUSTOM_WARNING.format(field.data))
