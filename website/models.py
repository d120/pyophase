import os

from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_delete
from django.template.defaultfilters import date as _date
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from ophasebase.models import OphaseCategory


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


class OInforz(models.Model):
    """An OInforz PDF booklet version"""
    class Meta:
        verbose_name = _("OInforz")
        verbose_name_plural = _("OInforze")

    def fixedname_upload_to(instance, filename):
        """returns the path and name where the image should upload to"""
        x, file_extension = os.path.splitext(filename)
        return '{}{}{}'.format('website/oinforz/', instance.name.lower(), file_extension)

    name = models.CharField(max_length=25, verbose_name=_('Abschluss'))
    file = models.FileField(verbose_name=_('OInforz PDF'),
                upload_to=fixedname_upload_to, storage=OverwriteStorage())
    last_modified = models.DateField(verbose_name=_('Stand des OInforzes'))

    def __str__(self):
        return '{} {}'.format(self.name, _date(self.last_modified, 'SHORT_DATE_FORMAT'))


# Register a signal receiver so the document is deleted when the model is deleted
@receiver(pre_delete, sender=OInforz)
def oinforz_delete(sender, instance, **kwargs):
    instance.file.delete(False)


class CategoryDetails(models.Model):
    class Meta:
        verbose_name = _("Webseitendetails für Kategorie")
        verbose_name_plural = _("Webseitendetails für Kategorien")

    def fixedname_upload_to(self, filename):
        """returns the path and name where the image should upload to"""
        x, file_extension = os.path.splitext(filename)
        return '{}{}{}'.format('website/schedule/', self.category.slug, file_extension)

    category = models.OneToOneField(OphaseCategory, on_delete=models.CASCADE, related_name="website")
    oinforz = models.ForeignKey(OInforz, verbose_name=_("OInforz"), on_delete=models.PROTECT, null=True, blank=True)
    schedule_image = models.ImageField(verbose_name=_('Stundenplan Bild'),
                upload_to=fixedname_upload_to, storage=OverwriteStorage(), null=True, blank=True)
    schedule_last_modified = models.DateField(verbose_name=_('Stand des Stundenplans'), auto_now=True)

    @property
    def description_template(self):
        return "website/description/{}.html".format(self.category.slug)

    def __str__(self):
        return self.category.name


# Create a new instance of CategoryDetails each time a OphaseCategory is created
@receiver(post_save, sender=OphaseCategory)
def create_category_details(sender, instance, created, **kwargs):
    if created:
        CategoryDetails.objects.create(category=instance)


# Update the object of CategoryDetails each time the corresponding object of OphaseCategory is updated
@receiver(post_save, sender=OphaseCategory)
def save_category_details(sender, instance, **kwargs):
    instance.website.save()


# Register a signal receiver so the image is deleted when the model is deleted
@receiver(pre_delete, sender=CategoryDetails)
def schedule_delete(sender, instance, **kwargs):
    instance.image.delete(False)
