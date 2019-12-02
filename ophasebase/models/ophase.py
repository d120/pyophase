import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import formats
from django.utils.translation import gettext_lazy as _

class Ophase(models.Model):
    """Object representing an Ophase."""
    class Meta:
        verbose_name = _('Ophase')
        verbose_name_plural = _('Ophasen')

    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False, verbose_name=_('Aktiv?'))
    contact_email_address = models.EmailField(verbose_name=_('Kontaktadresse Leitung'))
    categories = models.ManyToManyField("OphaseCategory", through="OphaseActiveCategory", related_name=u'ophase_categories')
    start_date_by_category = models.DateField(verbose_name=_('Beginn'), blank=True, null=True)
    end_date_by_category = models.DateField(verbose_name=_('Ende'), blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def start_date(self):
        if self.start_date_by_category is None:
            return datetime.date.today()
        return self.start_date_by_category

    @property
    def end_date(self):
        if self.end_date_by_category is None:
            return datetime.date.today()
        return self.end_date_by_category

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
        except:
            return None
