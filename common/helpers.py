from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site


def send_email(template, context, sender, receivers, subject, headers=None):
    context.update({'site': Site.objects.get_current(),
                    'STATIC_URL': settings.STATIC_URL})
    message = render_to_string(template, context)

    msg = EmailMultiAlternatives(subject, '', sender, receivers, headers=headers)
    msg.attach_alternative(message, "text/html")
    msg.send()
