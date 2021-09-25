import url_dao

SHORT_URL_BASE = 'http://www.short.my.com'


def encode_url(long_url):
    try:
        short_url = url_dao.generate_short_url(long_url)
        return f'{SHORT_URL_BASE}/{short_url}'
    except:
        print(f'failed to encode {long_url}')


def decode_url(short_url):
    url_parts = short_url.split('/')
    return url_dao.get_long_url(url_parts[3])

