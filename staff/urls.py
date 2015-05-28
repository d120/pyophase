from django.conf.urls import patterns, url

from staff import views

urlpatterns = patterns('',
    url(r'^$', views.StaffAdd.as_view(), name='registration'),
    url(r'success/$', views.StaffAddSuccess.as_view(), name='registration_success'),
)
