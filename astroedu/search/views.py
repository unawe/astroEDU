from operator import itemgetter

from django.shortcuts import render

from . import whoosh_utils
from astroedu.activities.models import Activity, MetadataOption
from .forms import SearchForm


def _pimp_facets(facets):

    # create a cache of MetadataOption
    options = {}
    for obj in MetadataOption.objects.all():
        options[(obj.code, obj.group)] = (obj.code, obj.title, obj.position)

    # go through the search result facets, to sort them and add the title
    for facet, values in facets['fields'].iteritems():
        if facet != 'keywords':
            new_values = []
            for code, count in values:
                # obj = MetadataOption.objects.get(code=code, group=facet)
                # new_values.append((code, obj.title, count, obj.position))
                opt = options[(code, facet)]
                new_values.append((code, opt[1], count, opt[2]))
            # sort by the position field
            facets['fields'][facet] = sorted(new_values, key=itemgetter(3))

    return facets


def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        # search_query = request.GET['q']
        search_query = form.cleaned_data['q']
        search_result = whoosh_utils.search(search_query, queryfacets=form.cleaned_data)
        context = {
            'query': search_query,
            'facets': _pimp_facets(search_result['facets']),
            'page': {'object_list': search_result['results']},
            'request': request,
            'form': form,
        }
    else:
        context = {
            'request': request,
            'form': form,
        }

    if not 'page' in context or not context['page']['object_list']:
        context['featured'] = Activity.objects.featured()[0:3]

    return render(request, 'search/search.html', context)
