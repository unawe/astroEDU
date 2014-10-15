from django.conf.urls import patterns, url

from astroedu.activities import views

urlpatterns = patterns('',
    url(r'^$', views.collections_list, name='list'),
    url(r'^(?P<collection_slug>[a-zA-Z0-9-]+)/$', views.collections_detail, name='detail'), 
)
