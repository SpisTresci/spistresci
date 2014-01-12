from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from registration.backends.default.views import RegistrationView

from spistresci.index.views import index
from spistresci.search.views import STSearchView, STSearchQuerySet, hide_menu, STSearchForm
from spistresci.book.views import STBookQuerySet, STBookView, book_redirect
from spistresci.auth.views import (logout, accounts_social_signup,
        accounts_profile, MyLoginView, ProfileRemove)
from spistresci.track.views import TrackedBookList
#from allauth.account.views import LoginView
from spistresci.register.views import register_user, egazeciarz_register_user
from spistresci.monitor.views import monitor

from spistresci.auth.forms import RegistrationForm, MyLoginForm
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from spistresci.partners.views import partners

admin.autodiscover()
dajaxice_autodiscover()

book_url_re = r'book/(?P<book_id>\d+)/.*$'

urlpatterns = patterns('',
     url('^$', index, name="index"),
     url('^logout/$', logout),
     url('^hide_menu/(?P<value>\d)/$', hide_menu),
     url('^monitor/$', monitor),
     url(r'^accounts/signup/$',
                           RegistrationView.as_view(form_class=RegistrationForm),
                           name='account_signup'),

     url(r'^accounts/login/$',
                           MyLoginView.as_view(form_class=MyLoginForm),
                           name="account_login"),

     url(r'^accounts/', include('registration.backends.default.urls')),
     url(r'^%s' % (book_url_re,), STBookView(searchqueryset = STBookQuerySet(), form_class=STSearchForm), name='book_page'),
     url(r'^book-redirect/$', book_redirect, name="book_redirect"),
#     url('^description/(?P<book_id>\w+)/$', book_description),
     url(r'^blogger/', include('spistresci.blogger.urls', namespace='blogger')),
     url(r'^profile/', include('spistresci.auth.urls', namespace='profile')),
     url(r'^profile/tracs/$', TrackedBookList.as_view(), name="tracked_book_list"),
     url(r'^profile/remove/$', ProfileRemove.as_view(), name="profile_remove"),
     url('^regulamin/', TemplateView.as_view(template_name='terms_of_use.html'), name='terms_of_use'),
     url('^partners/$', partners),
)

#TODO: check thread safe version of this
# Without threading...
urlpatterns += patterns('haystack.views',
    url(r'^search/$', STSearchView(searchqueryset = STSearchQuerySet(), form_class=STSearchForm), name='haystack_search'),
    url(r'^q/$', STSearchView(searchqueryset = STSearchQuerySet(), form_class=STSearchForm, template="search/results_list.html"), name='haystack_search'),
    url(r'^qb/$', STSearchView(searchqueryset = STSearchQuerySet(), form_class=STSearchForm, template="search/results_thumbnail_list.html"), name='haystack_search'),
    url(r'^qn/$', STSearchView(searchqueryset = STSearchQuerySet(), form_class=STSearchForm, template="search/results_thumbnail_list.html"), name='haystack_search'),
    url(r'^qp/$', STSearchView(searchqueryset = STSearchQuerySet(), form_class=STSearchForm, template="search/results_thumbnail_list.html"), name='haystack_search'),

    #url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/social/signup/$', accounts_social_signup),
    url(r'^accounts/profile/$', accounts_profile),

    #url(r'^accounts/loggedin/$', loggedin),
    #url(r'^accounts/invalid/$', invalid_login),
    #url(r'^accounts/register/$', register_user),
    url(r'^egazeciarz/accounts/register/$', egazeciarz_register_user),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('allauth.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

if settings.IS_DEV:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
