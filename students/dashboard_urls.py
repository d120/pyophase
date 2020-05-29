from django.conf.urls import url

from .dashboard_views import (
    ExportCertificateView,
    ExportNewsletterSubscriptionView,
    StudentStatsView,
)


app_name = 'students'
urlpatterns = [
    url(r'^$', StudentStatsView.as_view(), name='index'),
    url(r'^certificate/$', ExportCertificateView.as_view(), name='certificate'),
    url(r'^newsletter/(?P<newsletter_id>[0-9]+)/export/$', ExportNewsletterSubscriptionView.as_view(), name='newsletter_export'),
]
