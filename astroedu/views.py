# from django.http import HttpResponse, Http404
from django.shortcuts import render

from astroedu.activities.models import Activity


def home(request):
    return render(request, 'astroedu/home.html', {'featured': Activity.objects.featured()[0:3], })
