web: daphne DaddysMovie.asgi:application --port $PORT --bind 0.0.0.0 --proxy-headers -v2
worker: python manage.py runworker channel_layer -v2