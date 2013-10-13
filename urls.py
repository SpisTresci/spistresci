from django.conf.urls import patterns, include, url
from django.contrib import admin

from spistresci.index.views import index
from spistresci.search.views import STSearchView, STSearchQuerySet, hide_menu, STSearchForm
from spistresci.auth.views import logout, accounts_social_signup, accounts_profile
from spistresci.register.views import register_user, egazeciarz_register_user
from spistresci.monitor.views import monitor


admin.autodiscover()

urlpatterns = patterns('',
     url('^$', index),
     url('^logout/$', logout),
     url('^hide_menu/(?P<value>\d)/$', hide_menu),
     url('^monitor/$', monitor),
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

    url(r'^accounts/', include('allauth.urls')),

)