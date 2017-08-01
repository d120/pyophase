from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Order


class OrderClothingForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['type', 'size', 'color', 'additional']

    def __init__(self, *args, **kwargs):
        if "person" in kwargs:
            self.person = kwargs.pop('person')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.instance.person is not None:
            self.person = self.instance.person

        cleaned_data = super().clean()
        if cleaned_data.get('type', False) and cleaned_data['type'].additional_only and not cleaned_data['additional']:
            self.add_error('additional', ValidationError(_('Dieses Kleidungsstück ist nur als selbst bezahltes Kleidungsstück bestellbar.')))
        elif not self.person.eligible_for_clothing and not cleaned_data['additional']:
            self.add_error('additional', ValidationError(_('Nur Tutoren und Orgas bekommen ein kostenloses Kleidungsstück. Du kannst aber zusätzlich Kleidungsstücke bestellen, die du selbst bezahlst.')))
        elif not cleaned_data['additional'] and self.person.order_set.filter(additional=False).exclude(id=self.instance.id).count() >= 1:
            self.add_error('additional', ValidationError(_('Du kannst nur ein kostenloses Kleidungsstück bestellen. Du kannst aber zusätzlich Kleidungsstücke bestellen, die du selbst bezahlst.')))
        else:
            self.instance.person = self.person
