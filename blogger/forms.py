# -*- coding: utf-8 -*-

import re
from urlparse import urlparse

from django import forms
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from spistresci.blogger.models import BloggerProfile, BookRecommendation
from spistresci.models import MasterBook
from spistresci.urls import book_url_re

class BloggerProfileForm(forms.ModelForm):
    class Meta:
        model = BloggerProfile
        fields = ['website', 'website_name', 'photo', 'signature']

class BookRecommendationForm(forms.ModelForm):

    class Meta:
        model = BookRecommendation
        exclude = ['author', 'publication_date', 'masterbook']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.blogger = user.bloggerprofile
        self.base_fields['status'].choices = self.blogger.get_recommendation_statuses()
        super(BookRecommendationForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['status'].initial = self.instance.status
        self.fields.keyOrder = ['title', 'content', 'mark', 'website_path',
                                'book_path', 'promote_rate', 'status']

    def save(self, *args, **kwargs):
        status_before = None
        if self.instance.pk:
            status_before = self.instance.status
        obj = super(BookRecommendationForm, self).save(commit=False)
        obj.author = self.user
        obj.masterbook = MasterBook.objects.get(pk=self.master_book_pk)
        if not self.blogger.publication_available and \
            status_before == BookRecommendation.STATUS_PUBLICATED:
            obj.status = obj.STATUS_FOR_PUBLICATION
        obj.save()
        return obj

    def clean_book_path(self):
        value = self.cleaned_data['book_path']
        regex = re.search(book_url_re, value)
        if regex and regex.groups():
            master_book_pk = int(regex.groups()[0])
            if not MasterBook.objects.filter(pk=master_book_pk).count():
                raise ValidationError('Książka o podanym ID nie istnieje w bazie danych')
            self.master_book_pk = master_book_pk
            return value
        raise ValidationError('Podany adres książki jest nieprawidłowy')

    def clean_website_path(self):
        if not self.blogger.website:
            raise ValidationError('Brak adresu strony na profilu blogera.')

        value = self.cleaned_data['website_path']
        parsed_url = urlparse(value)
        parsed_blogger_url = urlparse(self.blogger.website)

        if parsed_url.netloc.strip('www.') != parsed_blogger_url.netloc.strip('www.'):
            raise ValidationError('Podany adres nie zgadza się z adresem bloga w profilu.')

        return value
