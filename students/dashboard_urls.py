from django.conf.urls import patterns, url

from .dashboard_components import StudentStatsView

urlpatterns = patterns('',
    url(r'^$', StudentStatsView.as_view(), name='index'),
)

