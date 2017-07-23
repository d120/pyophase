from collections import defaultdict

from django.template import loader
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import FormView, TemplateView, ListView, DetailView

from dashboard.components import DashboardAppMixin
from ophasebase.models import Ophase, OphaseCategory
from .dashboard_forms import GroupMassCreateForm, TutorPairingForm
from .models import Person, TutorGroup, AttendanceEvent, OrgaJob, OrgaSelectedJob, HelperJob, HelperSelectedJob


class StaffAppMixin(DashboardAppMixin):
    app_name_verbose = _('Personal')
    app_name = 'staff'
    permissions = ['staff.add_person']

    @property
    def sidebar_links(self):
        return [
            (_('Übersicht'), self.prefix_reverse_lazy('index')),
            (_('Kleingruppen erstellen'), self.prefix_reverse_lazy('group_mass_create')),
            (_('Tutoren paaren'), self.prefix_reverse_lazy('tutor_pairing')),
            (_('Termine'), self.prefix_reverse_lazy('event_index')),
        ]


class StaffOverview(StaffAppMixin, TemplateView):
    template_name = "staff/dashboard/staff_overview.html"

    def get_context_data(self):
        context = super().get_context_data()

        current_ophase = Ophase.current()
        context['ophase_title'] = _('Ophase')
        if current_ophase is not None:
            context['ophase_title'] = str(current_ophase)

            Staff = Person.objects.filter(ophase=current_ophase)
            context['count_staff'] = Staff.count()
            context['count_tutor'] = Staff.filter(is_tutor=True).count()
            context['count_orga'] = Staff.filter(is_orga=True).count()
            context['count_helper'] = Staff.filter(is_helper=True).count()

            context['url_filter_ophase'] = "?ophase__id__exact={}".format(current_ophase.id)

            # Create list of current tutors (split by categories)
            context['categories_for_tutors'] = []
            active_categories = Ophase.current().ophaseactivecategory_set.all()
            for ac in active_categories:
                tutors_for_category = Person.objects.filter(ophase=Ophase.current(), is_tutor=True, tutor_for=ac.category)
                tutors_count = tutors_for_category.count()
                tutors_string = ", ".join(t.get_name() for t in tutors_for_category) if tutors_count > 0 else "-"

                context['categories_for_tutors'].append(
                    {
                        "name": ac.category.name,
                        "count": tutors_count,
                        "tutors": tutors_string,
                        "filter": "?ophase__id__exact={}&tutorstatus={}".format(current_ophase.id, ac.category.id)
                    }
                )

            # Create a list of all orgajobs and fill them with persons that selected this job
            context['orga_jobs'] = []
            active_jobs = OrgaJob.filter_jobs_for_ophase_current()
            for aj in active_jobs:
                orgas = OrgaSelectedJob.objects.filter(job=aj, person__ophase=Ophase.current())
                orgas_by_status = defaultdict(list)
                for orga in orgas:
                    orgas_by_status[orga.status].append(orga.person.get_name())

                context['orga_jobs'].append(
                    {
                        "name": aj.label,
                        "orga": ", ".join(orgas_by_status["o"]),
                        "co_orga": ", ".join(orgas_by_status["c"]),
                        "interested": ", ".join(orgas_by_status["i"])
                    }
                )

            # Create a list of all helper and fill them with persons that selected this job
            context['helper_jobs'] = []
            active_jobs = HelperJob.filter_jobs_for_ophase_current()
            for aj in active_jobs:
                helpers = HelperSelectedJob.objects.filter(job=aj, person__ophase=Ophase.current())
                helpers_by_status = defaultdict(list)
                for helper in helpers:
                    helpers_by_status[helper.status].append(helper.person.get_name())

                context['helper_jobs'].append(
                    {
                        "name": aj.label,
                        "selected": ", ".join(helpers_by_status["e"]),
                        "interested": ", ".join(helpers_by_status["i"])
                    }
                )

        return context


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
            category = OphaseCategory.objects.get(id=form.cleaned_data['category'])
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
