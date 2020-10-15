from django.urls import path

from .dashboard_views import (
    ExportCertificateView,
    ExportNewsletterSubscriptionView,
    StudentStatsView,
)

app_name = 'students'
urlpatterns = [
    path('', StudentStatsView.as_view(), name='index'),
    path('certificate/', ExportCertificateView.as_view(), name='certificate'),
    path('newsletter/<int:newsletter_id>/export',
         ExportNewsletterSubscriptionView.as_view(), name='newsletter_export'),
]
