# -*- coding: utf-8 -*-

import json

from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, BaseFormView
from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from spistresci.blogger.models import BookRecommendation, BloggerProfile
from spistresci.blogger.forms import BloggerProfileForm, BookRecommendationForm
from spistresci.common.helpers import group_required


class BaseBloggerView(object):

    @method_decorator(group_required([settings.BLOGGER_GROUP_NAME]))
    def dispatch(self, request, *args, **kwargs):
        self.blogger_profile = BloggerProfile.objects.get_or_create(user=request.user)[0]
        self.blogger = request.user
        return super(BaseBloggerView, self).dispatch(request, *args, **kwargs)

class ProfilePreview(BaseBloggerView, DetailView):

    template_name = 'blogger/profile_preview.html'

    def get_object(self, *args, **kwargs):
        return self.request.user.bloggerprofile


class ProfileEdit(BaseBloggerView, UpdateView):

    form_class = BloggerProfileForm
    template_name = 'blogger/profile_edit.html'

    def get_object(self, *args, **kwargs):
        return self.request.user.bloggerprofile

    def get_success_url(self):
        return reverse('blogger:profile_preview')


class RecommendationList(BaseBloggerView, ListView):

    template_name = "blogger/recommendation_list.html"
    context_object_name = 'recommendations'

    def get_queryset(self):
        self.blogger = self.request.user
        return self.blogger.recommendations.all()

class RecommendationEdit(BaseBloggerView, UpdateView):
    template_name = "blogger/recommendation_edit.html"
    form_class = BookRecommendationForm
    pk_url_kwarg = 'recommendation_pk'
    model = BookRecommendation

    def get_success_url(self):
        return reverse('blogger:recommendation_list')

    def get_form_kwargs(self):
        kwargs = super(RecommendationEdit, self).get_form_kwargs()
        kwargs['user'] = self.blogger
        return kwargs

    def get_queryset(self):
        return self.blogger.recommendations.all()

class RecommendationNew(BaseBloggerView, CreateView):
    template_name = "blogger/recommendation_new.html"
    form_class = BookRecommendationForm
    model = BookRecommendation

    def get_success_url(self):
        return reverse('blogger:recommendation_list')

    def get_form_kwargs(self):
        kwargs = super(RecommendationNew, self).get_form_kwargs()
        kwargs['user'] = self.blogger
        return kwargs

class RecommendationPreview(BaseBloggerView, DetailView):

    model = BookRecommendation
    pk_url_kwarg = 'recommendation_pk'
    template_name = "blogger/recommendation_preview.html"

    def get_queryset(self, *args, **kwargs):
        return self.blogger.recommendations.all()

class RecommendationDelete(BaseBloggerView, DeleteView):

    model = BookRecommendation
    pk_url_kwarg = 'recommendation_pk'
    template_name = 'blogger/recommendation_delete.html'

    def get_queryset(self, *args, **kwargs):
        return self.blogger.recommendations.all()

    def get_success_url(self, *args, **kwargs):
        return reverse('blogger:recommendation_list')


class RecommendationPreviewIframe(BaseBloggerView, BaseFormView):

    response_class = HttpResponse
    template_name = "index_bloger_box.html"


    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(
            json.dumps(context),
            **response_kwargs
        )

    def post(self, request, *args, **kwargs):
        obj = dict(title=u"Tytuł rekomendacji",
                   content=u"Przykładowa treść rekomendacji książki. "*10,
                   mark='Słowna ocena książki',
                   website_path=self.blogger_profile.website,
                   book_path="",
                   promote_rate=1,
                   status=1)
        form = BookRecommendationForm(self.blogger, request.POST, initial_flag=True)
        form.is_valid()

        obj.update(form.cleaned_data)
        obj['masterbook'] = getattr(form, 'masterbook', None)
        obj['website_path'] = 'http://' + obj['website_path'].strip('http://')
        context = dict(blogger=self.blogger_profile,
                       object=obj)
        html = render(self.request, self.template_name, context)
        return self.render_to_response(dict(html=html.content))
