from django.db import models
from staff.models import Person
from django.utils.translation import ugettext_lazy as _


class Type(models.Model):
    class Meta:
        verbose_name = _("Art")
        verbose_name_plural = _("Arten")
        ordering = ['-preis', 'name']

    name = models.CharField(max_length=75, verbose_name=_("Art"), unique=True)
    price = models.FloatField(verbose_name=_("Preis"))


class Size(models.Model):
    class Meta:
        verbose_name = _("Größe")
        verbose_name_plural = _("Größen")

    size = models.CharField(max_length=75, verbose_name=_("Größe"), unique=True)


class Color(models.Model):
    class Meta:
        verbose_name = _("Farbe")
        verbose_name_plural = _("Farben")

    name = models.CharField(max_length=75, verbose_name=_("Farbe"), unique=True)
    color_code = models.CharField(max_length=7, verbose_name=_("Farbcode"), default="#FFFFFF")


class Order(models.Model):
    class Meta:
        verbose_name = _("Bestellung")
        verbose_name_plural = _("Bestellungen")

    person = models.ForeignKey(Person)
    type = models.ForeignKey(Type)
    size = models.ForeignKey(Size)
    color = models.ForeignKey(Color)
