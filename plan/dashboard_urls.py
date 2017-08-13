from django.conf.urls import url

from plan.dashboard_views import PlanOverview, TimeSlotCreateView, TimeSlotCreateSuccessView


app_name = 'plan'
urlpatterns = [
    url(r'^schedule/$', PlanOverview.as_view(), name='overview'),
    url(r'^timeslot/new/$', TimeSlotCreateView.as_view(), name='timeslot_create'),
    url(r'^timeslot/new/success/$', TimeSlotCreateSuccessView.as_view(), name='timeslot_create_success'),
]
