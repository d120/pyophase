from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView

from dashboard.components import DashboardAppMixin
from ophasebase.models import Notification


class OphasebaseAppMixin(DashboardAppMixin):
    app_name_verbose = _('Base')
    app_name = 'ophasebase'
    permissions = []

    @property
    def sidebar_links(self):
        return [
            (_('Notifications'), self.prefix_reverse_lazy('notifications_overview')),
        ]


class NotificationOverview(OphasebaseAppMixin, ListView):
    model = Notification
    context_object_name = "notifications"
    template_name = "ophasebase/dashboard/notifications.html"

    def get_queryset(self):
        #TODO Replace with filtered version
        return Notification.objects.all()
