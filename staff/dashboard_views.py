from collections import defaultdict
from csv import reader
from io import TextIOWrapper, BytesIO
from zipfile import ZipFile
from functools import partial

from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import FormView, TemplateView, ListView, DetailView
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q

from dashboard.components import DashboardAppMixin
from ophasebase.models import Ophase, OphaseCategory
from .dashboard_forms import GroupMassCreateForm, TutorPairingForm
from .models import Person, TutorGroup, AttendanceEvent, OrgaJob, OrgaSelectedJob, HelperJob, HelperSelectedJob
from .nametag import generate_nametag_response, generate_pdf_with_group_pictures, generate_pdf_with_group_pictures_response, generate_nametags, cycle_bucket
from .forms import TutorGroupSelect


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
    success_url = reverse_lazy('dashboard:staff:group_mass_create_success')

    def form_valid(self, form):
        session = self.request.session

        current_ophase = Ophase.current()
        if current_ophase is None:
            session['gmc_ophase'] = False
        else:
            session['gmc_ophase'] = True

            category = OphaseCategory.objects.get(id=form.cleaned_data['category'])

            existing_group_names = set(
                group.name for group in TutorGroup.objects.filter(ophase=current_ophase))
            submitted_group_names = set(form.cleaned_data['group_names'].splitlines())
            new_group_names = submitted_group_names.difference(existing_group_names)

            ntg = partial(TutorGroup, ophase=current_ophase, group_category=category)

            new_groups = (ntg(name=n) for n in new_group_names)

            session['gmc_duplicate_group_count'] = len(submitted_group_names) - len(new_group_names)
            session['gmc_new_group_count'] = len(new_group_names)

            TutorGroup.objects.bulk_create(new_groups)

            return super().form_valid(form)

class GroupMassCreateViewSuccess(StaffAppMixin, TemplateView):
    template_name = "staff/dashboard/group_mass_create_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.request.session

        context['ophase'] = session.pop('gmc_ophase', False)
        context['duplicate_group_count'] = session.pop('gmc_duplicate_group_count', None)
        context['new_group_count'] = session.pop('gmc_new_group_count', None)

        return context

class TutorPairingView(StaffAppMixin, FormView):
    permissions = ['staff.change_tutorgroup']
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
    permissions = ['staff.change_tutorgroup']
    template_name = "staff/dashboard/tutor_pairing_success.html"


class AttendanceEventIndexView(StaffAppMixin, ListView):
    permissions = ['staff.change_attendance']
    model = AttendanceEvent
    template_name = "staff/dashboard/events_overview.html"
    context_object_name = "events"


class AttendanceEventDetailView(StaffAppMixin, DetailView):
    permissions = ['staff.change_attendance']
    model = AttendanceEvent
    template_name = "staff/dashboard/event.html"
    context_object_name = "event"


class NametagCreation(StaffAppMixin, TemplateView):
    permissions = ['staff.change_tutorgroup']
    template_name = 'staff/dashboard/nametag_creation.html'

    def get_context_data(self, **kwargs):
        context = super(NametagCreation, self).get_context_data(**kwargs)
        persons = Person.objects.filter(Q(ophase=Ophase.current()), 
                Q(is_helper=True) | Q(is_tutor=True) | Q(is_orga=True)).prefetch_related('orga_jobs').order_by('name')
        context['staff'] = persons
        context['count_staff'] = persons.count()
        context['groupscount'] = TutorGroup.objects.filter(
            ophase=Ophase.current()).count()
        context['groups_without_picture'] = TutorGroup.objects.filter(
            ophase=Ophase.current(), picture='').count()
        context['form'] = TutorGroupSelect
        return context

    def post(self, request, *args, **kwargs):
        # should generate all nametags
        if request.POST['action'] == 'all_nametags':
            queryset = Person.objects.filter(Q(ophase=Ophase.current()),
                    Q(is_helper=True) | Q(is_tutor=True) | Q(is_orga=True)).prefetch_related('orga_jobs').order_by('name')
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
            return generate_nametag_response(request, [person], filename='schild.pdf')
        # generate group signs
        elif request.POST['action'] == 'group_signs':
            return generate_pdf_with_group_pictures_response(request,
                                                             TutorGroup.objects.filter(
                                                                 ophase=Ophase.current()),
                                                             'schilder.pdf',
                                                             'staff/reports/gruppenschilder.tex')
        elif request.POST['action'] == 'group_overview':
            # check whether a file was uploaded
            if 'roomscsv' not in request.FILES:
                messages.error(request, _(
                    'Du hast keine csv-Datei hochgeladen.'))
                return redirect('dashboard:staff:nametags')
            csv = TextIOWrapper(
                request.FILES['roomscsv'].file, encoding=request.encoding)
            csv_list = list(reader(csv))
            rooms = csv_list[2:]
            groups = TutorGroup.objects.filter(ophase=Ophase.current())
            grouprooms = zip(groups, rooms)
            timetable = [list(zip(csv_list[0], roomnumber, csv_list[1]))
                         for roomnumber in rooms]
            timetable_rooms = zip(groups, timetable)
            (group_overview_pdf, group_overview_log) = generate_pdf_with_group_pictures(request,
                                                                                        groups,
                                                                                        'staff/reports/gruppenuebersicht.tex',
                                                                                        {'grouprooms': grouprooms})
            (handout_pdf, handout_log) = generate_pdf_with_group_pictures(request,
                                                                          groups,
                                                                          'staff/reports/handzettel.tex',
                                                                          {'grouprooms': timetable_rooms})
            memoryfile = BytesIO()
            zipfile = ZipFile(memoryfile, 'w')
            if group_overview_pdf is not None:
                zipfile.writestr('group-overview.pdf', group_overview_pdf)
            else:
                zipfile.writestr('group-overview-log.txt',
                                 group_overview_log[0].decode('utf-8'))
            if handout_pdf is not None:
                zipfile.writestr('handout.pdf', handout_pdf)
            else:
                zipfile.writestr('handout-log.txt',
                                 handout_log[0].decode('utf-8'))
            zipfile.close()
            response = HttpResponse(content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=overview.zip'
            memoryfile.seek(0)
            response.write(memoryfile.read())
            return response
        elif request.POST['action'] == 'freshmen_nametags':
            if not 'roomscsv' in request.FILES:
                messages.error(request, _(
                    'Du hast keine Raum csv-Datei hochgeladen.'))
            if not 'freshmencsv' in request.FILES:
                messages.error(request, _(
                    'Du hast keine Erstsemester csv-Datei hochgeladen.'))
                freshmen = []
            else:
                freshmencsv = TextIOWrapper(
                    request.FILES['freshmencsv'].file, encoding=request.encoding)
                freshmen = list(reader(freshmencsv))[1:]
           # if len(messages.get_messages(request)) != 0:
           #     return redirect('dashboard:staff:nametags')
            roomscsv = TextIOWrapper(
                request.FILES['roomscsv'].file, encoding=request.encoding)
            rooms = list(reader(roomscsv))
            group_capacities = [int(room) for room in [room[0] for room in rooms][2:]] # skip header
            form = TutorGroupSelect(request.POST)
            form.is_valid()
            groups = form.cleaned_data.get('TutorGruppe')
            if len(groups) != len(group_capacities):
                messages.error(request, _(
                    'Es wurden nicht genauso viele Räume wie Gruppen angelegt'))
                return redirect('dashboard:staff:nametags')

            # Add empty entries to end freshmen list to create empty tags for groups not full already
            freshmen.extend([[" ", " "]] * (len(groups) * 5))

            groups_with_rooms = list(zip(groups, rooms[2:]))
            freshmen_group = list(zip(freshmen, cycle_bucket(groups_with_rooms, group_capacities)))
            # generate group assignement overview
            (assignement_pdf, assignement_log) = generate_nametags(
                [(f, g) for f, (g, r) in freshmen_group], template='staff/reports/gruppenzuweisung.tex')
            if not assignement_pdf:
                return render(request, "staff/reports/rendering-error.html", {"content": assignement_log[0].decode("utf-8")})

            # combine this with the freshmen_group-zip
            freshmen_tags = []
            for f, (g, r) in freshmen_group:
                timetable = list(zip(rooms[0], rooms[1], r[1:]))
                freshmen_tags.append([f, g, timetable])
            # Empty tags are created together with other tags already
            empty_tags = []
            """for i, group in enumerate(groups):
                for x in range(5):
                    empty_tags.append((group, timetable[i]))
                    """
            (nametags_pdf, nametag_log) = generate_pdf_with_group_pictures(request=request,
                                                                           groups=groups,
                                                                           template='staff/reports/namensschilder-ersties.tex',
                                                                           context={'freshmen': freshmen_tags,
                                                                                    'empty_tags': empty_tags})
            memoryfile = BytesIO()
            zipfile = ZipFile(memoryfile, 'w')
            if assignement_pdf is not None:
                zipfile.writestr('assignement-overview.pdf', assignement_pdf)
            else:
                zipfile.writestr('assignement-log.txt',
                                 assignement_log[0].decode('utf-8'))
            if nametags_pdf is not None:
                zipfile.writestr('nametags.pdf', nametags_pdf)
            else:
                zipfile.writestr('nametags-log.txt',
                                 nametag_log[0].decode('utf-8'))
            zipfile.close()
            response = HttpResponse(content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=freshmen.zip'
            memoryfile.seek(0)
            response.write(memoryfile.read())
            return response
        else:
            messages.error(request, _('Keine valide Aktion gewählt'))
            return redirect('dashboard:staff:nametags')


class GroupPictureAdd(StaffAppMixin, TemplateView):
    permissions = ['staff.change_tutorgroup']
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
        messages.info(request, _(
            'Bilder erfolgreich hochgeladen.'))
        return redirect('dashboard:staff:group_picture_add')
