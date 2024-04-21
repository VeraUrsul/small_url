from datetime import datetime
import random
import re

from flask import url_for

from small_url import db
from .constants import (
    ATTEMPTS_TO_CREATE_SHORT, MAX_SHORT_LENGTH,
    GENERATED_SHORT_LENGTH, ORIGINAL_LINK_LENGTH, PATTERN,
    READDRESING_FUNCTION, SYMBOLS
)

FIASCO = 'Попробуйте ещё раз создать короткую ссылку или напишите свой вариант'
INVALID_SHORT_NAME = 'Указано недопустимое имя для короткой ссылки'
TOO_LONG_ORIGINAL_LINK = 'Слишком много символов в длинной ссылке'
SHORT_OPTION_IS_BUSY = 'Предложенный вариант короткой ссылки уже существует.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                READDRESING_FUNCTION, short=self.short, _external=True
            )
        )

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404()

    @staticmethod
    def get(short):
        """Получение объекта класса URLMap по идентификатору из базы."""
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short():
        """Генерация уникального идентификатора из 6 случайных символов."""
        for _ in range(ATTEMPTS_TO_CREATE_SHORT):
            short = ''.join(random.choices(SYMBOLS, k=GENERATED_SHORT_LENGTH))
            if not URLMap.get(short):
                return short
        raise ValueError(FIASCO)

    @staticmethod
    def create(original, short, need_validate=True):
        if need_validate and ORIGINAL_LINK_LENGTH < len(original):
            raise ValueError(TOO_LONG_ORIGINAL_LINK)
        if need_validate and short:
            if MAX_SHORT_LENGTH < len(short):
                raise ValueError(INVALID_SHORT_NAME)
            if not re.match(PATTERN, short):
                raise ValueError(INVALID_SHORT_NAME)
            if URLMap.get(short):
                raise ValueError(SHORT_OPTION_IS_BUSY)
        if not short:
            short = URLMap.get_unique_short()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
