from unittest import TestCase
from app import app
import json

from shortening_url_service import SHORT_URL_BASE


class decode_tests(TestCase):
    def test_missing_query_param(self):
        with app.test_client() as c:
            response = c.get('/decode')

            self.assertEqual(response.status_code, 400)

    def test_malformed_url(self):
        with app.test_client() as c:
            response = c.get('/decode?url=blabla.com')

            self.assertEqual(response.status_code, 400)

    def test_url_not_exist(self):
        with app.test_client() as c:
            response = c.get('/decode?url=http://www.short.my.com/z')

            self.assertEqual(response.status_code, 204)

    def test_url_exist(self):
        with app.test_client() as c:
            long_url = 'http://www.blabla.com'
            encode_response = c.post('/encode', json=dict(url=long_url))
            self.assertEqual(encode_response.status_code, 200)

            short_url = encode_response.json.get('url')
            decode_response = c.get(f'/decode?url={short_url}')

            self.assertEqual(decode_response.status_code, 200)
            self.assertEqual(json.loads(decode_response.get_data()), {'long_url': long_url})


class encode_tests(TestCase):
    def test_missing_url(self):
        with app.test_client() as c:
            long_url = ''
            response = c.post('/encode', json=dict(url=long_url))

            self.assertEqual(response.status_code, 400)

    def test_malformed_url(self):
        with app.test_client() as c:
            long_url = 'blabla.com'
            response = c.post('/encode', json=dict(url=long_url))

            self.assertEqual(response.status_code, 400)

    def test_encode_success(self):
        with app.test_client() as c:
            long_url = 'http://www.blabla.com'
            encode_response = c.post('/encode', json=dict(url=long_url))
            self.assertEqual(encode_response.status_code, 200)
            self.assertEqual(json.loads(encode_response.get_data()), {'url': f'{SHORT_URL_BASE}/oA=='})

    def test_encode_same_url(self):
        with app.test_client() as c:
            long_url = 'http://www.blabla.com'
            first_encode_response = c.post('/encode', json=dict(url=long_url))
            self.assertEqual(first_encode_response.status_code, 200)
            second_encode_response = c.post('/encode', json=dict(url=long_url))
            self.assertEqual(second_encode_response.status_code, 200)
            self.assertEqual(first_encode_response.get_data(), second_encode_response.get_data())

    def test_multiple_url_encode(self):
        with app.test_client() as c:
            for i in range(555):
                response = c.post('/encode', json=dict(url=f'http://www.{i}.com'))
                self.assertEqual(response.status_code, 200)

            self.assertEqual(json.loads(response.get_data()), {'url': f'{SHORT_URL_BASE}/5A=='})
