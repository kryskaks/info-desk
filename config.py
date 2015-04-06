from datetime import timedelta
import os

DEBUG = True

DEBUG_TB_INTERCEPT_REDIRECTS = False

ADMINS = frozenset(['kryskaks@gmail.com'])

SECRET_KEY = 'top secret'

THREADS_PER_PAGE = 8

CSRF_ENABLED = True

CSRF_SESSION_KEY = ""

PERMANENT_SESSION_LIFETIME = timedelta(minutes=20)

DATABASE_URL = os.environ['INFO_DESK_DATABASE_URL']

ERROR_EMAILS = "krementar@w1.ua;krementar@interkassa.com"