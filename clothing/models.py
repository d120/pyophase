from django.db import models
from django.utils.translation import ugettext_lazy as _

from ophasebase.models import Ophase
from staff.models import Person


class Type(models.Model):
    class Meta:
        verbose_name = _("Art")
        verbose_name_plural = _("Arten")
        ordering = ['-price', 'name']

    name = models.CharField(max_length=75, verbose_name=_("Art"), unique=True)
    price = models.FloatField(verbose_name=_("Preis"))
    additional_only = models.BooleanField(verbose_name=_("Nur als selbst bezahltes Kleidungsstück möglich"), default=False)

    def __str__(self):
        return self.name


class Size(models.Model):
    class Meta:
        verbose_name = _("Größe")
        verbose_name_plural = _("Größen")

    size = models.CharField(max_length=75, verbose_name=_("Größe"), unique=True)

    def __str__(self):
        return self.size


class Color(models.Model):
    class Meta:
        verbose_name = _("Farbe")
        verbose_name_plural = _("Farben")

    name = models.CharField(max_length=75, verbose_name=_("Farbe"), unique=True)
    color_code = models.CharField(max_length=7, verbose_name=_("Farbcode"), default="#FFFFFF")

    def __str__(self):
        return self.name


class Order(models.Model):
    class Meta:
        verbose_name = _("Bestellung")
        verbose_name_plural = _("Bestellungen")

    person = models.ForeignKey(Person, verbose_name=_("Person"))
    type = models.ForeignKey(Type, verbose_name=_("Art"))
    size = models.ForeignKey(Size, verbose_name=_("Größe"))
    color = models.ForeignKey(Color, verbose_name=_("Farbe"))
    additional = models.BooleanField(verbose_name=_("Selbst bezahltes Kleidungsstück"))

    def __str__(self):
        return "{}: {} {} {}".format(
            self.person.name,
            self.type.name,
            self.size.size,
            self.color.name
        )

    @staticmethod
    def get_current(**kwargs):
        return Order.objects.filter(person__ophase=Ophase.current(), **kwargs)
