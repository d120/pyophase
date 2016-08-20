from django.conf.urls import url

from clothing.dashboard_views import OrderOverView

app_name = 'clothing'
urlpatterns = [
    url(r'^orders$', OrderOverView.as_view(), name='order_overview'),
]
