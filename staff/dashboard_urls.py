from django.conf.urls import url

from .dashboard_views import (
    GroupMassCreateView,
    TutorPairingSuccess,
    TutorPairingView,
)


app_name = 'staff'
urlpatterns = [
    url(r'^group_mass_create$', GroupMassCreateView.as_view(), name='group_mass_create'),
    url(r'^tutor_pairing$', TutorPairingView.as_view(), name='tutor_pairing'),
    url(r'^tutor_pairing_success$', TutorPairingSuccess.as_view(), name='tutor_pairing_success'),
]
