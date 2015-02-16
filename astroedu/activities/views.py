import re 

from django.http import HttpResponse, Http404, HttpResponsePermanentRedirect
from django.shortcuts import render
from astroedu.django_ext.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings

from astroedu.activities.models import Activity, Collection, ACTIVITY_SECTIONS, ACTIVITY_METADATA #, Richtext


def list(request):
    lst = get_list_or_404(Activity, user=request.user, select_related=('authors'), order_by='-release_date')
    return render(request, 'activities/list.html', {'object_list': lst, })

def detail(request, slug):
    obj = get_object_or_404(Activity, user=request.user, slug=slug)
    return render(request, 'activities/detail.html', {'object': obj, 'sections': ACTIVITY_SECTIONS, 'sections_meta': ACTIVITY_METADATA, })

def detail_by_code(request, code):
    obj = get_object_or_404(Activity, user=request.user, code=code)
    return HttpResponsePermanentRedirect(obj.get_absolute_url())

def epub(request, code):
    obj = get_object_or_404(Activity, user=request.user, code=code)
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
