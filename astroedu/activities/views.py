import re 

from django.http import HttpResponse, Http404, HttpResponsePermanentRedirect
from django.shortcuts import render
from astroedu.django_ext.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings

from astroedu.activities.models import Activity, Collection #, Richtext


def list(request):
    lst = get_list_or_404(Activity, user=request.user, order_by='-release_date')
    return render(request, 'activities/list.html', {'object_list': lst, })

def detail(request, activity_slug):
    obj = get_object_or_404(Activity, user=request.user, slug=activity_slug)
    return render(request, 'activities/detail.html', {'object': obj})

def detail_by_code(request, activity_code):
    obj = get_object_or_404(Activity, user=request.user, code=activity_code)
    return HttpResponsePermanentRedirect(obj.get_absolute_url())

def epub(request, activity_code):
    obj = get_object_or_404(Activity, user=request.user, code=activity_code)
    return render(request, 'activities/epub.html', {'object': obj})

# def rich(request, obj_id):
#     obj = get_object_or_404(Richtext, id=obj_id)
#     return render(request, 'activities/rich.html', {'object': obj})

# def search(request):
#     context = {}
#     return render(request, 'activities/index.html', context)


# def test(request):
#     return HttpResponse(
#         '<br/> BASE_DIR: ' + settings.BASE_DIR) 

def collections_list(request):
    lst = get_list_or_404(Collection, user=request.user)
    return render(request, 'collections/list.html', {'object_list': lst, })

def collections_detail(request, collection_slug):
    obj = get_object_or_404(Collection, user=request.user, slug=collection_slug)
    return render(request, 'collections/detail.html', {'object': obj})
