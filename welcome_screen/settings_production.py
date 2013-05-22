from settings import *
DEBUG = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Anita Wysokińska', 'awysokinska@spistresci.pl'),
    ('Krzysztof Szumny', 'kszumny@spistresci.pl'),
    ('Piotr Zawiślak', 'pzawislak@spistresci.pl'),
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
