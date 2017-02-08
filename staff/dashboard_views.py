from django.template import loader
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import FormView, TemplateView, ListView, DetailView

from dashboard.components import DashboardAppMixin
from ophasebase.models import Ophase
from .dashboard_forms import GroupMassCreateForm, TutorPairingForm
from .models import GroupCategory, Person, TutorGroup, AttendanceEvent


class StaffAppMixin(DashboardAppMixin):
    app_name_verbose = _('Personal')
    app_name = 'staff'
    permissions = ['staff.add_person']

    @property
    def sidebar_links(self):
        return [
            (_('Kleingruppen erstellen'), self.prefix_reverse_lazy('group_mass_create')),
            (_('Tutoren paaren'), self.prefix_reverse_lazy('tutor_pairing')),
            (_('Termine'), self.prefix_reverse_lazy('event_index')),
        ]


class GroupMassCreateView(StaffAppMixin, FormView):
    permissions = ['staff.add_tutorgroup']
    template_name = 'staff/dashboard/group_mass_create.html'
    form_class = GroupMassCreateForm

    def form_valid(self, form):
        template = loader.get_template("staff/dashboard/group_mass_create_success.html")
        context = self.get_context_data()

        current_ophase = Ophase.current()
        if current_ophase is None:
            context['ophase'] = False
        else:
            context['ophase'] = True
            category = GroupCategory.objects.get(id=form.cleaned_data['category'])
            existing_group_names = set(group.name for group in TutorGroup.objects.filter(ophase=current_ophase))
            new_groups = []
            context['duplicate_group_count'] = 0
            for name in form.cleaned_data['group_names'].splitlines():
                if name not in existing_group_names:
                    new_groups.append(TutorGroup(ophase=current_ophase, name=name, group_category=category))
                else:
                    context['duplicate_group_count'] += 1
            context['new_group_count'] = len(new_groups)
            TutorGroup.objects.bulk_create(new_groups)

        return TemplateResponse(self.request, template, context=context)


class TutorPairingView(StaffAppMixin, FormView):
    permissions = ['staff.edit_tutorgroup']
    template_name = 'staff/dashboard/tutor_pairing.html'
    form_class = TutorPairingForm
    success_url = reverse_lazy('dashboard:staff:tutor_pairing_success')

    def form_valid(self, form):
        pairing_data = {int(k[6:]): v for k, v in form.cleaned_data.items() if k.startswith("group-")}
        for group_id, choices in pairing_data.items():
            group = TutorGroup.objects.get(id=group_id)
            new_tutors = Person.objects.filter(id__in=choices)
            group.tutors.set(new_tutors)
        return super().form_valid(form)


class TutorPairingSuccess(StaffAppMixin, TemplateView):
    permissions = ['staff.edit_tutorgroup']
    template_name = "staff/dashboard/tutor_pairing_success.html"


class AttendanceEventIndexView(StaffAppMixin, ListView):
    permissions = ['staff.edit_attendance']
    model = AttendanceEvent
    template_name = "staff/dashboard/events_overview.html"
    context_object_name = "events"


class AttendanceEventDetailView(StaffAppMixin, DetailView):
    permissions = ['staff.edit_attendance']
    model = AttendanceEvent
    template_name = "staff/dashboard/event.html"
    context_object_name = "event"
