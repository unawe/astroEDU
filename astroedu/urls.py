from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
# import markupmirror.urls

# enable the admin:
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'astroedu.views.home', name='home'),
    url(r'^activities/', include('astroedu.activities.urls', namespace='activities')),

    # url(r'^search/', include('haystack.urls')),

    # (r'^markupmirror/', include(markupmirror.urls.preview)),
    # url('^markdown/', include( 'django_markdown.urls')),

    # url(r'^grappelli/', include('grappelli.urls')),
    # url(r'^tinymce/', include('tinymce.urls')),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/history/', include('djangoplicity.adminhistory.urls', namespace="adminhistory_site", app_name="history" )),
    url(r'^admin/', include(admin.site.urls)),
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

