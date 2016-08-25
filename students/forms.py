from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Student


class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['prename', 'name', 'tutor_group', 'want_exam', 'newsletters', 'email']
        widgets = {
            # use checkboxes for multipleChoice @see http://stackoverflow.com/a/16937145
            'newsletters': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        exam_enabled = kwargs.pop('exam_enabled', False)
        super().__init__(*args, **kwargs)

        if exam_enabled == False:
            del self.fields['want_exam']

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("newsletters").count() > 0 and cleaned_data.get("email") == "":
            self.add_error('email', ValidationError(_('Um Newsletter zu abonnieren muss eine E-Mail-Adresse angegeben werden.')))
