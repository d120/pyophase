from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView
from django.core.urlresolvers import reverse_lazy
from django.db import IntegrityError
from django.template import loader
from django.template.response import SimpleTemplateResponse

from ophasebase.models import Ophase, OrgaJob, HelperJob
from staff.models import Settings, GroupCategory
from staff.forms import PersonForm

class StaffAdd(CreateView):
    form_class = PersonForm
    template_name = 'staff/person_form.html'
    success_url = reverse_lazy('staff:registration_success')

    def get_context_data(self, **kwargs):
        current_ophase_qs = Ophase.objects.filter(is_active=True)
        settings_qs = Settings.objects.all()

        if (len(current_ophase_qs) == 1) and (len(settings_qs) == 1):
            current_ophase = current_ophase_qs[0]
            settings = settings_qs[0]

            vacancies = []
            if settings.tutor_registration_enabled:
                vacancies.append('Tutoren')
            if settings.orga_registration_enabled:
                vacancies.append('Organisatoren')
            if settings.helper_registration_enabled:
                vacancies.append('Helfer')
            vacancies_str = '.'.join(vacancies)
            vacancies_str = vacancies_str.replace('.', ', ', len(vacancies)-2)
            vacancies_str = vacancies_str.replace('.', ' und ')

            context = super(StaffAdd, self).get_context_data(**kwargs)
            context['ophase_title'] = current_ophase.__str__()
            context['ophase_duration'] = current_ophase.get_human_duration()
            context['any_registration_enabled'] = settings.tutor_registration_enabled or settings.orga_registration_enabled or settings.helper_registration_enabled
            context['tutor_registration_enabled'] = settings.tutor_registration_enabled
            context['orga_registration_enabled'] = settings.orga_registration_enabled
            context['helper_registration_enabled'] = settings.helper_registration_enabled
            context['staff_vacancies'] = vacancies_str
            return context
        else:
            context = super(StaffAdd, self).get_context_data(**kwargs)
            context['ophase_title'] = 'Ophase'
            context['any_registration_enabled'] = False
            return context

    def form_valid(self, form):
        try:
            return super(StaffAdd, self).form_valid(form)
        except IntegrityError:
            # this should happen when unique constraints fail
            template = loader.get_template("staff/already_registered.html")
            return SimpleTemplateResponse(template)

class StaffAddSuccess(TemplateView):
    template_name = 'staff/success.html'

class GenericJobList(ListView):
    """List all Jobs of a Model that do have a label field"""
    template_name = 'staff/job_list.html'

    def __init__(self):
        self.title = 'Aufgabenliste'

    def get_context_data(self, **kwargs):
        current_ophase_qs = Ophase.objects.filter(is_active=True)

        if len(current_ophase_qs) == 1:
            current_ophase = current_ophase_qs[0]

            context = super(GenericJobList, self).get_context_data(**kwargs)
            context['ophase_title'] = current_ophase.__str__()
            context['title'] = self.title
            return context

class GroupCategoryList(GenericJobList):
    """List all GroupCategorys"""
    model = GroupCategory

    def __init__(self):
        self.title = GroupCategory._meta.verbose_name_plural.title()

class OrgaJobList(GenericJobList):
    """List all OrgaJobs"""
    model = OrgaJob

    def __init__(self):
        self.title = OrgaJob._meta.verbose_name_plural.title()

class HelperJobList(GenericJobList):
    """List all HelperJobs"""
    model = HelperJob

    def __init__(self):
        self.title = HelperJob._meta.verbose_name_plural.title()
