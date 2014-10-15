from django.conf.urls import patterns, url

from astroedu.tests import views

urlpatterns = patterns('',
    # url(r'^$', views.list, name='list'),
    url(r'^email/$', views.email),
    url(r'^error/$', views.error),
    url(r'^debug_request/$', views.debug_request),
)