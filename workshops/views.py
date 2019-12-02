from django.core.mail import EmailMessage
from django.http import HttpResponseForbidden
from django.template import loader
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from dashboard.components import DashboardAppMixin
from ophasebase.models import Ophase
from workshops.forms import WorkshopSubmissionForm
from workshops.models import Settings, Workshop


class WorkshopAppMixin(DashboardAppMixin):
    app_name_verbose = _('Workshops')
    app_name = 'workshops'
    permissions = ['workshops.add_workshop']

    @property
    def sidebar_links(self):
        return [
            (_('Workshops'), self.prefix_admin_reverse_lazy('workshop', 'changelist')),
            (_('Slots einrichten'), self.prefix_admin_reverse_lazy('workshopslot', 'changelist')),
            (_('Konfiguration'), self.prefix_admin_reverse_lazy('settings', 'changelist')),
        ]


class WorkshopCreate(CreateView):
    model = Workshop
    success_url = reverse_lazy('workshops:create_success')
    form_class = WorkshopSubmissionForm

    def get_context_data(self, **kwargs):
        current_ophase = Ophase.current()
        settings = Settings.instance()
        context = super().get_context_data(**kwargs)
        if current_ophase is not None and settings is not None:
            context['ophase_title'] = str(current_ophase)
            context['workshop_submission_enabled'] = settings.workshop_submission_enabled
            context['orga_email'] = settings.orga_email
        else:
            context['ophase_title'] = 'Ophase'
            context['workshop_submission_enabled'] = False
            context['orga_email'] = ""
        context['other_workshops'] = Workshop.get_current().order_by('title')
        return context

    def form_valid(self, form):
        settings = Settings.instance()
        if settings is None or not settings.workshop_submission_enabled:
            return HttpResponseForbidden()

        context = self.get_context_data()
        form_content = ''
        for field in form.fields:
            form_content += "{}: {}\n".format(form[field].label, form.cleaned_data[field])

        email = EmailMessage()
        email.subject = _("Workshop in der %(ophase)s") % {'ophase': context['ophase_title']}
        email_template = loader.get_template('workshops/mail/submission.txt')
        email.body = email_template.render({
            'name': form.cleaned_data['tutor_name'],
            'title': form.cleaned_data['title'],
            'ophase': context['ophase_title'],
            'form_content': form_content
        })
        email.to = [form.cleaned_data['tutor_mail']]
        if settings is not None:
            email.reply_to = [settings.orga_email]
        email.send()

        return super().form_valid(form)


class WorkshopCreateSuccess(TemplateView):
    template_name = 'workshops/create_success.html'

    def get_context_data(self, **kwargs):
        current_ophase = Ophase.current()
        settings = Settings.instance()
        context = super().get_context_data(**kwargs)
        if current_ophase is not None and settings is not None:
            context['ophase_title'] = str(current_ophase)
            context['orga_email'] = settings.orga_email
        else:
            context['ophase_title'] = 'Ophase'
        return context
