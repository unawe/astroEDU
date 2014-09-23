from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.conf import settings

class MailForm(forms.Form):
    # subject = forms.CharField(max_length=100)
    message = forms.CharField()

def email(request):
    sender = 'UNAWE WEBMASTER <%s>' % settings.DEFAULT_FROM_EMAIL
    recipients = ['%s <%s>' % admin for admin in settings.ADMINS]
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            subject = 'astroEDU email test'
            message = form.cleaned_data['message']

            from django.core.mail import send_mail
            result = send_mail(subject, message, sender, recipients)
            return HttpResponse(str(result), mimetype='text/plain')
            #return HttpResponseRedirect('/')
    else:
        form = MailForm()

    return render(request, 'tests/email.html', {
        'form': form,
        'sender' : sender, 
        'recipients' : recipients,
    })


def error(request):
    raise UnknownError


@csrf_exempt
def debug_request(request):
    import json
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    stuff = {'GET': dict(request.GET.iterlists()), 'POST': dict(request.POST.iterlists()), 'HEADERS': request.META, }
    result = pp.pformat(stuff)
    if request.GET.get('json', None):
        json_data = json.loads(request.POST.get('data'))
        result += '\n\n JSON: \n'
        result += pp.pformat(json_data)
    return HttpResponse(result, mimetype='application/json')
