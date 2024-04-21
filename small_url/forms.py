from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired, Length, Optional, Regexp, URL, ValidationError
)

from .constants import MAX_SHORT_LENGTH, ORIGINAL_LINK_LENGTH, PATTERN
from .models import URLMap, SHORT_OPTION_IS_BUSY

BUTTON = 'Создать'
INVALID_LINK = 'Нерабочая ссылка'
LONG_LINK = 'Длинная ссылка'
REQUIRED_FIELD = 'Обязательное поле'
SHORT_OPTION = 'Ваш вариант короткой ссылки'
VALID_SYMBOLS = 'В качестве символов используйте цифры и латинский алфавит.'


class URLMapForm(FlaskForm):
    original_link = URLField(
        LONG_LINK,
        validators=[
            DataRequired(message=REQUIRED_FIELD),
            Length(max=ORIGINAL_LINK_LENGTH),
            URL(message=INVALID_LINK)
        ]
    )
    custom_id = StringField(
        SHORT_OPTION,
        validators=[
            Regexp(regex=PATTERN, message=VALID_SYMBOLS),
            Length(max=MAX_SHORT_LENGTH),
            Optional()
        ]
    )
    submit = SubmitField(BUTTON)

    def validate_custom_id(self, short):
        if short.data and URLMap.get(short.data):
            raise ValidationError(SHORT_OPTION_IS_BUSY.format(short.data))
