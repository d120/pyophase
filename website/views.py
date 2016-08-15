from django.views.generic import TemplateView
from ophasebase.models import Ophase
from students.models import Settings as StudentsSettings
from staff.models import Settings as StaffSettings
from workshops.models import Settings as WorkshopSettings
from website.models import Settings as WebsiteSettings


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

        if current_ophase is not None and students_settings is not None:
            context['student_registration_enabled'] = students_settings.student_registration_enabled
        else:
            context['student_registration_enabled'] = False

        context['any_staff_registration_enabled'] = False
        if current_ophase is not None and staff_settings is not None:
            context['any_staff_registration_enabled'] = staff_settings.tutor_registration_enabled or staff_settings.orga_registration_enabled or staff_settings.helper_registration_enabled
        if current_ophase is not None and workshop_settings is not None:
            context['any_staff_registration_enabled'] = context['any_staff_registration_enabled'] or workshop_settings.workshop_submission_enabled

        return context


class WebsiteView(TemplateView):
    """Extends the django TemplateView by adding the Ophase.current() object
    to the context data as current_ophase"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_ophase'] = Ophase.current()
        return context

class BachelorView(WebsiteView):
    template_name = "website/bachelor.html"

class MasterDeView(WebsiteView):
    template_name = "website/master-de.html"

class MasterDssView(WebsiteView):
    template_name = "website/master-dss.html"

class HelfenView(WebsiteView):
    template_name = "website/helfen.html"

