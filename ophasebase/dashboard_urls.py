from django.conf.urls import url

from .dashboard_views import (
    NotificationOverview
)


app_name = 'ophasebase'
urlpatterns = [
    url(r'^notifications/$', NotificationOverview.as_view(), name='notifications_overview'),
]
