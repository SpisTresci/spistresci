from django.conf.urls import patterns, url

from spistresci.blogger.views import (ProfileView, RecommendationList,
                                      RecommendationNew,
                                      RecommendationEdit)

urlpatterns = patterns('',
    url(r'^$', ProfileView.as_view(), name="profile"),
    url(r'^recommendations/$', RecommendationList.as_view(), name="recommendation_list"),
    url(r'^recommendations/new/$', RecommendationNew.as_view(), name="recommendation_new"),
    url(r'^recommendations/(?P<recommendation_pk>\d+)/edit/$', RecommendationEdit.as_view(), name="recommendation_edit"),
)
