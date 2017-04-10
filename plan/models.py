from django.db import models
from django.utils.translation import ugettext_lazy as _

from ophasebase.models import Ophase, Room, OphaseCategory
from staff.models import StaffFilterGroup, TutorGroup


class SlotType(models.Model):
    class Meta:
        verbose_name = _("Veranstaltungsart")
        verbose_name_plural = _("Veranstaltungsarten")
        ordering = ['name']

    name = models.CharField(max_length=50, blank=False)
    color = models.CharField(max_length=7, default="#FFFFFF", blank=False)

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    """Time slot for events"""
    class Meta:
        verbose_name = _("Zeitslot")
        verbose_name_plural = _("Zeitslots")
        ordering = ['begin']

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slottype = models.ForeignKey(SlotType, on_delete=models.CASCADE)
    begin = models.DateTimeField(verbose_name=_("Beginn"))
    end = models.DateTimeField(verbose_name=_("Ende"))
    category = models.ManyToManyField(OphaseCategory)
    relevant_for = models.ForeignKey(StaffFilterGroup, verbose_name=_("Filterkriterium: Wer könnte anwesend sein?"), null=True, on_delete=models.SET_NULL)
    attendance_required = models.BooleanField(blank=True, default=False)
    ophase = models.ForeignKey(Ophase, models.CASCADE)
    public = models.BooleanField(blank=True, default=False)

    @classmethod
    def get_current_events(cls, **kwargs):
        return cls.objects.filter(ophase=Ophase.current(), **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        unique_together = ['timeslot', 'tutorgroup']

    timeslot = models.ForeignKey(TimeSlot, verbose_name=_('Zeitslot'), on_delete=models.CASCADE)
    room = models.ForeignKey(Room, null=True, verbose_name=_("Raum"), blank=True, on_delete=models.SET_NULL)
    tutorgroup = models.ForeignKey(TutorGroup, null=True, verbose_name=_('Kleingruppe'), blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.tutorgroup is not None:
            return "{} ({})".format(str(self.timeslot), str(self.tutorgroup))
        return str(self.timeslot)
