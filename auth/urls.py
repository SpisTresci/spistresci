# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.auth.views import password_change, password_change_done

from spistresci.auth.views import Profile

urlpatterns = patterns('',
    url(r'^$', Profile.as_view(), name="home"),
    url(r'^password-change/$', password_change,
    	{'template_name': 'auth/password_change.html',
    	 'post_change_redirect': '/profile/password-change/done/'},
    	name="password_change"),
    url(r'^password-change/done/$', password_change_done,
    	{'template_name': 'auth/message.html',
    	 'extra_context': {'message': u'Hasło zostało zmienione'}},
    	name="password_change_done"),
)
