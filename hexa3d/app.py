import http
import validators

from flask import Flask, request

import shortening_url_service

app = Flask(__name__)


@app.route(
    '/encode',
    methods=[
        'POST',
    ],
)
def encode():
    url_to_encode = request.json['url']
    if url_to_encode is None or not (validators.url(url_to_encode)):
        response = ('invalid url', http.HTTPStatus.BAD_REQUEST)
    else:
        short_url = shortening_url_service.encode_url(url_to_encode)
        response = ({'url': short_url}, http.HTTPStatus.OK)

    return response


@app.route(
    '/decode',
    methods=[
        'GET',
    ],
)
def decode():
    url_to_decode = request.args.get('url')

    if (
        url_to_decode is None
        or not (validators.url(url_to_decode))
        or f'{shortening_url_service.SHORT_URL_BASE}/' not in url_to_decode
    ):
        response = ('', http.HTTPStatus.BAD_REQUEST)
    else:
        long_url = shortening_url_service.decode_url(url_to_decode)
        if long_url is not None:
            response = ({'long_url': long_url}, http.HTTPStatus.OK)
        else:
            response = ('', http.HTTPStatus.NO_CONTENT)

    return response


if __name__ == '__main__':
    app.run()
