from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def key(d, key_name):
    return d[key_name]
