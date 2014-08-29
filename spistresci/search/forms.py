# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import ModelChoiceIterator
from haystack.forms import ModelSearchForm

from spistresci.models import Bookstore, BookFormat, BookFormatType

from django.forms.widgets import SelectMultiple, CheckboxInput, \
    CheckboxSelectMultiple
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.html import format_html
from itertools import chain


class STCheckboxSelectMultiple(CheckboxSelectMultiple):
    def __init__(self, attrs=None, choices=(), *args, **kwargs):
        super(STCheckboxSelectMultiple, self).__init__(attrs, choices)
        self.kwargs = kwargs

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = ['    <div class="filter_content bullet_list">']
        # Normalize to strings
        str_values = set([force_text(v) for v in value])

        groups = self.kwargs.get('group_by')

        groups = groups.objects.all()
        model = self.choices.queryset.model
        for j, group in enumerate(groups):

            new_choices = model.objects.filter(type=group)
            if new_choices:
                output.append(
                    format_html(
                        '    <div class="filter_section{0}" >',
                        ' filter_section_last' if j == len(groups)-1 else ''
                    )
                )
                output.append(format_html('        <div id="menu_arrow{0}" class="filter_section_arrow"></div>', group.name))
                output.append(format_html('        <div class="filter_section_header">{0}</div>', group.name))
                output.append(format_html('        <ul id="sub{0}">', j))

                for i, (option_value, option_label) in enumerate([(nc.id, nc.name) for nc in new_choices]):
                    # If an ID attribute was given, add a numeric index as a suffix,
                    # so that the checkboxes don't all have the same ID attribute.
                    if has_id:
                        final_attrs = dict(final_attrs, id='%s_%s_%s' % (attrs['id'], j, i))
                        label_for = format_html(' for="{0}"', final_attrs['id'])
                    else:
                        label_for = ''

                    cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
                    option_value = force_text(option_value)
                    rendered_cb = cb.render(name, option_value, attrs={
                        'class': 'check-with-label',
                        'style': 'display:none;'
                    })
                    option_label = force_text(option_label)
                    output.append(format_html('            <li>{1}<label{0} class="label-for-check">{2}</label></li>',
                                              label_for, rendered_cb, option_label))

                output.append('        </ul>')
                output.append('    </div>')
        output.append('</div>')
        return mark_safe('\n'.join(output))


class SpisTresciSearchForm(ModelSearchForm):
    q = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'autocomplete': 'off',
                'placeholder': u'Wpisz tytuł książki lub nazwisko autora',
                'data-shake': '3',
            }
        )
    )
    price_from = forms.DecimalField(required=False)
    price_to = forms.DecimalField(required=False)
    bookstore = forms.ModelMultipleChoiceField(
        queryset=Bookstore.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
    )
    format = forms.ModelMultipleChoiceField(
        queryset=BookFormat.objects.all(),
        widget=STCheckboxSelectMultiple(
            group_by=BookFormatType,
        ),
        required=False,
    )

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(SpisTresciSearchForm, self).search()

        if self.cleaned_data['price_from']:
            sqs = sqs.filter(
                price_highest__gte=self.cleaned_data['price_from']
            )

        if self.cleaned_data['price_to']:
            sqs = sqs.filter(
                price_lowest__lte=self.cleaned_data['price_to']
            )

        # if self.cleaned_data['bookstore']:
        #     sqs = sqs.filter(bookstore__in=self.cleaned_data['bookstore'])
        #
        # if self.cleaned_data['bookstore']:
        #     sqs = sqs.filter(bookstore__in=self.cleaned_data['bookstore'])

        return sqs