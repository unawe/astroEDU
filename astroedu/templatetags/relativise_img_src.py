import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def relativise_img_src(value, activity):
    '''Run this filter through some HTML to prepend the local URL to attached images'''
    new_start = 0
    result = ''
    for m in re.finditer(ur'<img src="(.*?)".*?>', value):
        new_src = u'<img src="%s"/>' % activity.attachment_url(m.group(1))
        result += value[new_start:m.start()] + new_src
        new_start = m.end()
    result += value[new_start:]

    result = mark_safe(result)
    return result

