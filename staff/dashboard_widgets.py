from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from dashboard.components import TemplateWidgetComponent
from ophasebase.models import Ophase

from .models import Person


class StaffCountWidget(TemplateWidgetComponent):
    permissions = ['staff.add_person']
    name = _('Ophasenpersonal')
    template_name = "staff/dashboard/widget_staff.html"
    link_target = reverse_lazy('dashboard:staff:index')

    def __init__(self):
        self.__current_ophase = Ophase.current()

    def get_context_data(self):
        context = super().get_context_data()

        context['ophase_title'] = _('Ophase')
        if self.__current_ophase is not None:
            staff = Person.objects.filter(ophase=self.__current_ophase)
            stats = staff.aggregate(num_tutor=Count('pk', filter=Q(is_tutor=True)),\
                num_orga=Count('pk', filter=Q(is_orga=True)),\
                num_helper=Count('pk', filter=Q(is_helper=True)))

            context['count_tutor'] = stats['num_tutor']
            context['count_orga'] = stats['num_orga']
            context['count_helper'] = stats['num_helper']
        return context

    def get_status(self):
        if self.__current_ophase is not None:
            Staff = Person.objects.filter(ophase=self.__current_ophase)
            if Staff.count() > 10:
                return "success"
            return "danger"
