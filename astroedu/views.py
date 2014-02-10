# from django.http import HttpResponse, Http404
from django.shortcuts import render

from astroedu.activities.models import Activity


def home(request):
    # raise Http404
    # from django.core.mail import send_mail, BadHeaderError
    # subject = request.POST.get('subject', 'subj')
    # message = request.POST.get('message', 'mess')
    # from_email = request.POST.get('from_email', 'a@b.com')
    # if subject and message and from_email:
    #     try:
    #         send_mail(subject, message, from_email, ['rinoo7@gmail.com'])
    #     except BadHeaderError:
    #         return HttpResponse('Invalid header found.')
    #     return Http404('/contact/thanks/')
    # else:
    #     # In reality we'd use a form class
    #     # to get proper validation errors.
    #     return HttpResponse('Make sure all fields are entered and valid.')


    return render(request, 'astroedu/home.html', {'featured': Activity.objects.featured()[0:3], })
