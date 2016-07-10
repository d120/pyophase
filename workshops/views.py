from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

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
        else:
            context['ophase_title'] = 'Ophase'
            context['workshop_submission_enabled'] = False
        return context


class WorkshopCreateSuccess(TemplateView):
    template_name = 'workshops/create_success.html'

    def get_context_data(self, **kwargs):
        current_ophase = Ophase.current()
        context = super().get_context_data(**kwargs)
        if current_ophase is not None:
            context['ophase_title'] = str(current_ophase)
        else:
            context['ophase_title'] = 'Ophase'
        return context
