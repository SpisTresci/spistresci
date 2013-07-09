from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from main_service.views import index, STSearchView, STSearchQuerySet, hide_menu
from logos_stripe.views import main

urlpatterns = patterns('',
     ('^$', index),
     ('^main/$', main),
     ('^hide_menu/(?P<value>\d)/$', hide_menu)
)


#TODO: check thread safe version of this
# Without threading...
urlpatterns += patterns('haystack.views',
    url(r'^search/$', STSearchView(searchqueryset = STSearchQuerySet()), name='haystack_search'),
)