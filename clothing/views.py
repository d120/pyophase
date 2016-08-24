from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _

from formtools.wizard.views import SessionWizardView

from clothing.forms import OrderAskMailForm, OrderClothingFormSet
from clothing.models import Settings, Order
from staff.models import Person
from ophasebase.models import Ophase


class OrderClothingView(SessionWizardView):
    form_list = [OrderAskMailForm, OrderClothingFormSet]
    template_name = "clothing/order.html"

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        settings = Settings.instance()
        if settings is not None:
            context['clothing_ordering_enabled'] = settings.clothing_ordering_enabled
        else:
            context['clothing_ordering_enabled'] = False
        return context

    def get_form_kwargs(self, step=None):
        if step == "1":
            email = self.get_cleaned_data_for_step("0")['email']
            person = Person.get_by_email_address_current(email)
            return {'form_kwargs': {'person': person}}
        else:
            return super().get_form_kwargs(step)

    def done(self, form_list, form_dict, **kwargs):
        settings = Settings.instance()
        if settings is None or not settings.clothing_ordering_enabled:
            return HttpResponseForbidden()

        for form in form_dict.get('1'):
            if 'type' in form.cleaned_data:
                form.save()

        email_addr = self.get_cleaned_data_for_step("0")['email']
        person = Person.get_by_email_address_current(email_addr)
        orders = '\n'.join(o.info() for o in Order.get_current(person=person))

        email = EmailMessage()
        email.subject = _("Kleiderbestellung %(ophase)s") % {'ophase': str(Ophase.current())}
        email.body = _("""Hallo %(name)s,

deine Kleiderbestellung für die Ophase wurde aktualisiert.
Aktuell ist folgendes für dich vermerkt:

%(orders)s

Liebe Grüße
die Ophasenleitung
""") % {'name': person.prename, 'orders': orders}
        email.to = [email_addr]
        email.reply_to = ["ophase-leitung@fachschaft.informatik.tu-darmstadt.de"]
        email.send()

        return HttpResponseRedirect(reverse_lazy('clothing:order_success'))


class OrderClothingSuccessView(TemplateView):
    template_name = "clothing/order_success.html"
