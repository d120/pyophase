from django import forms
from django.utils.translation import ugettext as _

from .models import GroupCategory, Person, TutorGroup
from ophasebase.models import Ophase


class GroupMassCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(GroupMassCreateForm, self).__init__(*args, **kwargs)
        category_choices = [(gc.id, str(gc)) for gc in GroupCategory.objects.all()]
        self.fields['category'] = forms.ChoiceField(label=_('Gruppenkategorie'), choices=category_choices)
        self.fields['group_names'] = forms.CharField(label=_('Gruppennamen'), help_text=_('Einen Gruppennamen pro Zeile eintragen.'), widget=forms.Textarea)

    def clean_group_names(self):
        # remove unnecessary whitespace and duplicates
        data = self.cleaned_data['group_names']
        return '\n'.join(list(set([line.strip() for line in data.splitlines() if line.strip()])))


class TutorPairingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TutorPairingForm, self).__init__(*args, **kwargs)
        current_ophase = Ophase.current()

        group_categories = GroupCategory.objects.all()
        group_category_choices = [(gc.id, str(gc)) for gc in group_categories]
        self.fields['category'] = forms.ChoiceField(label=_('Gruppenkategorie'), choices=group_category_choices)

        tutor_groups = TutorGroup.objects.filter(ophase=current_ophase)
        tutors = Person.objects.filter(ophase=current_ophase, is_tutor=True)

        for gc in group_categories:
            category_css_class = str(gc).lower().replace(' ', '-')
            css_classes = ['tutor-select', category_css_class]
            tutor_choices_per_category = [(t.id, str(t)) for t in tutors.filter(tutor_for=gc)]
            for group in tutor_groups.filter(group_category=gc):
                current_tutors_per_group = [g.id for g in group.tutors.all()]
                self.fields["group-" + str(group.id)] = forms.MultipleChoiceField(label=str(group), choices=tutor_choices_per_category, initial=current_tutors_per_group, required=False)
                self.fields["group-" + str(group.id)].widget.attrs = {'class': ' '.join(css_classes)}
