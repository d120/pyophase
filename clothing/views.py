from django.core.mail import EmailMessage
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.template import Context, loader
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView

from ophasebase.models import Ophase
from staff.models import Person

from .forms import OrderAskMailForm, OrderClothingFormSet
from .models import Order, Settings


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

        form_dict.get('1').save()

        email_address = self.get_cleaned_data_for_step("0")['email']
        person = Person.get_by_email_address_current(email_address)
        orders = '\n'.join(o.info() for o in Order.get_current(person=person))
        if orders == "":
            orders = _("Keine Bestellungen")

        email = EmailMessage()
        email.subject = _("Kleiderbestellung %(ophase)s") % {'ophase': str(Ophase.current())}
        email_template = loader.get_template('clothing/mail.txt')
        email_context = Context({
            'name': person.prename,
            'orders': orders,
            'editurl': self.request.build_absolute_uri(reverse('clothing:order_new'))
        })
        email.body = email_template.render(email_context)
        email.to = [email_address]
        email.reply_to = [Ophase.current().contact_email_address]
        email.send()

        return HttpResponseRedirect(reverse_lazy('clothing:order_success'))


class OrderClothingSuccessView(TemplateView):
    template_name = "clothing/order_success.html"
