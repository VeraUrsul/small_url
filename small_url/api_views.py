from http import HTTPStatus
import os

from flask import jsonify, request, render_template, send_file

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

ORIGINAL_LINK = 'Указанный id не найден'
NOT_REQUIRED_FIELD = '"url" является обязательным полем!'
WITHOUT_REQUEST = 'Отсутствует тело запроса'


@app.route('/docs')
def swagger_ui():
    return render_template('swagger_ui.html')


@app.route('/specification')
def get_spec():
    filename = os.path.join(app.root_path, 'openapi.yml')
    return send_file(filename)


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(WITHOUT_REQUEST, HTTPStatus.BAD_REQUEST)
    if 'url' not in data or not data['url']:
        raise InvalidAPIUsage(NOT_REQUIRED_FIELD, HTTPStatus.BAD_REQUEST)
    try:
        return jsonify(
            URLMap.create(
                data['url'],
                data.get('custom_id'),
                need_validate=True
            ).to_dict()
        ), HTTPStatus.CREATED
    except ValueError as error:
        raise InvalidAPIUsage(str(error))


@app.route('/api/id/<string:short>/', methods=['GET'])
def original_url(short):
    url_map = URLMap.get(short)
    if url_map:
        return jsonify({'url': url_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage(ORIGINAL_LINK, HTTPStatus.NOT_FOUND)
