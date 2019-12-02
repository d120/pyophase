from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.http import HttpResponseForbidden
from django.template import loader
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView

from ophasebase.models import Ophase, OphaseCategory
from staff.forms import PersonForm
from staff.models import HelperJob, OrgaJob, Settings, Person


class StaffAdd(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('tuid_login')
    form_class = PersonForm
    template_name = 'staff/person_form.html'
    success_url = reverse_lazy('staff:registration_success')

    def dispatch(self, request, *args, **kwargs):
        if Person.get_by_user(request.user) is not None:
            return self.already_registerd(request)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def already_registerd(self, request):
        template = loader.get_template("staff/already_registered.html")
        return TemplateResponse(request, template)

    def get_initial(self):
        user = self.request.user
        initial = super().get_initial()
        initial['prename'] = user.first_name
        initial['name'] = user.last_name
        initial['email'] = user.email
        return initial

    def get_context_data(self, **kwargs):
        current_ophase = Ophase.current()
        settings = Settings.instance()
        context = super().get_context_data(**kwargs)

        if current_ophase is not None and settings is not None:
            context['ophase_title'] = str(current_ophase)
            context['ophase_duration'] = current_ophase.get_human_duration()
            context['any_registration_enabled'] = settings.any_registration_enabled()
            context['tutor_registration_enabled'] = settings.tutor_registration_enabled
            context['orga_registration_enabled'] = settings.orga_registration_enabled
            context['helper_registration_enabled'] = settings.helper_registration_enabled
            context['staff_vacancies'] = StaffAdd.vacancies_string_generator()
        else:
            context['ophase_title'] = 'Ophase'
            context['any_registration_enabled'] = False

        return context

    @staticmethod
    def vacancies_string_generator():
        """
        Generates a string which lists all job types in natural language enumeration
        :return: the generated string
        """
        settings = Settings.instance()

        job_types = ((settings.tutor_registration_enabled, _('Tutoren')),
                     (settings.orga_jobs_enabled, _('Organisatoren')),
                     (settings.helper_jobs_enabled, _('Helfer')))

        vacancies = [name for enabled, name in job_types if enabled]

        if len(vacancies) == 0:
            vacancies_str = ''
        elif len(vacancies) == 1:
            vacancies_str = vacancies[-1]
        else:
            vacancies_str = ', '.join(vacancies[:-1])
            vacancies_str = ' {} '.format(_('und')).join((vacancies_str, vacancies[-1]))
        return vacancies_str

    def form_valid(self, form):
        settings = Settings.instance()
        if settings is None or not settings.any_registration_enabled():
            return HttpResponseForbidden()

        try:
            if form.instance.tutor_experience is None:
                form.instance.tutor_experience = 0
            super_return = super().form_valid(form)
        except IntegrityError:
            # this should happen when unique constraints fail
            return self.already_registerd(self.request)

        # the enumeration symbol
        esym = '\n * '

        form_list = []

        for field in form.fields:
            label = form[field].label
            # remove html from label
            label = label.split('<', 1)[0].strip()

            content = form.cleaned_data[field]
            #Remove all fields that are not set
            if content:
                #format Many to Many and foreign key
                if isinstance(content, QuerySet):
                    content = esym + esym.join(str(c) for c in content)
                #format True as normal language
                if isinstance(content, bool):
                    content = _('Ja')

                form_list.append('{}: {}'.format(label, content))

        form_content = '\n'.join(form_list)

        values = {'ophase_title': str(Ophase.current()),
                 'user_prename': form.cleaned_data['prename'],
                 'user_name':  form.cleaned_data['name'],
                 'user_email': form.cleaned_data['email'],
                 'email_changedata': Ophase.current().contact_email_address,
                 'form_content': form_content,
                 }

        email = EmailMessage()
        email.subject = _('{ophase_title} Registrierung').format(**values)
        email.to = ['{user_prename} {user_name} <{user_email}>'.format(**values)]
        email_template = loader.get_template('staff/mail/register.txt')
        email.body = email_template.render(values)
        email.reply_to = [Ophase.current().contact_email_address]
        email.send()

        return super_return

class StaffAddSuccess(TemplateView):
    template_name = 'staff/success.html'

class GenericJobList(ListView):
    """List all Jobs of a Model that do have a label field"""
    template_name = 'staff/job_list.html'

    def __init__(self):
        self.title = _('Aufgabenliste')

    def get_context_data(self, **kwargs):
        current_ophase = Ophase.current()
        if current_ophase is not None:
            context = super().get_context_data(**kwargs)
            context['ophase_title'] = str(current_ophase)
            context['title'] = self.title
            return context

class GroupCategoryList(GenericJobList):
    """List all OphaseCategorie"""
    model = OphaseCategory

    def __init__(self):
        super().__init__()
        self.title = _("Tutorjobs")

class OrgaJobList(GenericJobList):
    """List all OrgaJobs"""
    model = OrgaJob

    def __init__(self):
        super().__init__()
        self.title = OrgaJob._meta.verbose_name_plural

class HelperJobList(GenericJobList):
    """List all HelperJobs"""
    model = HelperJob

    def __init__(self):
        super().__init__()
        self.title = HelperJob._meta.verbose_name_plural
