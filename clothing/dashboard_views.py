from django.db import models
from django.utils.translation import ugettext as _
from django.views.generic import ListView

from clothing.models import Order
from dashboard.components import DashboardAppMixin
from staff.models import Person


class ClothingAppMixin(DashboardAppMixin):
    app_name_verbose = _('Kleidung')
    app_name = 'clothing'
    permissions = ['clothing.add_order']

    @property
    def sidebar_links(self):
        return [
            (_('Übersicht'), self.prefix_reverse_lazy('order_overview')),
            (_('Grundbestellung'), self.prefix_reverse_lazy('order_free')),
        ]


class OrderOverView(ClothingAppMixin, ListView):
    model = Order
    context_object_name = "orders"
    template_name = "clothing/dashboard/orders_overview.html"

    def get_queryset(self):
        return Order.get_current()


class FreeClothingView(ClothingAppMixin, ListView):
    model = Person
    template_name = "clothing/dashboard/orders_person_free.html"
    context_object_name = "persons"

    def get_queryset(self):
        return Person.get_current()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['persons'] = context['persons'].annotate(
            num_free_orders=models.Sum(models.Case(
                models.When(order__additional=False, then=1),
                default=0,
                output_field=models.IntegerField()
            ))
        )
        return context
