from django.conf.urls import patterns, url

from exam import views

urlpatterns = patterns('',
    #url(r'^$', views.index, name='index'),
    url(r'assign/$', views.assign, name='assign'),
)
