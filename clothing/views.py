from django.core.mail import EmailMessage
from django.http import HttpResponseForbidden
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from dashboard.views import PersonalDashboardMixin
from ophasebase.models import Ophase
from clothing.forms import OrderClothingForm
from clothing.models import Order, Settings


class ClothingPersonalOverview(PersonalDashboardMixin, ListView):
    template_name = "clothing/personal_clothing_overview.html"
    model = Order
    context_object_name = "orders"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.TUIDUser.person_set.first()
        return qs.filter(person=user)


class ClothingOrderEnabledMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings = Settings.instance()
        if settings is not None:
            context['clothing_order_enabled'] = settings.clothing_ordering_enabled
        return context


class ClothingOrderBaseView(ClothingOrderEnabledMixin, PersonalDashboardMixin):
    template_name = "clothing/order.html"
    model = Order
    form_class = OrderClothingForm
    success_url = reverse_lazy("clothing:order_success")

    def form_valid(self, form):
        settings = Settings.instance()
        if settings is None or not settings.clothing_ordering_enabled:
            return HttpResponseForbidden()

        super_return = super().form_valid(form)

        person = form.person

        orders = '\n'.join(o.info() for o in Order.get_current(person=person))
        if orders == "":
            orders = _("Keine Bestellungen")

        email = EmailMessage()
        email.subject = _("Kleiderbestellung %(ophase)s") % {'ophase': str(Ophase.current())}
        email_template = loader.get_template('clothing/mail/order.txt')
        email.body = email_template.render({
            'name': person.prename,
            'orders': orders,
            'editurl': self.request.build_absolute_uri(reverse('clothing:overview'))
        })
        email.to = [person.email]
        email.reply_to = [Ophase.current().contact_email_address]
        email.send()

        return super_return


class ClothingOrderView(ClothingOrderBaseView, CreateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'instance' not in kwargs or kwargs['instance'] is None:
            kwargs['instance'] = Order()
            tuid = self.request.TUIDUser
            if tuid is not None:
                kwargs['instance'].person = tuid.person_set.first()
                kwargs['person'] = tuid.person_set.first()
        return kwargs


class ClothingOrderEditView(ClothingOrderBaseView, UpdateView):
    pass


class ClothingOrderDeleteView(ClothingOrderEnabledMixin, PersonalDashboardMixin, DeleteView):
    template_name = "clothing/order_delete.html"
    model = Order
    success_url = reverse_lazy("clothing:order_success")
    context_object_name = "order"


class OrderClothingSuccessView(PersonalDashboardMixin, TemplateView):
    template_name = "clothing/order_success.html"
