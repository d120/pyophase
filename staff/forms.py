from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import escape, format_html
from django.utils.translation import ugettext as _

from ophasebase.models import OphaseCategory
from .models import HelperJob, OrgaJob, Person, Settings


class PersonForm(forms.ModelForm):

    def __append_description_link(self, field, view):
        """Append a link to a description view to the field label"""
        self.fields[field].label = escape(self.fields[field].label)
        code = ' <a href="{}" target="_blank">(%s)</a>' % _('Aufgabenbeschreibung')
        self.fields[field].label += format_html(code, reverse(view))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__append_description_link('tutor_for', 'staff:tutor_group_category_list')
        self.__append_description_link('orga_jobs', 'staff:orgajob_list')
        self.__append_description_link('helper_jobs', 'staff:helperjob_list')

        # Add all fields you potentially need in Meta and then
        # dynamically remove not required fields from the form
        # Idea by https://www.silviogutierrez.com/blog/django-dynamic-forms/
        settings = Settings.instance()
        if settings is not None:
            self.fields['tutor_for'].queryset = OphaseCategory.objects.filter(id__in=settings.group_categories_enabled.all().values_list('id'))
            self.fields['orga_jobs'].queryset = OrgaJob.filter_jobs_for_ophase_current().filter(id__in=settings.orga_jobs_enabled.all().values_list('id'))
            self.fields['helper_jobs'].queryset = HelperJob.filter_jobs_for_ophase_current().filter(id__in=settings.helper_jobs_enabled.all().values_list('id'))

            fields_to_del = []
            #fields only required for a registration as tutor
            if not settings.tutor_registration_enabled:
                fields_to_del.extend(['is_tutor', 'tutor_for'])

            #fields only required for a registration as orga
            if not settings.orga_registration_enabled:
                fields_to_del.extend(['is_orga', 'orga_jobs'])

            #fields only required for a registration as helper
            if not settings.helper_registration_enabled:
                fields_to_del.extend(['is_helper', 'helper_jobs'])

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
        cleaned_data = super().clean()

        if cleaned_data.get("is_tutor") and cleaned_data.get("tutor_for") is None:
            self.add_error('tutor_for', ValidationError(_('Um Tutor zu sein muss ausgewählt werden, welche Art Gruppe betreut werden soll.')))

        if cleaned_data.get("is_orga") and cleaned_data.get("orga_jobs").count() == 0:
            self.add_error('orga_jobs', ValidationError(_('Um Orga zu sein muss ausgewählt werden, welche Aufgaben übernommen werden sollen.')))

        if cleaned_data.get("is_helper") and cleaned_data.get("helper_jobs").count() == 0:
            self.add_error('helper_jobs', ValidationError(_('Um Helfer zu sein muss ausgewählt werden, bei welchen Aufgaben geholfen werden soll.')))

        if cleaned_data.get('is_tutor') != True and cleaned_data.get('is_helper') != True and cleaned_data.get('is_orga') != True:
            self.add_error(None, ValidationError(_('Du kannst an der OPhase nur mitwirken, wenn du dich als Tutor, Orga oder Helfer meldest. Bitte wähle mindestens eine Tätigkeit aus.')))

            for field in ('is_tutor', 'tutor_for', 'is_orga', 'orga_jobs', 'is_helper', 'helper_jobs'):
                self.add_error(field, None)
