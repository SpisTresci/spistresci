# -*- coding: utf-8 -*-

from django import template
register = template.Library()

@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range( value )



@register.filter
def formats_to_readable(value):
    formats_mapping = {
        "ks":u"książka drukowana",
        "cd":u"audio cd",
    }

    if isinstance(value, basestring):
        return formats_mapping[value] if value in formats_mapping else value

    format_names = [item.name for item in list(value)]

    formats = [
        formats_mapping[name]
        if name in formats_mapping else name
        for name in format_names
    ]

    return formats
