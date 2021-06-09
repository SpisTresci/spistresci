from django.conf.urls import url

from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', views.manual_merging),
    url(r'^take/$', views.manual_merging_take),
]