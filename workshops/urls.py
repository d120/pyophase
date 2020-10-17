from django.urls import path

from . import views

app_name = 'workshops'
urlpatterns = [
    path('', views.WorkshopCreate.as_view(), name='create'),
    path('success/', views.WorkshopCreateSuccess.as_view(),
         name='create_success'),
]
