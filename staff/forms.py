# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError

from staff.models import Person, Settings
from ophasebase.models import HelperJob, OrgaJob

class PersonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)

        # Only display jobs that need persons
        # http://stackoverflow.com/a/291968 http://stackoverflow.com/a/13539479
        self.fields['helper_jobs'].queryset = HelperJob.objects.filter(has_enough_persons=False)
        self.fields['orga_jobs'].queryset = OrgaJob.objects.filter(has_enough_persons=False)

        # Add all fields you potentially need in Meta and then
        # dynamically remove not required fields from the form
        # Idea by https://www.silviogutierrez.com/blog/django-dynamic-forms/
        settingsAll = Settings.objects.all()
        if len(settingsAll) == 1:
            settings = settingsAll[0]

            fields_to_del = []
            #fields only required for a registration as tutor
            if not(settings.tutor_registration_enabled):
                fields_to_del.extend(['is_tutor','tutor_for'])

            #fields only required for a registration as orga
            if not(settings.orga_registration_enabled):
                fields_to_del.extend(['is_orga', 'orga_jobs'])

            #fields only required for a registration as helper
            if not(settings.helper_registration_enabled):
                fields_to_del.extend(['is_helper', 'helper_jobs'])

            #fields only required for a registration as tutor or orga
            if not(settings.tutor_registration_enabled) and not(settings.orga_registration_enabled):
                fields_to_del.extend(['dress_size'])

            #delete all fields not required
            for item in fields_to_del:
                del self.fields[item]

    class Meta:
        model = Person

        fields = [#fields that are always required
                  'prename', 'name', 'email', 'phone', 'matriculated_since',
                  'degree_course', 'experience_ophase', 'why_participate',
                  #fields only required for a registration as tutor
                  'is_tutor', 'tutor_for',
                  #fields only required for a registration as orga
                  'is_orga', 'orga_jobs',
                  #fields only required for a registration as helper
                  'is_helper', 'helper_jobs',
                  #fields only required for a registration as tutor or orga
                  'dress_size',
                  #fields that are always required at the end of the form
                  'remarks']

        widgets = {
            # set type for the phone field to tel. This might be done better
            'phone': forms.TextInput(attrs={'type': 'tel'}),
            # use checkboxes for multipleChoice @see http://stackoverflow.com/a/16937145
            'orga_jobs': forms.CheckboxSelectMultiple,
            'helper_jobs': forms.CheckboxSelectMultiple
        }


    def clean(self):
        cleaned_data = super(PersonForm, self).clean()

        if cleaned_data.get("is_tutor") and cleaned_data.get("tutor_for") is None:
            self.add_error('tutor_for', ValidationError('Um Tutor zu sein muss ausgewählt werden, welche Art Gruppe betreut werden soll.'))

        if cleaned_data.get("is_orga") and cleaned_data.get("orga_jobs").count() == 0:
            self.add_error('orga_jobs', ValidationError('Um Orga zu sein muss ausgewählt werden, welche Aufgaben übernommen werden sollen.'))

        if cleaned_data.get("is_helper") and cleaned_data.get("helper_jobs").count() == 0:
            self.add_error('helper_jobs', ValidationError('Um Helfer zu sein muss ausgewählt werden, bei welchen Aufgaben geholfen werden soll.'))

        if (cleaned_data.get("is_tutor") or cleaned_data.get("is_orga")) and cleaned_data.get("dress_size") is None:
            self.add_error('dress_size', ValidationError('Tutoren und Orgas bekommen ein kostenloses Kleidungsstück, wofür die Größe benötigt wird.'))
