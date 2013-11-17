from django.conf.urls import patterns, url

from spistresci.blogger.views import (ProfilePreview, RecommendationList,
                                      RecommendationNew, ProfileEdit,
                                      RecommendationEdit, RecommendationPreview)

urlpatterns = patterns('',
    url(r'^$', ProfilePreview.as_view(), name="profile_preview"),
    url(r'^edit/$', ProfileEdit.as_view(), name="profile_edit"),
    url(r'^recommendations/$', RecommendationList.as_view(), name="recommendation_list"),
    url(r'^recommendations/new/$', RecommendationNew.as_view(), name="recommendation_new"),
    url(r'^recommendations/(?P<recommendation_pk>\d+)/$', RecommendationPreview.as_view(), name="recommendation_preview"),
    url(r'^recommendations/(?P<recommendation_pk>\d+)/edit/$', RecommendationEdit.as_view(), name="recommendation_edit"),
)
