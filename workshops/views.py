from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseForbidden

from ophasebase.models import Ophase
from workshops.models import Workshop, Settings
from workshops.forms import WorkshopSubmissionForm


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
        email.body = _("""Hallo %(name)s,

vielen Dank, dass du den Workshop "%(title)s" in der kommenden %(ophase)s anbieten möchtest.
Diese E-Mail dient hauptsächlich dazu, deine Eintragung zu bestätigen.
Der Workshoporga wird sich zu gegebener Zeit mit dir in Verbindung setzen.
Wenn sich etwas ändern sollte, antworte einfach auf diese E-Mail.

Hier nochmal die von dir eingetragenen Daten:

%(form_content)s

Liebe Grüße
das Orga-Team
""") % {'name': form.cleaned_data['tutor_name'], 'title': form.cleaned_data['title'], 'ophase': context['ophase_title'], 'form_content': form_content}
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
