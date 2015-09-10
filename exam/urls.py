from django.conf.urls import patterns, url

from exam import views

urlpatterns = patterns('',
    #url(r'^$', views.index, name='index'),
    url(r'^assignment/new$', views.MakeAssignmentView.as_view(), name='assignment_new'),
    url(r'^assignment/success$', views.MakeAssignmentSuccess.as_view(), name='assignment_success')
)
