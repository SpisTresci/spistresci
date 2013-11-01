# from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.conf import settings
from django.utils.decorators import method_decorator

from spistresci.blogger.models import BookRecommendation, BloggerProfile
from spistresci.common.helpers import group_required


class BaseBloggerView(object):

    @method_decorator(group_required([settings.BLOGGER_GROUP_NAME]))
    def dispatch(self, request, *args, **kwargs):
        self.blogger_profile = BloggerProfile.objects.get_or_create(user=request.user)[0]
        self.blogger = request.user
        return super(BaseBloggerView, self).dispatch(request, *args, **kwargs)


class ProfileView(BaseBloggerView, DetailView):
    model = BloggerProfile
    template_name = 'blogger/profile.html'

    def get_object(self, *args, **kwargs):
        return self.request.user.bloggerprofile


class RecommendationList(BaseBloggerView, ListView):
    model = BookRecommendation
    template_name = "blogger/book_recommendation.html"
    context_object_name = 'recommendations'

    def get_queryset(self):
        self.blogger = self.request.user
        return self.blogger.recommendations.all()

class RecommendationNew(BaseBloggerView, FormView):
    model = BookRecommendation

class RecommendationEdit(BaseBloggerView, FormView):
    model = BookRecommendation

class RecommendationView(BaseBloggerView, FormView):
    model = BookRecommendation


