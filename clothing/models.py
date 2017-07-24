from django.core.exceptions import ValidationError
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
        ordering = ('size_sortable', 'size')

    size = models.CharField(max_length=75, verbose_name=_("Größe"), unique=True)
    size_sortable = models.PositiveSmallIntegerField(default = 0, verbose_name=_("Sortierbare Größe"), help_text=_("Dieser Wert wird automatisch berechnet"))

    def __str__(self):
        return self.size

    def sortable_size(self):
        """returns a sortable value of the current size.
           So that XS < S < M < L < XL < XXL < 3XL is true"""
        # The compution runs on Uppercase without trailing whitespace
        input = self.size.strip().upper()
        # Main value is given by the last char
        last_char = input[-1]

        # Assign the base value regarding the last char
        value = {'S':10, 'M':20, 'L':30}.get(last_char, 0)

        # A 'X' before has only a  effect if the last char is 'L' or 'S'
        x_value = {'S':-1, 'L':1}.get(last_char, 0)

        # If a 'X' before would have an effect
        if x_value != 0:
            # Loop from the second to last char
            for c in reversed(input[:-1]):
                # ignore space between chars
                if c.isspace():
                    continue
                # if a 'X' occur add the x_value
                elif c == 'X':
                    value += x_value
                # if a number occure add the x_value times the value of c
                elif c in [str(i) for i in range(2,10)]:
                    value += x_value * (int(c) - 1)
                    # a number is the first possible char with an effect
                    break
                else:
                    # If another char occur we end the loop. All following 
                    # chars will not have an effect on the value
                    break

        return value

    def save(self, *args, **kwargs):
        self.size_sortable = self.sortable_size()
        super().save(*args, **kwargs)


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

    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name=_("Person"))
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name=_("Art"))
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name=_("Größe"))
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name=_("Farbe"))
    additional = models.BooleanField(verbose_name=_("Selbst bezahltes Kleidungsstück"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Erstellt am"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Verändert am"))
    paid = models.BooleanField(default=False)
    received_at = models.DateField(null=True, blank=True, verbose_name=_("Ausgegeben am"))

    def __str__(self):
        return "{}: {} {} {}".format(
            self.person.name,
            self.type.name,
            self.size.size,
            self.color.name
        )

    def info(self):
        return "{} {} {} ({})".format(
            str(self.type), str(self.size), str(self.color),
            _("selbst bezahlt") if self.additional else _("kostenlos")
        )

    @staticmethod
    def get_current(**kwargs):
        return Order.objects.filter(person__ophase=Ophase.current(), **kwargs)

    @classmethod
    def user_eligible_but_not_ordered_yet(cls, user):
        return user.eligible_for_clothing and (cls.get_current().filter(person=user, additional=False).count() == 0)


class Settings(models.Model):
    """Configuration for clothing app."""
    class Meta:
        verbose_name = _("Einstellungen")
        verbose_name_plural = _("Einstellungen")

    clothing_ordering_enabled = models.BooleanField(default=False, verbose_name=_("Kleiderbestellung aktiv"))

    def get_name(self):
        return '%s' % _("Clothing Einstellungen")

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
