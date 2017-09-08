from django.conf.urls import url

from . import views


app_name = 'clothing'
urlpatterns = [
    url(r'^$', views.ClothingPersonalOverview.as_view(), name='overview'),
    url(r'^order/$', views.ClothingOrderView.as_view(), name='order_new'),
    url(r'^order/(?P<pk>[0-9]+)/edit/$', views.ClothingOrderEditView.as_view(), name='order_edit'),
    url(r'^order/(?P<pk>[0-9]+)/delete/$', views.ClothingOrderDeleteView.as_view(), name='order_delete'),
    url(r'^success/$', views.ClothingOrderSuccessView.as_view(), name='order_success'),
    url(r'^forbidden/$', views.ClothingOrderForbiddenView.as_view(), name='order_forbidden'),
]
