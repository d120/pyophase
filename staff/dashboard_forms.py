from django import forms

from .models import GroupCategory

class GroupMassCreateForm(forms.Form):
    category_choices = [(gc.id, str(gc)) for gc in GroupCategory.objects.all()]
    category = forms.ChoiceField(label="Gruppenkategorie", choices=category_choices)
    group_names = forms.CharField(label="Gruppennamen", help_text="Einen Gruppennamen pro Zeile eintragen.", widget=forms.Textarea)

    def clean_group_names(self):
        # remove unnecessary whitespace and duplicates
        data = self.cleaned_data['group_names']
        return '\n'.join(list(set([line.strip() for line in data.splitlines() if line.strip()])))
