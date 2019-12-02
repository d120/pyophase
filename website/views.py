from django.http.response import Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from ophasebase.models import Ophase, OphaseCategory, OphaseActiveCategory
from staff.models import Settings as StaffSettings
from students.models import Settings as StudentsSettings
from workshops.models import Settings as WorkshopSettings
from django.utils.translation import gettext as _

from .models import Settings as WebsiteSettings, OInforz


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


class WebsiteMixin():
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


class CategoryDetailView(WebsiteMixin, DetailView):
    """Extends the django TemplateView by adding the Ophase.current() object
    to the context data as current_ophase"""

    model = OphaseCategory
    context_object_name = 'category'

    def get_template_names(self):
        template_name = "website/detail/{}.html".format(self.object.slug)
        try:
            get_template(template_name)
            return template_name
        except TemplateDoesNotExist:
            raise Http404(_('Keine Detailinformationen gefunden.'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(OphaseActiveCategory, ophase=Ophase.current(), category=self.object)
        context['ophase_category_duration'] = category.get_human_duration()
        return context


class HelperView(WebsiteMixin, TemplateView):
    template_name = "website/helfen.html"


class OInforzView(WebsiteMixin, TemplateView):
    template_name = "website/oinforz.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['oinforze'] = OInforz.objects.all()
        return context
