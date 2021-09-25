# hexa3d url shortner service


clone the repository to local machine

setup a working virtual env (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

install requirements.txt

in terminal: "{local_path}/hexa3d/venv/bin/python -m flask run"

example requests:

DECODE:
curl --location --request POST 'http://127.0.0.1:5000/encode' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=nGpvKxNWouikGeQZHGewUtb2lah2HmFOqq6McgX4uWZFU8JP6UZRepCJHxJSRWIg' \
--data-raw '{
    "url": "http://www.blabla.com"
}'

ENCODE:
curl --location --request GET 'http://127.0.0.1:5000/decode?url=http://www.short.my.com/4' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=nGpvKxNWouikGeQZHGewUtb2lah2HmFOqq6McgX4uWZFU8JP6UZRepCJHxJSRWIg' \

