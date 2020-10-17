from django.urls import path

from . import views

app_name = 'clothing'
urlpatterns = [
    path('', views.ClothingPersonalOverview.as_view(), name='overview'),
    path('order/', views.ClothingOrderView.as_view(), name='order_new'),
    path('order/<int:pk>/edit/', views.ClothingOrderEditView.as_view(),
         name='order_edit'),
    path('order/<int:pk>/delete/', views.ClothingOrderDeleteView.as_view(),
         name='order_delete'),
    path('success/', views.ClothingOrderSuccessView.as_view(),
         name='order_success'),
    path('forbidden/', views.ClothingOrderForbiddenView.as_view(),
         name='order_forbidden'),
]
