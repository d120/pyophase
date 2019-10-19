from django.db import models
from django.db.models import Min, Max
from django.utils import formats
from django.utils.translation import ugettext_lazy as _

from ophasebase.models.ophase import Ophase


class OphaseCategory(models.Model):
    """Object representing the category of an Ophase"""
    class Meta:
        verbose_name = _('Art der Ophase')
        verbose_name_plural = _('Arten der Ophase')
        ordering = ['priority']

    name = models.CharField(max_length=100, verbose_name=_('Name'))
    slug = models.CharField(max_length=25, verbose_name=_('URL Slug'), unique=True)
    lang = models.CharField(max_length=5, verbose_name=_('Sprachcode'), default="de")
    priority = models.PositiveIntegerField(verbose_name=_("Priorität"), help_text=_("Die Priorität bestimmt unter anderem die Reihenfolge der Anzeige auf der Webseite"))

    def label(self):
        """Return name as label for compatibility with Job model"""
        return self.name

    def __str__(self):
        return self.name


class OphaseActiveCategory(models.Model):
    """An active category of a given Ophase"""
    class Meta:
        verbose_name = _('Aktive Kategorie einer Ophase')
        verbose_name_plural = _('Aktive Kategorien einer Ophase')
        ordering = ['ophase', 'category']

    ophase = models.ForeignKey(Ophase, verbose_name=_('Ophase'), on_delete=models.CASCADE)
    category = models.ForeignKey(OphaseCategory, verbose_name=_('Art der Ophase'), on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name=_('Beginn'))
    end_date = models.DateField(verbose_name=_('Ende'))

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
        Returns the start_date and end_date of the ophase category as
        human readable e.g. 3. - 6. April
        """
        beginformat = 'j. '
        if self.start_date.month != self.end_date.month:
            beginformat += 'F'
        endformat = 'j. F'
        return '%(begin)s - %(end)s' % {
          'begin': formats.date_format(self.start_date, beginformat),
          'end': formats.date_format(self.end_date, endformat),}

    def __str__(self):
        return "{}: {}".format(self.ophase, self.category)

    def save(self, *args, **kwargs):
        res = super().save(*args, **kwargs)

        dates = OphaseActiveCategory.objects.filter(ophase=self.ophase).aggregate(start=Min('start_date'), end=Max('end_date'))
        self.ophase.start_date_by_category = dates.get('start', None)
        self.ophase.end_date_by_category = dates.get('end', None)
        self.ophase.save()

        return res
