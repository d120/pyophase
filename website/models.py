from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class Settings(models.Model):
    """Configuration for Website App."""
    class Meta:
        verbose_name = _("Einstellungen")
        verbose_name_plural = _("Einstellungen")

    helpdesk_phone_number = models.CharField(max_length=50)
    vorkurs_start_date = models.DateField()
    vorkurs_end_date = models.DateField()
    vorkurs_url = models.CharField(max_length=2000)
    vorkurs_forum_url = models.CharField(max_length=2000)
    vorkurs_slides_url = models.CharField(max_length=2000)
    accounts_url = models.CharField(max_length=2000)
    einforz_url = models.CharField(max_length=2000)

    @staticmethod
    def get_name():
        return '%s' % _("Website Einstellungen")

    def __str__(self):
        return self.get_name()

    def clean(self, *args, **kwargs):
        super().clean()
        if Settings.objects.count() > 0 and self.id != Settings.objects.get().id:
            raise ValidationError(_("Es ist nur sinnvoll und möglich eine Instanz des Einstellungsobjekts anzulegen."))

    @staticmethod
    def instance():
        try:
            return Settings.objects.get()
        except Settings.DoesNotExist:
            return None

class Schedule(models.Model):
    """A Schedule for a Degree during the Ophase"""
    class Meta:
        verbose_name = _("Stundenplan")
        verbose_name_plural = _("Stundenpläne")

    DEGREE_CHOICES = (
        ('BSC', _('Bachelor')),
        ('MSC', _('Master Deutsch')),
        ('DSS', _('Distributed Software Systems')),
    )

    degree = models.CharField(max_length=3, choices=DEGREE_CHOICES, verbose_name=_('Abschluss'), unique=True)
    image = models.ImageField(upload_to='website/schedule/', verbose_name=_('Stundenplan Bild'))
    stand = models.DateField(verbose_name=_('Stand des Stundenplans'))
