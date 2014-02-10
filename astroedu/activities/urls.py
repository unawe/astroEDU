from django.conf.urls import patterns, url

from astroedu.activities import views

urlpatterns = patterns('',
    url(r'^$', views.collections_list, name='collections_list'),
    url(r'^all/$', views.list, name='list'),
    url(r'^(?P<activity_slug>\w*\d{4})/$', views.detail, name='detail'),  # ends with 4 numbers --> it's an activity
    url(r'^(?P<activity_slug>\w*\d{4})/epub$', views.epub, name='epub'),
    url(r'^(?P<collection_slug>\w+)/$', views.collections_detail, name='collections_detail'),  # otherwise --> it's a collection
)
