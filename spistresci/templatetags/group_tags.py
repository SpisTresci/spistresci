from django import template

register = template.Library()

@register.filter
def belongs_to_group(user, groups):
    """Returns a boolean if the user is in the given group, or comma-separated
    list of groups.

    Usage::

        {% if user|belongs_to_group:"Friends" %}
        ...
        {% endif %}

    or::

        {% if user|belongs_to_group:"Friends,Enemies" %}
        ...
        {% endif %}

    """
    try:
        return bool(user.groups.filter(name__in=groups.split(',')).values('name'))
    except:
        return False

def callMethod(obj, methodName):
    method = getattr(obj, methodName)

    if obj.__dict__.has_key("__callArg"):
        ret = method(*obj.__callArg)
        del obj.__callArg
        return ret
    return method()

def args(obj, arg):
    if not obj.__dict__.has_key("__callArg"):
        obj.__callArg = []

    obj.__callArg += [arg]
    return obj

register.filter("call", callMethod)
register.filter("args", args)
