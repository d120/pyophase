from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from clothing.forms import OrderClothingForm
from clothing.models import Order


class OrderClothingView(CreateView):
    model = Order
    form_class = OrderClothingForm
    template_name = "clothing/order.html"
    success_url = reverse_lazy('clothing:order_success')


class OrderClothingSuccessView(TemplateView):
    template_name = "clothing/order_success.html"
