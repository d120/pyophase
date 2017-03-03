from django.db import models
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