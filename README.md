# Daddys Movie
 This is a web application for streaming movies privately. You can copy the code from this project. I am not liable to anything you do with this project, I made this for educational purposes.


# HOW TO SETUP USING A FREE HEROKU SERVER

This web application has only been tested on Heroku. 
* Download the project [Daddys Movie](https://github.com/LTSana/Daddys-Movie/archive/refs/heads/main.zip)
* Create a free [HEROKU](https://id.heroku.com/login) account.
* Download the [HEROKU CLI](https://devcenter.heroku.com/articles/heroku-cli) to be able to connect to the servers terminal.
* Create a free [CLOUDINARY](https://cloudinary.com/users/register/free) account to store your movie covers.

Add the following to your resources:
1. Heroku Postgres
2. Heroku Redis (You will need to verify your account by adding a valid bank card, if you do not want simple keep `REDIS_AVAILABLE = False` to avoid using REDIS configurations.)

Instructions to get the code on Heroku. (Open your terminal and run these commands) 
`name_app` is the name of your Heroku App
```cmd
1. $ heroku login
2. $ heroku git:clone -a name_app
3. $ cd name_app
4. $ git add .
5. $ git commit -am "make it better"
6. $ git push heroku master
```

Now that the source code has been added to your Heroku app follow these instructions.
1. Go to `settings`
2. Click on `Reveal Config Vars`
3. Add the environment variables for your app. [HERE](#the-environment-variables)
4. All the variables with `******` you need to provide your own keys.
5. You can get a [SECRET KEY HERE](https://djecrety.ir/)

For `reCAPTCHA` you need a Google Account
1. Signup for a google account. (If you already have one just signin)
2. Go to [Google reCAPTCHA admin](https://www.google.com/recaptcha/admin)
3. Click the `+` button to create a new reCAPTCHA.
4. Fill in all the needed fields.
5. Select the `reCAPTCHA v3` option.
6. When done, copy the `SITE KEY` and `SECRETE KEY` to your environment variables.


### The environment variables
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
