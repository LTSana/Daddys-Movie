web: gunicorn DaddysMovie.wsgi --log-file -
web2: daphne DaddysMovie.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channel_layer -v2