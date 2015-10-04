from django import forms
from django.core.exceptions import ValidationError
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
        super(StudentRegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(StudentRegisterForm, self).clean()

        if cleaned_data.get("newsletters").count() > 0 and cleaned_data.get("email") == "":
            self.add_error('email', ValidationError('Um Newsletter zu abonnieren muss eine E-Mail-Adresse angegeben werden.'))
