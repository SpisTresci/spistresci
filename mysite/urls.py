from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from mysite.views import main, logo

urlpatterns = patterns('',
     ('^$', main),    
     ('^image/$',logo),

)
