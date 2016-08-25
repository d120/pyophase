from django.conf.urls import url

from . import views


app_name = 'clothing'
urlpatterns = [
    url(r'^$', views.OrderClothingView.as_view(), name='order_new'),
    url(r'^success/$', views.OrderClothingSuccessView.as_view(), name='order_success'),
]
