from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from ophasebase.models import Ophase, Room, OphaseCategory
from staff.models import TutorGroup


class SlotType(models.Model):
    class Meta:
        verbose_name = _("Veranstaltungsart")
        verbose_name_plural = _("Veranstaltungsarten")
        ordering = ['name']

    name = models.CharField(max_length=50, blank=False)
    color = models.CharField(max_length=7, default="#FFFFFF", blank=False)
    split_groups = models.BooleanField(verbose_name=_("In Kleingruppen aufteilen?"), default=False, blank=True)

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
    relevant_for = models.ForeignKey("staff.StaffFilterGroup", verbose_name=_("Filterkriterium: Wer könnte anwesend sein?"), blank=True, null=True, on_delete=models.SET_NULL)
    attendance_required = models.BooleanField(blank=True, default=False)
    ophase = models.ForeignKey(Ophase, models.CASCADE)
    public = models.BooleanField(blank=True, default=False)

    @classmethod
    def get_current_events(cls, **kwargs):
        return cls.objects.filter(ophase=Ophase.current(), **kwargs)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.ophase_id is None:
            # set Ophase to current active one. We assume that there is only one active Ophase at the same time!
            self.ophase = Ophase.current()
        super().save(*args, **kwargs)


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

    @staticmethod
    @receiver(post_save, sender=TimeSlot)
    def handle_timeslot_created(sender, instance, created, **kwargs):
        """
        Create corresponding event for a recently created timeslot
        Only those kind of timeslot that require only one event are considered by this callback
        
        :param created: A boolean; True if a new record was created 
        :param instance: The actual instance being saved (timeslot)
        :param sender: The model class
        """

        # Create a single event if groups don't have to be split
        if not instance.slottype.split_groups:
            Event.objects.create(timeslot=instance)

    @staticmethod
    # @receiver(m2m_changed, sender=TimeSlot.category.though)
    def handle_timeslot_created(sender, instance, action, **kwargs):
        """
        Create corresponding events for a recently created timeslot
        Only those kind of timeslot that require only mulitple event are considered by this callback
        
        :param instance: The actual instance being saved (timeslot)
        :param sender: The model class
        """

        # Added categories? Split groups?
        if action == "post_add" and instance.slottype.split_groups:
            # Create events for all tutorgroups in all categories
            for category in instance.category.all():
                for tg in category.tutorgroup_set.all():
                    if not Event.objects.filter(timeslot=instance, tutorgroup=tg).exists():
                        Event.objects.create(
                            timeslot=instance,
                            tutorgroup=tg
                        )

m2m_changed.connect(Event.handle_timeslot_created, sender=TimeSlot.category.through)


class Booking(models.Model):
    class Meta:
        verbose_name = _('Raumbuchung')
        verbose_name_plural = _('Raumbuchungen')
        ordering = ['room', '-begin']

    STATUS_CHOICES = (
        (1, _('Gebucht')),
        (2, _('Blockiert')),
        (3, _('Anfragen?')),
        (4, _('Angefragt')),
        (5, _('Überlappung')),
    )

    room = models.ForeignKey(Room, verbose_name=_('Raum'), on_delete=models.CASCADE)
    begin = models.DateTimeField(verbose_name=_('Anfang'))
    end = models.DateTimeField(verbose_name=_('Ende'))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    comment = models.TextField(verbose_name=_('Kommentar'), blank=True)

    def __str__(self):
        return "{} ({} - {})".format(self.room, self.begin, self.end)
