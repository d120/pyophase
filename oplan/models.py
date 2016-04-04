from django.db import models
from ophasebase.models import Ophase, Room
from staff.models import GroupCategory
from django.utils.translation import ugettext_lazy as _

# Oplan models


class Event(models.Model):
    """
    An event relevant for room planning.

    a.k.a. Raumbedarf / Termin
    """
    class Meta:
        verbose_name = _('Termin')
        verbose_name_plural = _('Termine')
        ordering = ['kommentar', 'duration', 'room', 'start_time']

    room = models.ForeignKey(Room, verbose_name=_('Raum'), blank=True, null=True)
    start_time = models.DateTimeField(verbose_name=_('Termin'), blank=True, null=True)
    duration = models.DurationField(verbose_name=_('Dauer'))
    min_places = models.IntegerField(verbose_name=_('Min. Places'), default=-1)
    kommentar = models.TextField(verbose_name=_('Kommentar'))
    room_preference = models.ForeignKey(Room, verbose_name=_('Room Preference'), related_name='room_preference', blank=True, null=True)
    zielgruppe = models.ManyToManyField('staff.GroupCategory', verbose_name=_('Zielgruppe'), related_name='events')
    color = models.CharField(verbose_name=_('Farbe'), max_length=7, default='#999999')


    def __str__(self):
        return str(self.room)

class RoomOpening(models.Model):
    """
    Information of whether a room is occupied (by another event) or reserved (for us) in a given time slot
    """
    class Meta:
        verbose_name = _('Raumreservierung')
        verbose_name_plural = _('Raumreservierungen')

    STATUS_CHOICES = (
        (1, _('OK (Reserved)')),
        (2, _('Blocked by other event')),
        (3, _('Should Request')),
        (4, _('Requested')),
    )

    room = models.ForeignKey(Room, verbose_name=_('Raum'))
    start_time = models.DateTimeField(verbose_name=_('Termin'))
    duration = models.DurationField(verbose_name=_('Dauer'))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    kommentar = models.TextField(verbose_name=_('Kommentar'))
    


