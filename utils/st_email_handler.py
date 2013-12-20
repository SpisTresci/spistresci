from django.utils.log import AdminEmailHandler
from django.core.mail import get_connection


class STEmailHandler(AdminEmailHandler):
    def connection(self):
        
        return get_connection(backend=self.email_backend, fail_silently=True, 
            host=settings.ADMIN_EMAIL_HOST, port=settings.ADMIN_EMAIL_PORT, username=settings.ADMIN_EMAIL_HOST_USER, password=settings.ADMIN_EMAIL_PASSWORD, use_ttl=settings.ADMIN_EMAIL_USE_TTL)

        
