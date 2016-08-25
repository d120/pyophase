from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from staff.models import Person

from .models import Order


class OrderAskMailForm(forms.Form):
    email = forms.EmailField(label=_('E-Mail-Adresse wie bei der Registrierung angegeben'))

    def clean(self):
        cleaned_data = super().clean()
        if any(self.errors):
            return
        person = Person.get_by_email_address_current(cleaned_data["email"])
        if person is None:
            self.add_error('email', ValidationError(_('Die E-Mail-Adresse gehört nicht zu einer registrierten Person.')))


class OrderClothingForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['type', 'size', 'color', 'additional']

    def __init__(self, *args, **kwargs):
        self.person = kwargs.pop('person')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['type'].additional_only and not cleaned_data['additional']:
            self.add_error('additional', ValidationError(_('Dieses Kleidungsstück ist nur als selbst bezahltes Kleidungsstück bestellbar.')))
        elif not self.person.eligible_for_clothing and not cleaned_data['additional']:
            self.add_error('additional', ValidationError(_('Nur Tutoren und Orgas bekommen ein kostenloses Kleidungsstück. Du kannst aber zusätzlich Kleidungsstücke bestellen, die du selbst bezahlst.')))
        else:
            self.instance.person = self.person


class BaseOrderClothingFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Order.get_current(person=kwargs['form_kwargs']['person'])

    def clean(self):
        if any(self.errors):
            return
        num_non_additional = sum(1 for form in self.forms if 'type' in form.cleaned_data and not form.cleaned_data['additional'])
        if num_non_additional > 1:
            raise ValidationError(_('Du kannst nur ein kostenloses Kleidungsstück bestellen. Du kannst aber zusätzlich Kleidungsstücke bestellen, die du selbst bezahlst.'))


OrderClothingFormSet = forms.modelformset_factory(Order, form=OrderClothingForm, formset=BaseOrderClothingFormSet, min_num=1, extra=2, can_delete=True)
