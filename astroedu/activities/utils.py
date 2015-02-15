import os
import re
import urllib

import bleach
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives, send_mail, BadHeaderError
from django.conf import settings

def beautify_age_range(age_ranges):
    'Unifies a list of age ranges into a string. Input list must be sorted.'
    age_min = ''
    age_max = ''
    error = False

    for item in age_ranges:
        if ' - ' in item:
            x, y = item.split(' - ')
            if not age_min and not age_max:  # first range
                age_min = x
                age_max = x
            elif not age_max:  # the previous range was n+, that should have been the last
                error = True
            if x == age_max:  # checking the list is sorted; previous range max = this range min
                age_max = y
            else:
                error = True
        elif '+' in item:
            x = item[:item.find('+')]
            if x == age_max:  # checking the list is sorted; previous range max = this range min
                age_max = ''
            else:
                error = True
            break

    if error:
        return ' '.join(age_ranges)
    elif age_max:
        return age_min + ' - ' + age_max
    elif age_min:
        return age_min + '+'
    else:
        return ' '.join(age_ranges)

class UnsupportedMediaPathException(Exception):
    pass
    
def local_resource(uri):
    """
    Returns the full file path and a relative path for the resource
    """
    if uri.startswith(settings.MEDIA_URL):
        local = uri.replace(settings.MEDIA_URL, '')
        path = os.path.join(settings.MEDIA_ROOT, local)
    elif uri.startswith(settings.STATIC_URL):
        local = uri.replace(settings.STATIC_URL, '')
        path = os.path.join(settings.STATIC_ROOT, local)
    else:
        raise UnsupportedMediaPathException('media urls must start with %s or %s' % (settings.MEDIA_URL, settings.STATIC_URL))

    # return path
    return urllib.unquote(path), urllib.unquote(local)

# def send_notification_mail():
#     # import logging
#     # logger = logging.getLogger(__name__)
#
#     from_email = settings.DEFAULT_FROM_EMAIL
#     to = 'rinoo7@gmail.com'
#    
#     subject = 'test email'
#     html_body = '<b>test</b> email'
#     text_body = strip_tags( html_body )
#    
#     # Send
#
#     if subject and html_body and from_email and to:
#         #logger.info(settings.EMAIL_HOST)
#         msg = EmailMultiAlternatives( subject, text_body, from_email, [to] )
#         msg.attach_alternative( html_body, 'text/html' )
#         msg.send()
#    
#     return

def bleach_clean(text):
    result = bleach.clean(text, settings.BLEACH_ALLOWED_TAGS, settings.BLEACH_ALLOWED_ATTRIBUTES, settings.BLEACH_ALLOWED_STYLES, strip=False, strip_comments=False)

    # bleach escaped too much stuff, let's put it back
    result = re.sub(r'&lt;(.*)=""/&gt;', r'<\1>', result)  # automatic links
    result = re.sub(r'</?br\w?/?>', r'<br/>', result)  # we prefer xhtml line breaks

    return result


