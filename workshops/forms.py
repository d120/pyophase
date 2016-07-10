from django import forms

from workshops.models import Workshop, WorkshopSlot

class WorkshopSubmissionForm(forms.ModelForm):
    class Meta:
        model = Workshop
        exclude = ['ophase']
        widgets = {
            'how_often': forms.NumberInput(attrs={'min': '1', 'max': str(WorkshopSlot.get_current().count()), 'step': '1', 'value': '1'}),
            'max_participants': forms.NumberInput(attrs={'value': '0'}),
        }
