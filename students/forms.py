from django import forms
from .models import Student


class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['prename', 'name', 'tutor_group', 'want_exam', 'want_newsletter', 'newsletters', 'email']
        widgets = {
            # use checkboxes for multipleChoice @see http://stackoverflow.com/a/16937145
            'newsletters': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super(StudentRegisterForm, self).__init__(*args, **kwargs)
