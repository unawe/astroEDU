from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.conf import settings


class MailForm(forms.Form):
    message = forms.CharField()


def email(request):
    sender = 'UNAWE WEBMASTER <%s>' % settings.DEFAULT_FROM_EMAIL
    recipients = ['%s <%s>' % admin for admin in settings.ADMINS]
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            subject = 'astroedu email test'
            message = form.cleaned_data['message']

            from django.core.mail import send_mail
            result = send_mail(subject, message, sender, recipients)
            return HttpResponse(str(result), content_type='text/plain')
    else:
        form = MailForm()

    return render(request, 'testing/email.html', {
        'form': form,
        'sender': sender,
        'recipients': recipients,
    })


def markdown(request):
    from django_mistune import markdown
    mtext = '## Boa Tarde\n\n_TTX_\n'
    htext = markdown(mtext)
    return render(request, 'testing/markdown.html', {'value': htext + '\n\n---\n\n' + mtext})


def error(request):
    raise UnknownError


@csrf_exempt
def debug_request(request):
    import json
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    stuff = {'GET': dict(request.GET), 'POST': dict(request.POST), 'HEADERS': request.META, }
    result = pp.pformat(stuff)
    if request.GET.get('json', None):
        json_data = json.loads(request.POST.get('data'))
        result += '\n\n JSON: \n'
        result += pp.pformat(json_data)
    return HttpResponse(result, content_type='application/json')
