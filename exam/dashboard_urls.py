from django.conf.urls import patterns, url

from . import dashboard_views

urlpatterns = patterns('',
    url(r'^assignment/new$', dashboard_views.MakeAssignmentView.as_view(), name='assignment_new'),
    url(r'^assignment/success$', dashboard_views.MakeAssignmentSuccess.as_view(), name='assignment_success')
)
