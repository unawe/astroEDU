from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from astroedu.activities.models import Activity, Collection
# import markupmirror.urls

# generate sitemap
activity_list = {
    'queryset': Activity.objects.all(),
    # 'date_field': 'published',
}
collection_list = {
    'queryset': Collection.objects.all(),
}
sitemaps = {
    'flatpages': FlatPageSitemap,
    'activities': GenericSitemap(activity_list, priority=0.7),
    'collections': GenericSitemap(collection_list, priority=0.6),
}

# enable the admin:
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'astroedu.views.home', name='home'),
    url(r'^tests/', include('astroedu.tests.urls', namespace='tests')),
    url(r'^activities/', include('astroedu.activities.urls', namespace='activities')),
    url(r'^collections/', include('astroedu.activities.urls_collections', namespace='collections')),


    # url(r'^search/', include('haystack.urls')),

    # (r'^markupmirror/', include(markupmirror.urls.preview)),
    # url('^markdown/', include( 'django_markdown.urls')),

    # url(r'^grappelli/', include('grappelli.urls')),
    # url(r'^tinymce/', include('tinymce.urls')),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/history/', include('djangoplicity.adminhistory.urls', namespace="adminhistory_site", app_name="history" )),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^500/$', TemplateView.as_view(template_name="500.html")),
        (r'^404/$', TemplateView.as_view(template_name="404.html")),
        # redirects (use nginx rewrite for production)
        url(r'^blog/?$', lambda x: HttpResponseRedirect('http://medium.com/@IAUastroEDU')),
        url(r'^volunteer/?$', lambda x: HttpResponseRedirect('https://unawe.typeform.com/to/UIBI5e')),
        url(r'^collections/?$', lambda x: HttpResponseRedirect('/activities/')),
    )


from haystack.forms import SearchForm, ModelSearchForm, HighlightedModelSearchForm, FacetedSearchForm
from astroedu.activities.forms import MultiFacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView, FacetedSearchView, search_view_factory

sqs = SearchQuerySet().facet('age').facet('level').facet('time').facet('group').facet('supervised').facet('cost').facet('location').facet('skills').facet('learning')

# urlpatterns += patterns(
#     'haystack.views',
#     url(r'^search/', search_view_factory(
#         view_class=SearchView,
#         # searchqueryset=sqs,
#         form_class=SearchForm,
#         ), name='haystack_search'),
# )

urlpatterns += patterns(
    'haystack.views',
    url(r'^search/', search_view_factory(
        view_class=FacetedSearchView,
        searchqueryset=sqs,
        form_class=FacetedSearchForm,
        ), name='haystack_search'),
)

# urlpatterns += patterns(
#     'haystack.views',
#     url(r'^search2/', search_view_factory(
#         view_class=FacetedSearchView,
# #         searchqueryset=sqs,
#         form_class=MultiFacetedSearchForm,
#         ), name='haystack_search'),
# )

# serve MEDIA_ROOT (uploaded files) in development
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

# Flatpages fallback    
urlpatterns += patterns('django.contrib.flatpages.views',
    (r'^(?P<url>.*/)$', 'flatpage'),
)

