from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView, RedirectView
from smartpages.views import SmartPageView
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from smartpages.models import SmartPage
from activities.models import Activity, Collection
# import markupmirror.urls

sitemaps = {
    'smartpages': SmartPage.sitemap(),
    'activities': Activity.sitemap(priority=0.7),
    'collections': Collection.sitemap(priority=0.6),
}

urlpatterns = i18n_patterns(

    url(r'^$', 'astroedu.views.home', name='home'),
    url(r'^search/', 'astroedu.search.views.search', name='search'),
    url(r'^testing/', include('astroedu.testing.urls', namespace='testing')),
    url(r'^activities/', include('activities.urls', namespace='activities')),
    url(r'^collections/', include('activities.urls_collections', namespace='collections')),

    # (r'^markupmirror/', include(markupmirror.urls.preview)),
    # url('^markdown/', include( 'django_markdown.urls')),

    # url(r'^grappelli/', include('grappelli.urls')),
    # url(r'^tinymce/', include('tinymce.urls')),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/about/', 'astroedu.views.about', name='about'),
    url(r'^admin/history/', include('djangoplicity.adminhistory.urls', namespace='adminhistory_site', app_name='history')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
)

if settings.DEBUG:
    urlpatterns += [
        # test 404 and 500 pages
        url(r'^500/$', TemplateView.as_view(template_name='500.html')),
        url(r'^404/$', TemplateView.as_view(template_name='404.html')),

        # redirects (use nginx rewrite for production)
        url(r'^favicon\.ico/?$', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),

        url(r'^opensearch_desc\.xml/?$', RedirectView.as_view(url='/static/opensearch_desc.xml', permanent=True)),
        url(r'^blog/?$', RedirectView.as_view(url='http://medium.com/@IAUastroedu', permanent=True)),
        url(r'^volunteer/?$', RedirectView.as_view(url='https://unawe.typeform.com/to/UIBI5e', permanent=True)),
        url(r'^a/', include('activities.urls')),
        # serve MEDIA_ROOT (uploaded files) in development
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    ]

urlpatterns += i18n_patterns(
    url(r'^(?P<url>.*/)$', SmartPageView.as_view(), name='smartpage'),
)
