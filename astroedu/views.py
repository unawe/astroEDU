from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from astroedu.activities.models import Activity


def home(request):
    return render(request, 'astroedu/home.html', {'featured': Activity.objects.featured()[0:3], })

@login_required
def about(request):
    import django
    result = 'Django: %s\n' % django.get_version()
    return HttpResponse(result, content_type='text/plain')