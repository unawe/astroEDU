import re 

from django.http import HttpResponse, Http404
from django.shortcuts import render
from astroedu.django_ext.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings

from astroedu.activities.models import Activity, Collection #, Richtext

def _get_activity_or_404(user, activity_identifier):
    if re.match('^\w*\d{4}$', activity_identifier):
        obj = get_object_or_404(Activity, user=user, code=activity_identifier)
    else:
        obj = get_object_or_404(Activity, user=user, slug=activity_identifier)
    return obj 

def list(request):
    # lst = Activity.objects.all()  #.order_by('-pub_date')[:5]
    lst = get_list_or_404(Activity, user=request.user, order_by='-release_date')
    #.order_by('-release_date')
    print type(lst)
    # lst = Activity.objects.featured()  #.order_by('-pub_date')[:5]
    return render(request, 'activities/list.html', {'object_list': lst, })

    # from datetime import datetime
    # from django.utils.timezone import utc, now
    # return HttpResponse(
    #     'datetime.now ' + str(datetime.now()) + '<br/>'
    #     + 'utcnow ' + str(datetime.utcnow().replace(tzinfo=utc)) + '<br/>'
    #     + 'django.utils.timezone.now ' + str(now()) + '<br/>'
    # )


def detail(request, activity_identifier):
    obj = _get_activity_or_404(user=request.user, activity_identifier=activity_identifier)
    return render(request, 'activities/detail.html', {'object': obj})

def epub(request, activity_identifier):
    obj = _get_activity_or_404(user=request.user, activity_identifier=activity_identifier)
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
