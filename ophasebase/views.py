from django.views.generic import TemplateView

from ophasebase.models import Ophase
from staff.models import Settings as StaffSettings
from students.models import Settings as StudentsSettings
from workshops.models import Settings as WorkshopSettings


class LoginSelectView(TemplateView):
    template_name = "ophasebase/login-select.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()  #
        next_url = self.request.GET.get('next', None)
        if next_url is not None:
            context['next_url'] = "?next={}".format(next_url)
        return context


class LandingPageView(TemplateView):
    template_name = "ophasebase/landing_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        students_settings = StudentsSettings.instance()
        staff_settings = StaffSettings.instance()
        workshop_settings = WorkshopSettings.instance()

        current_ophase = Ophase.current()
        context['current_ophase'] = Ophase.current()

        context['student_registration_enabled'] = False
        context['any_staff_registration_enabled'] = False
        if current_ophase is not None:
            if students_settings is not None:
                context[
                    'student_registration_enabled'] = students_settings.student_registration_enabled
            if staff_settings is not None:
                context[
                    'any_staff_registration_enabled'] = staff_settings.any_registration_enabled()
            if workshop_settings is not None:
                context['any_staff_registration_enabled'] = context[
                                                                'any_staff_registration_enabled'] or workshop_settings.workshop_submission_enabled

        return context
