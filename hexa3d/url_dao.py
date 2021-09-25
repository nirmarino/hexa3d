import threading
import base64
import hashlib

LAST_CHAR = -1

# in-memory db\cache
SHORT_TO_LONG_REPO = {}
LONG_TO_SHORT_REPO = {}
last_used_key = '0'

lock = threading.Lock()


def get_long_url(short_url):
    return SHORT_TO_LONG_REPO.get(short_url)


def generate_short_url(long_url):
    with lock:
        short_url = _get_short_url(long_url)
        if short_url is None:
            short_url = _generate_short_url_key(long_url)
            SHORT_TO_LONG_REPO[short_url] = long_url
            LONG_TO_SHORT_REPO[long_url] = short_url
        return short_url


def _get_short_url(long_url):
    return LONG_TO_SHORT_REPO.get(long_url)


def _generate_short_url_key(url):
    hasher = hashlib.sha1(url.encode('utf-8'))
    for i in range(len(url)):
        if base64.urlsafe_b64encode(hasher.digest()[: i + 1]) not in SHORT_TO_LONG_REPO.keys():
            return base64.urlsafe_b64encode(hasher.digest()[: i + 1]).decode()

    return base64.urlsafe_b64encode(hasher.digest()).decode()
