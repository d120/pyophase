from django.urls import path

from .dashboard_views import (
    FreeClothingView,
    OrderAggregatedView,
    OrderOverView,
)

app_name = 'clothing'
urlpatterns = [
    path('orders/', OrderOverView.as_view(), name='order_overview'),
    path('orders/free/', FreeClothingView.as_view(), name='order_free'),
    path('orders/aggregated/', OrderAggregatedView.as_view(),
         name='order_aggregated'),
]
