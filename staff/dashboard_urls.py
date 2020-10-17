from django.urls import path

from .dashboard_views import (
    GroupMassCreateView,
    GroupMassCreateViewSuccess,
    TutorPairingSuccess,
    TutorPairingView,
    AttendanceEventIndexView, AttendanceEventDetailView, StaffOverview,
    NametagCreation, GroupPictureAdd)

app_name = 'staff'
urlpatterns = [
    path('', StaffOverview.as_view(), name='index'),
    path('group_mass_create/', GroupMassCreateView.as_view(),
         name='group_mass_create'),
    path('group_mass_create_success/', GroupMassCreateViewSuccess.as_view(),
         name='group_mass_create_success'),
    path('tutor_pairing/', TutorPairingView.as_view(), name='tutor_pairing'),
    path('tutor_pairing_success/', TutorPairingSuccess.as_view(),
         name='tutor_pairing_success'),
    path('group_picture_add/', GroupPictureAdd.as_view(),
         name='group_picture_add'),
    path('event/', AttendanceEventIndexView.as_view(), name='event_index'),
    path('event/<int:pk>/', AttendanceEventDetailView.as_view(),
         name='event_detail'),
    path('nametags/', NametagCreation.as_view(), name='nametags'),
]
