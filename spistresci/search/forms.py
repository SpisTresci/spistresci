# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import CheckboxInput, CheckboxSelectMultiple
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string

from haystack.forms import ModelSearchForm

from spistresci.models import Bookstore, BookFormat, BookFormatType


class STCheckboxSelectMultiple(CheckboxSelectMultiple):
    def __init__(self, attrs=None, choices=(), *args, **kwargs):
        super(STCheckboxSelectMultiple, self).__init__(attrs, choices)
        self.kwargs = kwargs

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []

        # Normalize to strings
        model = self.choices.queryset.model

        dic = {
            'output': ['    <div class="filter_content bullet_list">'],
            'has_id': attrs and 'id' in attrs,
            'final_attrs': self.build_attrs(attrs, name=name),
            'str_values': set([force_text(v) for v in value]),
        }

        groups = self.kwargs.get('group_by', [])
        if groups:
            groups = groups.objects.all()

            for i, group in enumerate(groups):
                dic.update({
                    'new_choices': model.objects.filter(type=group),
                    'last': i == len(groups)-1,
                    'group': group,
                    'attrs': attrs,
                    'gr_counter': i,
                    'name': name,
                })
                if dic['new_choices']:
                    self.render_group(**dic)
        else:
            class gr():
                name = "Wszystkie"

            dic.update({
                'new_choices': model.objects.all(),
                'last': True,
                'group': gr(),
                'attrs': attrs,
                'gr_counter': 0,
                'name': name,
            })
            self.render_group(**dic)

        dic['output'].append('</div>')
        return mark_safe('\n'.join(dic['output']))

    def render_group(self, output, new_choices, group, last, has_id,
                     attrs, final_attrs, str_values, gr_counter, name):

        output.append(
            format_html(
                '<div class="filter_section{0}" >',
                ' filter_section_last' if last else ''
            )
        )
        output.append(
            format_html(
                '<div id="menu_arrow{0}" class="filter_section_arrow"></div>',
                group.name
            )
        )
        output.append(
            format_html(
                '<div class="filter_section_header">{0}</div>',
                group.name
            )
        )
        output.append(format_html('<ul id="sub{0}">', gr_counter))

        new_choices = [(nc.id, nc.name) for nc in new_choices]
        for i, (value, label) in enumerate(new_choices):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(
                    final_attrs,
                    id='%s_%s_%s' % (attrs['id'], gr_counter, i)
                )
                label_for = format_html(' for="{0}"', final_attrs['id'])
            else:
                label_for = ''

            cb = CheckboxInput(
                final_attrs,
                check_test=lambda val: val in str_values
            )

            value = force_text(value)
            rendered_cb = cb.render(name, value, attrs={
                'class': 'check-with-label',
                'style': 'display:none;'
            })
            label = force_text(label)
            output.append(
                format_html(
                    '<li>{1}<label{0} class="label-for-check">{2}</label></li>',
                    label_for,
                    rendered_cb,
                    label
                )
            )

        output.append('</ul>')
        output.append('</div>')


class RangeWidget(forms.MultiWidget):
    def __init__(self, widget, *args, **kwargs):
        widgets = (widget, widget)

        super(RangeWidget, self).__init__(widgets=widgets, *args, **kwargs)

    def decompress(self, value):
        return value

    def format_output(self, rendered_widgets):
        widget_context = {
            'min': rendered_widgets[0],
            'max': rendered_widgets[1],
        }
        return render_to_string('filter/price.html', widget_context)


class RangeField(forms.MultiValueField):
    default_error_messages = {
        'invalid_start': _(u'Wprowadź poprawną cenę'),
        'invalid_end': _(u'Wprowadź poprawną cenę'),
    }

    def __init__(self, field_class, widget=forms.TextInput, *args, **kwargs):
        if not 'initial' in kwargs:
            kwargs['initial'] = ['', '']

        fields = (field_class(), field_class())

        super(RangeField, self).__init__(
            fields=fields,
            widget=RangeWidget(widget),
            *args,
            **kwargs
        )

    def compress(self, data_list):
        if data_list:
            return [
                self.fields[0].clean(data_list[0]),
                self.fields[1].clean(data_list[1]),
            ]

        return None


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
    # price_range = RangeField(forms.DecimalField)
    bookstores = forms.ModelMultipleChoiceField(
        queryset=Bookstore.objects.all(),
        widget=STCheckboxSelectMultiple,
        required=False,
    )
    formats = forms.ModelMultipleChoiceField(
        queryset=BookFormat.objects.all(),
        widget=STCheckboxSelectMultiple(
            group_by=BookFormatType,
        ),
        required=False,
    )

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(SpisTresciSearchForm, self).search()

        # if self.cleaned_data['price_from']:
        #     sqs = sqs.filter(
        #         price_highest__gte=self.cleaned_data['price_from']
        #     )
        #
        # if self.cleaned_data['price_to']:
        #     sqs = sqs.filter(
        #         price_lowest__lte=self.cleaned_data['price_to']
        #     )

        # if self.cleaned_data['bookstore']:
        #     sqs = sqs.filter(bookstore__in=self.cleaned_data['bookstore'])
        #
        # if self.cleaned_data['bookstore']:
        #     sqs = sqs.filter(bookstore__in=self.cleaned_data['bookstore'])

        return sqs
