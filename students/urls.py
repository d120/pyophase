from django.urls import path

from . import views

app_name = 'students'
urlpatterns = [
    path('', views.StudentAddProtected.as_view(),
         kwargs={'exam_enabled': True}, name='registration'),
    path('master/', views.StudentAdd.as_view(), kwargs={'exam_enabled': False},
         name='registration-master'),
    path('success/', views.StudentAddSuccess.as_view(),
         name='registration_success'),
]
