from django.conf.urls import patterns, url

from .dashboard_views import StudentStatsView, ExportCertificateView

urlpatterns = patterns('',
    url(r'^$', StudentStatsView.as_view(), name='index'),
    url(r'^certificate$', ExportCertificateView.as_view(), name='certificate'),
)

