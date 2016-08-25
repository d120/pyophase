from django.utils.translation import ugettext_lazy as _

from dashboard.components import TemplateWidgetComponent
from ophasebase.models import Ophase

from .models import Workshop


class WorkshopCountWidget(TemplateWidgetComponent):
    name = _('Workshops')
    template_name = "workshops/dashboard/widget_workshops.html"
    status = 'info'

    def get_context_data(self):
        context = super().get_context_data()
        current_ophase = Ophase.current()
        if current_ophase is not None:
            workshops = Workshop.get_current()
            context['num_workshops'] = workshops.count()
            context['filled_slots'] = sum(w.how_often for w in workshops)
            context['num_workshop_tutors'] = len(set(w.tutor_mail for w in workshops))
        return context
