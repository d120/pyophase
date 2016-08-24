from collections import OrderedDict

from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from django.views.generic import TemplateView

from clothing.models import Order, Type, Color, Size
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
            (_('Aggregierte Bestellungen'), self.prefix_reverse_lazy('order_aggregated')),
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


class OrderAggregatedView(ClothingAppMixin, TemplateView):
    template_name = "clothing/dashboard/orders_aggregated.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        types = Type.objects.all()
        colors = Color.objects.all()
        sizes = Size.objects.all()

        context['orders'] = OrderedDict()
        for additional_type, additional_name in [(False, _('Kostenlos')), (True, _('Zusätzlich'))]:
            # Create bins
            context['orders'][additional_name] = OrderedDict()
            for color in colors:
                context['orders'][additional_name][color.name] = OrderedDict()
                for type in types:
                    context['orders'][additional_name][color.name][type.name] = OrderedDict()
                    for size in sizes:
                        context['orders'][additional_name][color.name][type.name][size.size] = 0

        # Store orders
        orders = Order.objects.values('additional', 'type__name','size__size','color__name')
        orders = orders.annotate(count=Count('pk'))
        for order in orders:
            additional_name = _('Kostenlos')
            if order['additional'] == True:
                additional_name = _('Zusätzlich')

            c = order['color__name']
            t = order['type__name']
            s = order['size__size']
            context['orders'][additional_name][c][t][s] = order['count']

        return context
