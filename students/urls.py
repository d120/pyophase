from django.conf.urls import patterns, url

from students import views

urlpatterns = patterns('',
    url(r'^$', views.StudentAdd.as_view(), name='registration'),
    url(r'success/$', views.StudentAddSuccess.as_view(), name='registration_success'),
)
