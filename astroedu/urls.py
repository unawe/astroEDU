from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.http import HttpResponseRedirect
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap
from astroedu.activities.models import Activity, Collection
# import markupmirror.urls

sitemaps = {
    'flatpages': FlatPageSitemap,
    'activities': Activity.sitemap(priority=0.7),
    'collections': Collection.sitemap(priority=0.6),
}

urlpatterns = patterns('',

    url(r'^$', 'astroedu.views.home', name='home'),
    url(r'^search/', 'astroedu.search.views.search', name='search'),
    url(r'^testing/', include('astroedu.testing.urls', namespace='testing')),
    url(r'^activities/', include('astroedu.activities.urls', namespace='activities')),
    url(r'^collections/', include('astroedu.activities.urls_collections', namespace='collections')),

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
        # test 404 and 500 pages
        (r'^500/$', TemplateView.as_view(template_name="500.html")),
        (r'^404/$', TemplateView.as_view(template_name="404.html")),
        # redirects (use nginx rewrite for production)
        (r'^favicon\.ico/?$', RedirectView.as_view(url='/static/favicon.ico')),
        (r'^opensearch_desc\.xml/?$', RedirectView.as_view(url='/static/opensearch_desc.xml')),
        (r'^blog/?$', RedirectView.as_view(url='http://medium.com/@IAUastroEDU')),
        (r'^volunteer/?$', RedirectView.as_view(url='https://unawe.typeform.com/to/UIBI5e')),
        url(r'^a/', include('astroedu.activities.urls')),
        # serve MEDIA_ROOT (uploaded files) in development
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

# Flatpages fallback    
urlpatterns += patterns('django.contrib.flatpages.views',
    (r'^(?P<url>.*/)$', 'flatpage'),
)

