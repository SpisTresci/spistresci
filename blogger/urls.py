from django.conf.urls import patterns, url

from spistresci.blogger.views import (ProfileView, RecommendationList,
                                      RecommendationNew, RecommendationView,
                                      RecommendationEdit)

urlpatterns = patterns('',
    url(r'^$', ProfileView.as_view(), name="profile"),
    url(r'^recommendations/$', RecommendationList.as_view(), name="recommendations"),
    url(r'^recommendations/new/$', RecommendationNew.as_view(), name="recommendation_new"),
    url(r'^recommendations/(?P<recommendation_pk>\d+)/$', RecommendationView.as_view(), name="recommendation_preview"),
    url(r'^recommendations/(?P<recommendation_pk>\d+)/edit/$', RecommendationEdit.as_view(), name="recommendation_edit"),
)
