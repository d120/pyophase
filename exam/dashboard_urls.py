from django.conf.urls import patterns, url

from . import dashboard_views

urlpatterns = [
    url(r'^assignment/$', dashboard_views.AssignmentIndexView.as_view(), name='assignment'),
    url(r'^assignment/new$', dashboard_views.MakeAssignmentView.as_view(), name='assignment_new'),
    url(r'^assignment/success$', dashboard_views.MakeAssignmentSuccess.as_view(), name='assignment_success'),
    url(r'^assignment/(?P<pk>[0-9]+)/$', dashboard_views.AssignmentDetailView.as_view(), name='assignment_detail'),
    url(r'^assignment/(?P<assignment_id>[0-9]+)/name_list', dashboard_views.AssignmentNameListView.as_view(), name='assignment_name_list'),
]
