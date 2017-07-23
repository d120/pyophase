from django.conf.urls import include, url

from . import views


app_name = 'dashboard'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^permissionmissing/$', views.PermissionMissingView.as_view(), name='missing_permission'),

    url(r'^my/$', views.PersonalOverview.as_view(), name='personal_overview'),

    url(r'^staff/', include('staff.dashboard_urls', namespace='staff')),
    url(r'^students/', include('students.dashboard_urls', namespace='students')),
    url(r'^exam/', include('exam.dashboard_urls', namespace='exam')),
    url(r'^clothing/', include('clothing.dashboard_urls', namespace='clothing')),
]
