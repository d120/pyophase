from django.urls import include, path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('permissionmissing/', views.PermissionMissingView.as_view(),
         name='missing_permission'),

    path('my/', views.PersonalOverview.as_view(), name='personal_overview'),

    path('staff/', include('staff.dashboard_urls', namespace='staff')),
    path('students/',
         include('students.dashboard_urls', namespace='students')),
    path('exam/', include('exam.dashboard_urls', namespace='exam')),
    path('clothing/',
         include('clothing.dashboard_urls', namespace='clothing')),
]
