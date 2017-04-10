from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from dashboard.components import DashboardAppMixin
from students.models import Student



class PlanAppMixin(DashboardAppMixin):
    app_name_verbose = "Plan"
    app_name = 'plan'

    @property
    def sidebar_links(self):
        return [
        ]
