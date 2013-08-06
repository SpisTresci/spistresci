from django.conf.urls import patterns, include, url
from django.contrib import admin

from spistresci.views.index import index
from spistresci.views.search import STSearchView, STSearchQuerySet, hide_menu, STSearchForm
from spistresci.views.auth import logout, accounts_social_signup, accounts_profile
from spistresci.views.register import register_user, egazeciarz_register_user

admin.autodiscover()

urlpatterns = patterns('',
     ('^$', index),
     ('^logout/$', logout),
     ('^hide_menu/(?P<value>\d)/$', hide_menu),
)

#TODO: check thread safe version of this
# Without threading...
urlpatterns += patterns('haystack.views',
    url(r'^search/$', STSearchView(searchqueryset = STSearchQuerySet(), form_class=STSearchForm), name='haystack_search'),
    url(r'^q/$', STSearchView(searchqueryset = STSearchQuerySet(), form_class=STSearchForm, template="search_results_list.html"), name='haystack_search'),

    #url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/social/signup/$', accounts_social_signup),
    url(r'^accounts/profile/$', accounts_profile),

    #url(r'^accounts/loggedin/$', loggedin),
    #url(r'^accounts/invalid/$', invalid_login),
    url(r'^accounts/register/$', register_user),
    url(r'^egazeciarz/accounts/register/$', egazeciarz_register_user),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    (r'^accounts/', include('allauth.urls')),

)