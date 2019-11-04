from django import forms

from .models import Workshop, WorkshopSlot


class WorkshopSubmissionForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Workshop
        exclude = ['ophase', 'assigned']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['how_often'].widget = forms.NumberInput(attrs={'min': '1', 'max': str(WorkshopSlot.get_current().count()), 'step': '1', 'value': '1'})
        self.fields['max_participants'].widget = forms.NumberInput(attrs={'value': '0'})
