from django.conf.urls import patterns, url

from .dashboard_views import GroupMassCreateView

urlpatterns = patterns('',
    url(r'^group_mass_create$', GroupMassCreateView.as_view(), name='group_mass_create'),
)
