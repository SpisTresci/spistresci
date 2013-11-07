# -*- coding: utf-8 -*-

import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from spistresci.blogger.models import BloggerProfile, BookRecommendation
from spistresci.models import MasterBook
from spistresci.urls import book_url_re

class BookUrlWidget(forms.TextInput):

    def render(self, name, value, attrs=None):
        if value:
            value = reverse('book_details', kwargs=dict(book_id=value))
        return super(BookUrlWidget, self).render(name, value, attrs=attrs)

class BookUrlField(forms.CharField):

    widget = BookUrlWidget()

    def validate(self, value):
        regex = re.search(book_url_re, value)
        if regex and regex.groups():
            master_book_pk = int(regex.groups()[0])
            if not MasterBook.objects.filter(pk=master_book_pk).count():
                raise ValidationError('Książka o podanym ID nie istnieje w bazie danych')
            return master_book_pk
        raise ValidationError('Podany adres książki jest nieprawidłowy')

    def clean(self, value):
        master_book_pk = self.validate(value)
        return MasterBook.objects.get(pk=master_book_pk)


class BloggerProfileForm(forms.ModelForm):
    class Meta:
        model = BloggerProfile
        fields = ['website', 'photo', 'signature']

class BookRecommendationForm(forms.ModelForm):

    masterbook = BookUrlField()

    class Meta:
        model = BookRecommendation
        exclude = ['author', 'publication_date']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.blogger = user.bloggerprofile
        self.base_fields['status'].choices = self.blogger.get_recommendation_statuses()
        super(BookRecommendationForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['status'].initial = self.instance.status
        self.fields.keyOrder = ['title', 'content', 'mark', 'website_path',
                                'masterbook', 'promote_rate']

    def save(self, *args, **kwargs):
        obj = super(BookRecommendationForm, self).save(commit=False)
        obj.author = self.user
        obj.save()
        return obj

    def clean(self):
        if not self.blogger.publication_available and \
            self.instance.status == BookRecommendation.STATUS_PUBLICATED:
            raise forms.ValidationError(u"Nie możesz edytować opublikowanej rekomendacji")

        return super(BookRecommendationForm, self).clean()

