release: python manage.py migrate
web: daphne DaddysMovie.asgi:application --port $PORT --bind 0.0.0.0 -v2