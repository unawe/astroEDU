from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.conf import settings

class MailForm(forms.Form):
    # subject = forms.CharField(max_length=100)
    message = forms.CharField()

def email(request):
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            subject = 'astroEDU email test'
            message = form.cleaned_data['message']
            sender = 'UNAWE WEBMASTER <%s>' % settings.DEFAULT_FROM_EMAIL
            recipients = ['%s <%s>' % admin for admin in settings.ADMINS]

            from django.core.mail import send_mail
            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/')
    else:
        form = MailForm()

    return render(request, 'tests/email.html', {
        'form': form,
    })


def error(request):
    raise UnknownError


def debug_request(request):
	import pprint
    pp = pprint.PrettyPrinter(indent=4)
    stuff = {'GET': dict(request.GET.iterlists()), 'POST': dict(request.POST.iterlists()), 'HEADERS': request.META, }
    return HttpResponse(pp.pformat(stuff), mimetype='application/json')
