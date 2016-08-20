from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from clothing.models import Order
from staff.models import Person


class OrderClothingForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['email', 'type', 'size', 'color', 'additional']
        exclude = ['person']

    email = forms.EmailField(label=_('E-Mail-Adresse (bei der Registrierung angegeben)'))

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        person = Person.get_by_email_address_current(email)

        if person is None:
            self.add_error('email', ValidationError(
                _('Die E-Mail-Adresse gehört nicht zu einer registrierten Person.')))
        elif not person.eligible_for_clothing and not cleaned_data.get("additional"):
            self.add_error('additional', ValidationError(
                _('Du bist nicht berechtigt, kostenfrei Kleidungsstücke zu bestellen. Du kannst aber zusäztliche Kleidungsstücke bestellen, die du dann selbst bezahlen musst.')))
        elif not cleaned_data.get("additional") and Order.get_current().filter(person=person, additional=False).count() > 0:
            self.add_error('additional', ValidationError(
                _('Du hast bereits ein kostenloses Kleidungsstück bestellt. Du kannst aber zusäztliche Kleidungsstücke bestellen, die du dann selbst bezahlen musst.')))
        else:
            self.instance.person = person
