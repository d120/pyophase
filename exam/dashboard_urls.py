from django.urls import path

from . import dashboard_views

app_name = 'exam'
urlpatterns = [
    path('assignment/new/', dashboard_views.MakeAssignmentView.as_view(),
         name='assignment_new'),
    path('assignment/success/',
         dashboard_views.MakeAssignmentSuccess.as_view(),
         name='assignment_success'),
    path('assignment/<int:assignment_id>/name_list/',
         dashboard_views.AssignmentNameListView.as_view(),
         name='assignment_name_list'),
]
