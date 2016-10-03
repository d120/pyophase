from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ophasebase.models import Ophase
from staff.models import Settings as StaffSettings
from students.models import Settings as StudentsSettings
from workshops.models import Settings as WorkshopSettings

from .models import Schedule, Settings as WebsiteSettings, OInforz


class HomepageView(TemplateView):
    template_name = "website/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        students_settings = StudentsSettings.instance()
        staff_settings = StaffSettings.instance()
        workshop_settings = WorkshopSettings.instance()
        website_settings = WebsiteSettings.instance()

        current_ophase = Ophase.current()
        context['current_ophase'] = current_ophase
        context['website_settings'] = website_settings

        context['student_registration_enabled'] = False
        context['any_staff_registration_enabled'] = False
        if current_ophase is not None:
            if students_settings is not None:
                context['student_registration_enabled'] = students_settings.student_registration_enabled
            if staff_settings is not None:
                context['any_staff_registration_enabled'] = staff_settings.any_registration_enabled()
            if workshop_settings is not None:
                context['any_staff_registration_enabled'] = context['any_staff_registration_enabled'] or workshop_settings.workshop_submission_enabled

        return context


class WebsiteView(TemplateView):
    """Extends the django TemplateView by adding the Ophase.current() object
    to the context data as current_ophase"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_ophase = Ophase.current()
        website_settings = WebsiteSettings.instance()
        context['current_ophase'] = current_ophase
        context['ophase_title'] = str(current_ophase)
        context['website_settings'] = website_settings
        context['ophase_duration'] = current_ophase.get_human_duration()
        return context


class ScheduleView(WebsiteView):
    """Extends the django TemplateView by adding the Ophase.current() object
    to the context data as current_ophase"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule'] = get_object_or_404(Schedule, degree=self.kwargs['degree'])
        return context

    def get_template_names(self):
        degree = self.kwargs['degree']

        if degree == 'BSC':
            return 'website/bachelor.html'
        elif degree == 'MSC':
            return 'website/master-de.html'
        elif degree == 'DSS':
            return 'website/master-dss.html'
        elif degree == 'JBA':
            return 'website/jba.html'
        elif degree == 'EDU':
            return 'website/lehramt.html'


class HelfenView(WebsiteView):
    template_name = "website/helfen.html"


class OInforzView(WebsiteView):
    template_name = "website/oinforz.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['oinforze'] = OInforz.objects.all()
        return context