__author__ = 'work'

from django.core import mail
from django.conf import settings

core_mail_admins = mail.mail_admins

def st_mail_admins(*args, **kwargs):
    connection = mail.get_connection(fail_silently=True,
                                host=settings.ADMIN_EMAIL_HOST,
                                port=settings.ADMIN_EMAIL_PORT,
                                username=settings.ADMIN_EMAIL_HOST_USER,
                                password=settings.ADMIN_EMAIL_PASSWORD,
                                use_ttl=settings.ADMIN_EMAIL_USE_TLS)

    # overwrite connection only when it is not given in kwargs
    if 'connection' not in kwargs.keys():
        kwargs['connection'] = connection

    core_mail_admins(*args, **kwargs)

mail.mail_admins = st_mail_admins
