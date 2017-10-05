from django.conf.urls import url

from .dashboard_views import (
    GroupMassCreateView,
    TutorPairingSuccess,
    TutorPairingView,
    AttendanceEventIndexView, AttendanceEventDetailView, StaffOverview,
    NametagCreation, GroupPictureAdd)


app_name = 'staff'
urlpatterns = [
    url(r'^$', StaffOverview.as_view(), name='index'),

    url(r'^group_mass_create/$', GroupMassCreateView.as_view(), name='group_mass_create'),
    url(r'^tutor_pairing/$', TutorPairingView.as_view(), name='tutor_pairing'),
    url(r'^tutor_pairing_success/$', TutorPairingSuccess.as_view(), name='tutor_pairing_success'),
    url(r'^group_picture_add/$', GroupPictureAdd.as_view(), name='group_picture_add'),
    url(r'^event/$', AttendanceEventIndexView.as_view(), name='event_index'),
    url(r'^event/(?P<pk>[0-9]+)/$', AttendanceEventDetailView.as_view(), name='event_detail'),
    url(r'^nametags/$', NametagCreation.as_view(), name='nametags'),
]
