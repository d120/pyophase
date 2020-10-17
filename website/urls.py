from django.urls import path

from . import views

app_name = 'website'
urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage'),
    path('detail/<slug:slug>', views.CategoryDetailView.as_view(),
         name='detail_view'),
    path('helfen/', views.HelperView.as_view(), name='helfen'),
    path('oinforz/', views.OInforzView.as_view(), name='oinforz'),
]
