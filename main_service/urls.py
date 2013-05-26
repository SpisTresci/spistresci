from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from main_service.views import index, search

urlpatterns = patterns('',
     ('^$', index),
     ('^search/$', search),
)
