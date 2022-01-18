web: daphne DaddysMovie.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=DaddysMovie.settings -v2