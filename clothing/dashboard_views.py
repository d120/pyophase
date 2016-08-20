from django.utils.translation import ugettext as _
from django.views.generic import ListView

from clothing.models import Order
from dashboard.components import DashboardAppMixin
from ophasebase.models import Ophase


class ClothingAppMixin(DashboardAppMixin):
    app_name_verbose = _('Kleidung')
    app_name = 'clothing'
    permissions = ['clothing.add_order']

    @property
    def sidebar_links(self):
        return [
            (_('Übersicht'), self.prefix_reverse_lazy('order_overview')),
        ]


class OrderOverView(ClothingAppMixin, ListView):
    model = Order
    context_object_name = "orders"
    template_name = "clothing/dashboard/orders_overview.html"

    def get_queryset(self):
        return Order.objects.filter(person__ophase=Ophase.current())
