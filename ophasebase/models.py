from django.core.exceptions import ValidationError
from django.db import models
from django.utils import formats
from django.utils.translation import ugettext_lazy as _


class Building(models.Model):
    """A building on the campus."""
    class Meta:
        verbose_name = _('Gebäude')
        verbose_name_plural = _('Gebäude')
        ordering = ['area', 'subarea', 'number']
        unique_together = ("area", "subarea", "number")

    AREA_CHOICES = (
        ("B", _('Botanischer Garten (B)')),
        ("H", _('Hochschulstadion (H)')),
        ("L", _('Lichtwiese (L)')),
        ("S", _('Stadtmitte (S)')),
        ("W", _('Windkanal (W)')),
    )

    area = models.CharField(max_length=1, choices=AREA_CHOICES, default="S", verbose_name=_('Campus'))
    subarea = models.PositiveSmallIntegerField(verbose_name=_('Campusabschnitt'))
    number = models.PositiveSmallIntegerField(verbose_name=_('Gebäudenummer'))
    label = models.CharField(max_length=50, default="", verbose_name=_('Gebäudename'), blank=True)
    remarks = models.CharField(max_length=200, default="", verbose_name=_('Anmerkungen'), blank=True)

    def get_name(self):
        return "%s%d|%02d" % (self.area, self.subarea, self.number)
    get_name.short_description = 'Nummer'

    def __str__(self):
        return self.get_name()


class Room(models.Model):
    """A room which could be used during the Ophase."""
    class Meta:
        verbose_name = _('Raum')
        verbose_name_plural = _('Räume')
        ordering = ['building', 'number']
        unique_together = ('building', 'number')

    ROOM_TYPE_CHOICES = (
        ("SR", _('Kleingruppenraum')),
        ("HS", _('Hörsaal')),
        ("PC", _('PC-Pool')),
        ("LZ", _('Lernzentrum')),
        ("SO", _('Sonstiges'))
    )

    building = models.ForeignKey(Building, models.CASCADE, verbose_name=_('Gebäude'))
    number = models.CharField(max_length=50, verbose_name=_('Nummer'))
    type = models.CharField(max_length=2, choices=ROOM_TYPE_CHOICES, verbose_name=_('Typ'))
    has_beamer = models.BooleanField(default=False, verbose_name=_('Beamer vorhanden?'))
    capacity = models.IntegerField(verbose_name=_('Anzahl Plätze'))
    lat = models.FloatField(verbose_name=_('Latitude'), default=0, blank=True)
    lng = models.FloatField(verbose_name=_('Longitude'), default=0, blank=True)

    def get_name(self):
        return "%s %s" % (self.building, self.number)
    get_name.short_description = _('Name')

    def __str__(self):
        return self.get_name()


class Ophase(models.Model):
    """Object representing an Ophase."""
    class Meta:
        verbose_name = _('Ophase')
        verbose_name_plural = _('Ophasen')

    start_date = models.DateField(verbose_name=_('Beginn'))
    end_date = models.DateField(verbose_name=_('Ende'))
    is_active = models.BooleanField(default=False, verbose_name=_('Aktiv?'))
    contact_email_address = models.CharField(max_length=100, verbose_name=_('Kontaktadresse Leitung'))

    def get_name(self):
        term = _('Ophase')
        if self.start_date.month == 4:
            term = _('Sommerophase')
        elif self.start_date.month == 10:
            term = _('Winterophase')
        return "%s %d" % (term, self.start_date.year)

    get_name.short_description = _('Ophase')

    def __str__(self):
        return self.get_name()

    def get_human_duration(self):
        """Returns the start_date and end_date of the ophase as human readable 
e.g. vom 3. April 2014 bis 6. April 2016"""
        return _('vom %(begin)s bis %(end)s') % {
          'begin': formats.date_format(self.start_date, 'DATE_FORMAT'),
          'end': formats.date_format(self.end_date, 'DATE_FORMAT'),}

    def get_human_short_duration(self):
        """Returns the start_date and end_date of the ophase as 
human readable e.g. 3. - 6. April"""
        beginformat = 'j. '
        if self.start_date.month != self.end_date.month:
            beginformat +='F'
        endformat = 'j. F'
        return '%(begin)s - %(end)s' % {
          'begin': formats.date_format(self.start_date, beginformat),
          'end': formats.date_format(self.end_date, endformat),}

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if self.start_date > self.end_date:
            raise ValidationError({'end_date': _('Ende der Ophase kann nicht vor ihrem Anfang liegen.')})

    def save(self, *args, **kwargs):
        # ensure is_active is only set for one Ophase at the same time
        if self.is_active:
            Ophase.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    @staticmethod
    def current():
        try:
            return Ophase.objects.get(is_active=True)
        except Ophase.DoesNotExist:
            return None
