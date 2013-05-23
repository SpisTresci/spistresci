from settings import *
import os
DEBUG = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Anita Wysokinska', 'awysokinska@spistresci.pl'),
    ('Krzysztof Szumny', 'kszumny@spistresci.pl'),
    ('Piotr Zawislak', 'pzawislak@spistresci.pl'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'subscriptions',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'Z0oBvgF1R3',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

EMAIL_SUBJECT_PREFIX= 'Welcome Screen:'

#Note: This seems to be stupid, but in production mode template dir should be absolute path :/
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT,'templates'),
)
