# Daddys Movie
 This is a web application for streaming movies privately. You can copy the code from this project. I am not liable to anything you do with this project, I made this for educational purposes.


# HOW TO SETUP

This web application has only been tested on Heroku. 
* Create a free [HEROKU](https://id.heroku.com/login) account.
* Download the [HEROKU CLI](https://devcenter.heroku.com/articles/heroku-cli) to be able to connect to the servers terminal.
* Create a free [CLOUDINARY](https://cloudinary.com/users/register/free) account to store your movie covers.

Add the following to your resources:
1. Heroku Postgres
2. Heroku Redis (You will need to verify your account by adding a valid bank card, if you do not want simple keep `REDIS_AVAILABLE = False` to avoid using REDIS configurations.)

The environment variables:
```.ENV
SECRET_KEY = ******
DEBUG = False

DATABASE_ENGINE = django.db.backends.postgresql_psycopg2
DATABASE_NAME = ******
DATABASE_USER = ******
DATABASE_PASSWORD = ******
DATABASE_HOST = ******
DATABASE_PORT = ******

CLOUDINARY_NAME = ******
CLOUDINARY_API_KEY = ******
CLOUDINARY_API_SECRET = ******

RECAPTCHA_SITE_KEY = ******
RECAPTCHA_SECRET_KEY = ******

ENCRYPTION_KEY = ******

REDIS_AVAILABLE = True
REDIS_TLS_URL = ******
REDIS_URL = ******

```
