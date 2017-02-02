from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.http import HttpResponseForbidden
from django.template import loader
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView

from ophasebase.models import Ophase, OphaseCategory
from staff.forms import PersonForm
from staff.models import HelperJob, OrgaJob, Settings


class StaffAdd(CreateView):
    form_class = PersonForm
    template_name = 'staff/person_form.html'
    success_url = reverse_lazy('staff:registration_success')

    def get_context_data(self, **kwargs):
        current_ophase = Ophase.current()
        settings = Settings.instance()

        if current_ophase is not None and settings is not None:
            vacancies = []
            if settings.tutor_registration_enabled:
                vacancies.append(_('Tutoren'))
            if settings.orga_registration_enabled:
                vacancies.append(_('Organisatoren'))
            if settings.helper_registration_enabled:
                vacancies.append(_('Helfer'))
            vacancies_str = '.'.join(vacancies)
            vacancies_str = vacancies_str.replace('.', ', ', len(vacancies)-2)
            vacancies_str = vacancies_str.replace('.', ' %s '% _('und'))

            context = super().get_context_data(**kwargs)
            context['ophase_title'] = str(current_ophase)
            context['ophase_duration'] = current_ophase.get_human_duration()
            context['any_registration_enabled'] = settings.any_registration_enabled()
            context['tutor_registration_enabled'] = settings.tutor_registration_enabled
            context['orga_registration_enabled'] = settings.orga_registration_enabled
            context['helper_registration_enabled'] = settings.helper_registration_enabled
            context['staff_vacancies'] = vacancies_str
            return context
        else:
            context = super().get_context_data(**kwargs)
            context['ophase_title'] = 'Ophase'
            context['any_registration_enabled'] = False
            return context

    def form_valid(self, form):
        settings = Settings.instance()
        if settings is None or not settings.any_registration_enabled():
            return HttpResponseForbidden()

        try:
            super_return = super().form_valid(form)
        except IntegrityError:
            # this should happen when unique constraints fail
            template = loader.get_template("staff/already_registered.html")
            return TemplateResponse(self.request, template)

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
    """List all GroupCategorys"""
    model = OphaseCategory

    def __init__(self):
        super().__init__()
        self.title = OphaseCategory._meta.verbose_name_plural

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
