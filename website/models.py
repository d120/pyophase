from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.template.defaultfilters import date as _date
from django.utils.translation import ugettext_lazy as _

import os

class Settings(models.Model):
    """Configuration for Website App."""
    class Meta:
        verbose_name = _("Einstellungen")
        verbose_name_plural = _("Einstellungen")

    helpdesk_phone_number = models.CharField(max_length=50)
    vorkurs_start_date = models.DateField()
    vorkurs_end_date = models.DateField()
    vorkurs_url = models.URLField()
    vorkurs_forum_url = models.URLField()
    vorkurs_slides_url = models.URLField()
    accounts_url = models.URLField()
    einforz_url = models.URLField()

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

class OverwriteStorage(FileSystemStorage):
    """Delete the old file so that the name is available"""
    def get_available_name(self, name, max_length):
        self.delete(name)
        return super().get_available_name(name, max_length)

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

    def fixedname_upload_to(instance, filename):
        """returns the path and name where the image should upload to"""
        path = 'website/schedule/'
        name = instance.degree.lower()
        x, file_extension = os.path.splitext(filename)
        return '{}{}{}'.format(path, name, file_extension)

    degree = models.CharField(max_length=3, choices=DEGREE_CHOICES, verbose_name=_('Abschluss'), unique=True)
    image = models.ImageField(verbose_name=_('Stundenplan Bild'),
                upload_to=fixedname_upload_to, storage=OverwriteStorage())
    stand = models.DateField(verbose_name=_('Stand des Stundenplans'))

    def __str__(self):
        return '{} {}'.format(self.get_degree_display(), _date(self.stand, 'SHORT_DATE_FORMAT'))

#Register an signal receiver so the image is deletet when the model is deleted
@receiver(pre_delete, sender=Schedule)
def schedule_delete(sender, instance, **kwargs):
    instance.image.delete(False)
