
import django_mistune
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def markdown(value):
    result = django_mistune.markdown(value)
    result = mark_safe(result)
    return result
