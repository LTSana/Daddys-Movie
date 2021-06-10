release: python manage.py migrate
web: gunicorn DaddysMovie.wsgi --log-file -
web2: daphne DaddysMovie.asgi:application --port $PORT --bind 0.0.0.0
worker: python manage.py runworker channel_layer