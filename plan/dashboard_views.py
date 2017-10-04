from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, DetailView
from django.utils.translation import ugettext_lazy as _

from dashboard.components import DashboardAppMixin
from ophasebase.models import OphaseCategory, Ophase
from plan.forms import TimeSlotForm
from plan.models import TimeSlot


class PlanAppMixin(DashboardAppMixin):
    app_name_verbose = "Plan"
    app_name = 'plan'
    permissions = ['plan.add_timeslot']

    @property
    def sidebar_links(self):
        return [
            (_('Übersicht'), self.prefix_reverse_lazy('overview')),
            (_('Neuer Timeslot'), self.prefix_reverse_lazy('timeslot_create')),
        ]


class PlanOverview(PlanAppMixin, ListView):
    model = TimeSlot
    context_object_name = "time_slots"
    template_name = "plan/schedule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Ophase.current().ophaseactivecategory_set.all()
        return context


class PlanCategoryView(PlanAppMixin, DetailView):
    model = OphaseCategory
    context_object_name = "category"
    template_name = "plan/schedule_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Ophase.current().ophaseactivecategory_set.all()
        context["time_slots"] = context["category"].timeslot_set.all()
        return context


class PlanCategoryPublicView(PlanCategoryView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["time_slots"] = context["time_slots"].filter(public=True)
        context["public"] = True
        return context


class TimeSlotCreateView(PlanAppMixin, CreateView):
    success_url = reverse_lazy("dashboard:plan:timeslot_create_success")
    template_name = "plan/timeslot_create.html"
    model = TimeSlot
    form_class = TimeSlotForm


class TimeSlotCreateSuccessView(PlanAppMixin, TemplateView):
    template_name = "plan/timeslot_create_success.html"
