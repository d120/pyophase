from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from dashboard.components import TemplateWidgetComponent
from ophasebase.models import Ophase

from .models import Person


class StaffCountWidget(TemplateWidgetComponent):
    permissions = ['staff.add_person']
    name = _('Ophasenpersonal')
    template_name = "staff/dashboard/widget_staff.html"
    link_target = reverse_lazy('dashboard:staff:index')

    def get_context_data(self):
        context = super().get_context_data()

        current_ophase = Ophase.current()
        context['ophase_title'] = _('Ophase')
        if current_ophase is not None:
            context['ophase_title'] = str(current_ophase)

            Staff = Person.objects.filter(ophase=current_ophase)
            context['count_staff'] = Staff.count()
            context['count_tutor'] = Staff.filter(is_tutor=True).count()
            context['count_orga'] = Staff.filter(is_orga=True).count()
            context['count_helper'] = Staff.filter(is_helper=True).count()
        return context

    def get_status(self):
        current_ophase = Ophase.current()
        if current_ophase is not None:
            Staff = Person.objects.filter(ophase=current_ophase)
            if Staff.count() > 10:
                return "success"
            return "danger"
