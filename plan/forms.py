from django import forms

from .models import TimeSlot


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['name', 'slottype', 'begin', 'end', 'category', 'relevant_for', 'attendance_required', 'public']
        widgets = {
            # use checkboxes for multipleChoice @see http://stackoverflow.com/a/16937145
            'category': forms.CheckboxSelectMultiple,
            # TODO Use DateTimePicker
        }
