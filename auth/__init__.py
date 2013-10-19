__author__ = 'work'

# MONKEY PATCH
# for sending registration email in html format instead of plain text

from django.conf import settings
from django.template.loader import render_to_string

from registration.models import RegistrationProfile

from spistresci.common.helpers import send_email


def send_activation_email(self, site):
    ctx_dict = {'activation_key': self.activation_key,
                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                'site': site}
    subject = render_to_string('registration/activation_email_subject.txt',
                               ctx_dict)
    subject = ''.join(subject.splitlines())
    template = 'registration/activation_email.html'
    send_email(template, ctx_dict, settings.DEFAULT_FROM_EMAIL,
    		   [self.user.email], subject)

RegistrationProfile.send_activation_email = send_activation_email
