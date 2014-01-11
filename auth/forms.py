# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django import forms
from django.utils.safestring import mark_safe

from django_common.helper import md5_hash

from registration.forms import RegistrationForm as BaseRegistrationForm



class RegistrationForm(BaseRegistrationForm):

    term_of_use = forms.BooleanField(label=mark_safe('Akceptuję <a href="/regulamin/">regulamin</a> serwisu.'), required=True)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.HiddenInput()
        self.fields['username'].initial = md5_hash(max_length=30)  # 30 is length of username attribute in User model
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['placeholder'] = 'Hasło'
        self.fields['password2'].widget.attrs['placeholder'] = u'Powtórz hasło'

        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''

    def as_p(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
            normal_row = '<p%(html_class_attr)s>%(field)s %(label)s%(help_text)s</p>',
            error_row = '%s',
            row_ender = '</p>',
            help_text_html = ' <span class="helptext">%s</span>',
            errors_on_separate_row = True)

from allauth.account.forms import LoginForm

class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password'].widget.attrs['placeholder'] = 'Hasło'

        self.fields['login'].label = ''
        self.fields['password'].label = ''
        self.fields['remember'].label = 'Pamiętaj mnie.'

    def as_p(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
            normal_row = '<p%(html_class_attr)s>%(field)s %(label)s%(help_text)s</p>',
            error_row = '%s',
            row_ender = '</p>',
            help_text_html = ' <span class="helptext">%s</span>',
            errors_on_separate_row = True)

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email']
