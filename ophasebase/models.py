from django.core.exceptions import ValidationError
from django.db import models
from django.utils import formats
from django.utils.datetime_safe import datetime
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

    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False, verbose_name=_('Aktiv?'))
    contact_email_address = models.EmailField(verbose_name=_('Kontaktadresse Leitung'))
    categories = models.ManyToManyField("OphaseCategory", through="OphaseActiveCategory", related_name=u'ophase_categories')

    def __str__(self):
        return self.name

    @property
    def start_date(self):
        if self.ophaseactivecategory_set.count() == 0:
            return datetime.now()
        return min(c.start_date for c in self.ophaseactivecategory_set.all())

    @property
    def end_date(self):
        if self.ophaseactivecategory_set.count() == 0:
            return datetime.now()
        return max(c.end_date for c in self.ophaseactivecategory_set.all())

    def get_semester(self):
        term = _('Jahr')
        if self.start_date.month == 4:
            term = _('Sommersemester')
        elif self.start_date.month == 10:
            term = _('Wintersemester')
        return "%s %d" % (term, self.start_date.year)

    def get_human_duration(self):
        """
        Returns the start_date and end_date of the ophase as human readable
        e.g. vom 3. April 2014 bis 6. April 2016
        """
        return _('vom %(begin)s bis %(end)s') % {
          'begin': formats.date_format(self.start_date, 'DATE_FORMAT'),
          'end': formats.date_format(self.end_date, 'DATE_FORMAT'),}

    def get_human_short_duration(self):
        """
        Returns the start_date and end_date of the ophase as
        human readable e.g. 3. - 6. April
        """
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


class OphaseCategory(models.Model):
    """Object representing the category of an Ophase"""
    class Meta:
        verbose_name = _('Art der Ophase')
        verbose_name_plural = _('Arten der Ophase')
        ordering = ['priority']

    name = models.CharField(max_length=100, verbose_name=_('Name'))
    priority = models.PositiveIntegerField(verbose_name=_("Priorität"), help_text=_("Die Priorität bestimmt unter anderem die Reihenfolge der Anzeige auf der Webseite"))

    def __str__(self):
        return self.name


class OphaseActiveCategory(models.Model):
    """An active category of a given Ophase"""
    class Meta:
        verbose_name = _('Aktive Kategorie einer Ophase')
        verbose_name_plural = _('Aktive Katgegorien einer Ophase')
        ordering = ['ophase', 'category']

    ophase = models.ForeignKey(Ophase, verbose_name=_('Ophase'))
    category = models.ForeignKey(OphaseCategory, verbose_name=_('Art der Ophase'))
    start_date = models.DateField(verbose_name=_('Beginn'))
    end_date = models.DateField(verbose_name=_('Ende'))

    def __str__(self):
        return "{}: {}".format(self.ophase, self.category)
