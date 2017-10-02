from collections import defaultdict
from csv import reader
from io import TextIOWrapper

from django.template import loader
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import FormView, TemplateView, ListView, DetailView
from django.shortcuts import redirect
from django.contrib import messages

from dashboard.components import DashboardAppMixin
from ophasebase.models import Ophase, OphaseCategory
from .dashboard_forms import GroupMassCreateForm, TutorPairingForm
from .models import Person, TutorGroup, AttendanceEvent, OrgaJob, OrgaSelectedJob, HelperJob, HelperSelectedJob
from .nametag import generate_nametag_response, generate_pdf_with_group_pictures


class StaffAppMixin(DashboardAppMixin):
    app_name_verbose = _('Personal')
    app_name = 'staff'
    permissions = ['staff.add_person']

    @property
    def sidebar_links(self):
        return [
            (_('Übersicht'), self.prefix_reverse_lazy('index')),
            (_('Kleingruppen erstellen'),
             self.prefix_reverse_lazy('group_mass_create')),
            (_('Gruppenbilder hinzufügen'),
             self.prefix_reverse_lazy('group_picture_add')),
            (_('Tutoren paaren'), self.prefix_reverse_lazy('tutor_pairing')),
            (_('Termine'), self.prefix_reverse_lazy('event_index')),
            (_('Schilder'), self.prefix_reverse_lazy('nametags'))
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

            context['url_filter_ophase'] = "?ophase__id__exact={}".format(
                current_ophase.id)

            # Create list of current tutors (split by categories)
            context['categories_for_tutors'] = []
            active_categories = Ophase.current().ophaseactivecategory_set.all()
            for ac in active_categories:
                tutors_for_category = Person.objects.filter(ophase=Ophase.current(), is_tutor=True,
                                                            tutor_for=ac.category)
                tutors_count = tutors_for_category.count()
                tutors_string = ", ".join(
                    t.get_name() for t in tutors_for_category) if tutors_count > 0 else "-"

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
                orgas = OrgaSelectedJob.objects.filter(
                    job=aj, person__ophase=Ophase.current())
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
                helpers = HelperSelectedJob.objects.filter(
                    job=aj, person__ophase=Ophase.current())
                helpers_by_status = defaultdict(list)
                for helper in helpers:
                    helpers_by_status[helper.status].append(
                        helper.person.get_name())

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
        template = loader.get_template(
            "staff/dashboard/group_mass_create_success.html")
        context = self.get_context_data()

        current_ophase = Ophase.current()
        if current_ophase is None:
            context['ophase'] = False
        else:
            context['ophase'] = True
            category = OphaseCategory.objects.get(
                id=form.cleaned_data['category'])
            existing_group_names = set(
                group.name for group in TutorGroup.objects.filter(ophase=current_ophase))
            new_groups = []
            context['duplicate_group_count'] = 0
            for name in form.cleaned_data['group_names'].splitlines():
                if name not in existing_group_names:
                    new_groups.append(TutorGroup(
                        ophase=current_ophase, name=name, group_category=category))
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
        pairing_data = {
            int(k[6:]): v for k, v in form.cleaned_data.items() if k.startswith("group-")}
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


class NametagCreation(StaffAppMixin, TemplateView):
    template_name = 'staff/dashboard/nametag_creation.html'

    def get_context_data(self, **kwargs):
        context = super(NametagCreation, self).get_context_data(**kwargs)
        persons = Person.objects.filter(ophase=Ophase.current()).exclude(
            is_helper=True).prefetch_related('orga_jobs').order_by('name')
        context['staff'] = persons
        context['count_staff'] = persons.count()
        context['groupscount'] = TutorGroup.objects.filter(
            ophase=Ophase.current()).count()
        context['groups_without_picture'] = TutorGroup.objects.filter(
            ophase=Ophase.current(), picture='').count()
        return context

    def post(self, request, *args, **kwargs):
        # should generate all nametags
        if request.POST['action'] == 'all_nametags':
            queryset = Person.objects.filter(ophase=Ophase.current()).exclude(
                is_helper=True).prefetch_related('orga_jobs').order_by('name')
            return generate_nametag_response(request, queryset)
        # generate single nametag
        elif request.POST['action'] == 'single_nametag':
            person = {'prename': request.POST['prename'],
                      'name': request.POST['name']}
            if 'tutor' in request.POST:
                person['is_tutor'] = True
            if 'orga' in request.POST:
                person['is_orga'] = True
            if len(request.POST['extrahead']) != 0:
                person['nametag_shortname'] = request.POST['extrahead']
                person['nametag_long'] = request.POST['extrarow']
            person['get_approved_orgajob_names'] = []
            if 'helpdesk' in request.POST:
                person['get_approved_orgajob_names'].append('Helpdesk')
            if 'leitung' in request.POST:
                person['get_approved_orgajob_names'].append('Leitung')
        # generate group signs
        elif request.POST['action'] == 'group_signs':
            return generate_pdf_with_group_pictures(request,
                                                    TutorGroup.objects.filter(
                                                        ophase=Ophase.current()),
                                                    'schilder.pdf',
                                                    'staff/reports/gruppenschilder.tex')
        elif request.POST['action'] == 'group_overview':
            # check whether a file was uploaded
            if not 'roomscsv' in request.FILES:
                messages.error(request, _(
                    'Du hast keine csv-Datei hochgeladen.'))
                return redirect('dashboard:staff:nametags')
            csv = TextIOWrapper(
                request.FILES['roomscsv'].file, encoding=request.encoding)
            rooms = list(reader(csv))[2:]
            groups = TutorGroup.objects.filter(ophase=Ophase.current())
            grouprooms = zip(groups, rooms)
            return generate_pdf_with_group_pictures(request,
                                                    groups,
                                                    'uebersicht.pdf',
                                                    'staff/reports/gruppenuebersicht.tex',
                                                    {'grouprooms': grouprooms})

        return generate_nametag_response(request, [person], filename='schild.pdf')


class GroupPictureAdd(StaffAppMixin, TemplateView):
    permissions = ['staff.edit_tutorgroup']
    template_name = 'staff/dashboard/grouppicture_add.html'

    def get_context_data(self, **kwargs):
        context = super(GroupPictureAdd, self).get_context_data(**kwargs)
        context['groups'] = TutorGroup.objects.filter(ophase=Ophase.current())
        return context

    def post(self, request, *args, **kwargs):
        tutorgroups = TutorGroup.objects.filter(ophase=Ophase.current())
        for group in tutorgroups:
            if request.POST['action-' + str(group.id)] == 'change':
                group.picture = request.FILES[str(group.id)]
                group.save()
            elif request.POST['action-' + str(group.id)] == 'delete':
                group.picture.delete()
        return redirect('dashboard:staff:group_picture_add')
