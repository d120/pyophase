from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from dashboard.components import TemplateWidgetComponent
from ophasebase.models import Ophase

from .models import Order, Person


class ClothingOrderWidget(TemplateWidgetComponent):
    permissions = ['clothing.add_order']
    name = _('Kleidung')
    template_name = "clothing/dashboard/widget_orders.html"
    link_target = reverse_lazy('dashboard:clothing:order_overview')

    def get_context_data(self):
        context = super().get_context_data()

        current_ophase = Ophase.current()
        context['ophase_title'] = _('Ophase')
        if current_ophase is not None:
            context['ophase_title'] = str(current_ophase)

            staff = Person.get_current()
            context['count_eligible'] = sum(1 for s in staff.all() if s.eligible_for_clothing)

            orders = Order.get_current()
            context['count_orders'] = orders.count()
            context['count_orders_additional'] = orders.filter(additional=True).count()
            context['count_orders_free'] = context['count_orders'] - context['count_orders_additional']
        return context

    def get_status(self):
        return "info"
