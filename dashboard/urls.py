from django.conf.urls import patterns, url, include

from . import views

urlpatterns = patterns('',
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^permissionmissing$', views.PermissionMissingView.as_view(), name='missing_permission'),
    url(r'^students/', include('students.dashboard_urls', namespace='students')),
)
