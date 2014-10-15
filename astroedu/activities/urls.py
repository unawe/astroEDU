from django.conf.urls import patterns, url

from astroedu.activities import views

urlpatterns = patterns('',
    url(r'^$', views.list, name='list'),
    #url(r'^(?P<activity_slug>\w*\d{4})/epub$', views.epub, name='epub'),
    url(r'^(?P<activity_slug>[a-zA-Z0-9-]+)/$', views.detail, name='detail'),
)
