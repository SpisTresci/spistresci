from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from main_service.views import index, search
from logos_stripe.views import main

urlpatterns = patterns('',
     ('^$', index),
     ('^search/$', search),
     ('^main/$', main),
)
