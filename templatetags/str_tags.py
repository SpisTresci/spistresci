from urllib import quote, unquote
from django import template
register = template.Library()

@register.filter
def truncatewords_by_chars(value, limit):
    try:
        if len(value) < limit:
            return value
        else:
            words = value.split(" ")

            words_r = ""
            for word in words:
                if len(words_r) + len(" ") + len(word) > limit:
                    if len(words_r) + len("...") < limit:
                        return words_r + "..."
                    else:
                        return " ".join(words_r.split(" ")[:-1]) + "..."

                else:
                    words_r += " " + word
    except:
        return value

@register.filter
def encode(value):
    return quote(value, '')

@register.filter
def decode(value):
    return unquote(value)
