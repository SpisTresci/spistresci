from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import user_passes_test

from spistresci.constants import getListOfTopMenuServices


def send_email(template, context, sender, receivers, subject, headers=None):
    context.update({'site': Site.objects.get_current(),
                    'STATIC_URL': settings.STATIC_URL})
    message = render_to_string(template, context)

    msg = EmailMultiAlternatives(subject, '', sender, receivers, headers=headers)
    msg.attach_alternative(message, "text/html")
    msg.send()


def google_analytics_context_processor(request):
    return dict(google_analytics_id=getattr(settings, 'GOOGLE_ANALYTICS_ID', None))

def menu_context_processor(request):
	return dict(top_menu=getListOfTopMenuServices(request),
        serve_local_files=getattr(settings, 'SERVE_LOCAL_FILES', True))

def group_required(group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)
