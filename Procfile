web2: daphne DaddysMovie.asgi:application --port $PORT --bind 0.0.0.0
web: gunicorn DaddysMovie.wsgi --log-file -
worker: python manage.py runworker channel_layer -v2
