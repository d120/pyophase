from django.db import models
from django.utils import formats
from django.core.exceptions import ValidationError


class GroupCategory(models.Model):
    """Group category like "Bachelor", "Master german", "Master english", ..."""
    class Meta:
        verbose_name = "Gruppenkategorie"
        verbose_name_plural = "Gruppenkategorien"

    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label


class Job(models.Model):
    """A job during the Ophase for which persons are needed."""
    class Meta:
        abstract = True

    label = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.label


class OrgaJob(Job):
    """Job for an organizer."""
    class Meta:
        verbose_name = "Orgajob"
        verbose_name_plural = "Orgajobs"


class HelperJob(Job):
    """Job for a helper."""
    class Meta:
        verbose_name = "Helferjob"
        verbose_name_plural = "Helferjobs"


class Building(models.Model):
    """A building on the campus."""
    class Meta:
        verbose_name = "Gebäude"
        verbose_name_plural = "Gebäude"
        ordering = ['area', 'subarea', 'number']
        unique_together = ("area", "subarea", "number")

    AREA_CHOICES = (
        ("B", "Botanischer Garten (B)"),
        ("H", "Hochschulstadion (H)"),
        ("L", "Lichtwiese (L)"),
        ("S", "Stadtmitte (S)"),
        ("W", "Windkanal (W)"),
    )

    area = models.CharField(max_length=1, choices=AREA_CHOICES, default="S", verbose_name="Campus")
    subarea = models.PositiveSmallIntegerField(verbose_name="Campusabschnitt")
    number = models.PositiveSmallIntegerField(verbose_name="Gebäudenummer")
    label = models.CharField(max_length=50, default="", verbose_name="Gebäudename", blank=True)
    remarks = models.CharField(max_length=200, default="", verbose_name="Anmerkungen", blank=True)

    def get_name(self):
        return "%s%d|%02d" % (self.area, self.subarea, self.number)
    get_name.short_description = 'Nummer'

    def __str__(self):
        return self.get_name()


class Room(models.Model):
    """A room which could be used during the Ophase."""
    class Meta:
        verbose_name = "Raum"
        verbose_name_plural = "Räume"
        ordering = ['building', 'number']
        unique_together = ('building', 'number')

    ROOM_TYPE_CHOICES = (
        ("SR", "Kleingruppenraum"),
        ("HS", "Hörsaal"),
        ("PC", "PC-Pool"),
        ("LZ", "Lernzentrum"),
        ("SO", "Sonstiges")
    )

    building = models.ForeignKey(Building, verbose_name="Gebäude")
    number = models.CharField(max_length=50, verbose_name="Nummer")
    type = models.CharField(max_length=2, choices=ROOM_TYPE_CHOICES, verbose_name="Typ")
    hasBeamer = models.BooleanField(default=False, verbose_name="Beamer vorhanden?")
    capacity = models.IntegerField(verbose_name="Anzahl Plätze")
    lat = models.FloatField(verbose_name="Latitude", default=0, blank=True)
    lng = models.FloatField(verbose_name="Longitude", default=0, blank=True)

    def get_name(self):
        return "%s %s" % (self.building, self.number)
    get_name.short_description = "Name"

    def __str__(self):
        return self.get_name()


class Ophase(models.Model):
    """Settings object for Ophase."""
    class Meta:
        verbose_name = "Ophase"
        verbose_name_plural = "Ophasen"

    start_date = models.DateField(verbose_name="Beginn")
    end_date = models.DateField(verbose_name="Ende")
    is_active = models.BooleanField(default=False, verbose_name="Aktiv?")

    def get_name(self):
        term = "Ophase"
        if self.start_date.month == 4:
            term = "Sommerophase"
        elif self.start_date.month == 10:
            term = "Winterophase"
        return "%s %d" % (term, self.start_date.year)

    get_name.short_description = "Ophase"

    def __str__(self):
        return self.get_name()

    def get_human_duration(self):
        return "vom %s bis %s" % (formats.date_format(self.start_date, "MONTH_DAY_FORMAT"),
         formats.date_format(self.end_date, "DATE_FORMAT"))

    def clean(self, *args, **kwargs):
        super(Ophase, self).clean(*args, **kwargs)
        if self.start_date > self.end_date:
            raise ValidationError({'end_date': 'Ende der Ophase kann nicht vor ihrem Anfang liegen.'})

    def save(self, *args, **kwargs):
        # ensure is_active is only set for one Ophase at the same time
        if self.is_active:
            Ophase.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super(Ophase, self).save(*args, **kwargs)
