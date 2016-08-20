from django.conf.urls import url

from clothing import views

app_name = 'clothing'
urlpatterns = [
    url(r'^order/new/$', views.OrderClothingView.as_view(), name='order_new'),
    url(r'^order/success/$', views.OrderClothingSuccessView.as_view(), name='order_success'),
]
