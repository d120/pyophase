from django.conf.urls import patterns, url

from .dashboard_views import StudentStatsView, ExportCertificateView, ExportNewsletterSubscriptionView, \
    NewsletterOverviewView

urlpatterns = patterns('',
    url(r'^$', StudentStatsView.as_view(), name='index'),
    url(r'^certificate$', ExportCertificateView.as_view(), name='certificate'),
    url(r'^newsletter/$', NewsletterOverviewView.as_view(), name='newsletter'),
    url(r'^newsletter/(?P<newsletter_id>[0-9]+)/export/$', ExportNewsletterSubscriptionView.as_view(), name='newsletter_export'),
)

