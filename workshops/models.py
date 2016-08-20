from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import date as _date
from django.utils.translation import ugettext_lazy as _

from ophasebase.models import Ophase

class WorkshopSlot(models.Model):
    """Date and time of a workshop slot."""
    class Meta:
        verbose_name = _('Workshopslot')
        verbose_name_plural = _('Workshopslots')
        ordering = ['date', 'start_time']

    ophase = models.ForeignKey(Ophase, models.CASCADE)
    date = models.DateField(verbose_name=_('Datum'))
    start_time = models.TimeField(verbose_name=_('Beginn'))
    end_time = models.TimeField(verbose_name=_('Ende'))

    def __str__(self):
        return _date(self.date, "D, ") + _date(self.date, "SHORT_DATE_FORMAT") + _date(self.start_time, " H:i - ") + _date(self.end_time, "H:i")

    @staticmethod
    def get_current(**kwargs):
        return WorkshopSlot.objects.filter(ophase=Ophase.current(), **kwargs)


class Workshop(models.Model):
    """A workshop offered in the Ophase."""
    class Meta:
        verbose_name = _('Workshop')
        verbose_name_plural = _('Workshops')

    ophase = models.ForeignKey(Ophase, models.CASCADE)
    tutor_name = models.CharField(max_length=100, verbose_name=_('Name'))
    tutor_mail = models.EmailField(verbose_name=_('E-Mail-Adresse'))
    title = models.CharField(max_length=200, verbose_name=_('Workshoptitel'), help_text=_('Unter welcher Überschrift steht der Workshop?'))
    workshop_type = models.CharField(max_length=40, verbose_name=_('Art des Workshops'), help_text=_('Welche Art Veranstaltung ist das? Vortrag, Vortrag mit Hands-on, Workshop, Sport, Ausflug, ...'))
    possible_slots = models.ManyToManyField(WorkshopSlot, verbose_name=_('Mögliche Zeitslots'), help_text=_('Welche Slots sind zeitlich möglich (unabhängig davon wie oft der Workshop stattfinden kann)?'))
    how_often = models.PositiveSmallIntegerField(verbose_name=_('Anzahl'), help_text=_('Wie oft kann dieser Workshop angeboten werden?'))
    location_info = models.CharField(max_length=200, verbose_name=_('Raumbedarf'), help_text=_('Wo soll der Workshop stattfinden (Hörsaal, Gruppenraum, Poolraum, ...)?'))
    max_participants = models.PositiveSmallIntegerField(verbose_name=_('Max. Teilnehmerzahl'), help_text=_('Maximale Teilnehmeranzahl (auf 0 lassen für volle Raumkapazität).'))
    equipment = models.CharField(blank=True, max_length=200, verbose_name=_('Benötigtes Material'), help_text=_('Wird etwas benötigt das wir zur Verfügung stellen sollen?'))
    participant_requirements = models.TextField(blank=True, verbose_name=_('Teilnahmevoraussetzungen'), help_text=_('Benötigen die Teilnehmer Vorkenntnisse oder müssen sie etwas mitbringen?'))
    description = models.TextField(verbose_name=_('Beschreibungstext'), help_text=_('Eine kurze Beschreibung für OInforz und Aushänge um was es geht und was die Teilnehmer erwartet.'))
    remarks = models.TextField(blank=True, verbose_name=_('Anmerkungen'), help_text=_('Sonstige Informationen für den Orga'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Eingetragen am"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Verändert am"))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.ophase_id is None:
            # set Ophase to current active one. We assume that there is only one active Ophase at the same time!
            self.ophase = Ophase.current()
        super().save(*args, **kwargs)

    @staticmethod
    def get_current(**kwargs):
        return Workshop.objects.filter(ophase=Ophase.current(), **kwargs)


class Settings(models.Model):
    """Configuration for Workshop app."""
    class Meta:
        verbose_name = _("Einstellungen")
        verbose_name_plural = _("Einstellungen")

    workshop_submission_enabled = models.BooleanField(default=False, verbose_name=_("Workshop-Einreichung aktiv"))
    orga_email = models.CharField(max_length=100, verbose_name=_("E-Mail-Adresse des Workshop-Orgas"))

    def get_name(self):
        return '%s' % _("Workshops Einstellungen")

    def __str__(self):
        return self.get_name()

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if Settings.objects.count() > 0 and self.id != Settings.objects.get().id:
            raise ValidationError(_("Es ist nur sinnvoll und möglich eine Instanz des Einstellungsobjekts anzulegen."))

    @staticmethod
    def instance():
        try:
            return Settings.objects.get()
        except Settings.DoesNotExist:
            return None
