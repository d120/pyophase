from functools import partial
from itertools import chain, repeat

import math
from django.db import models
from django.db.models import Sum
from django.utils import formats
from django.utils.translation import ugettext_lazy as _

from ophasebase.models import Ophase, OphaseCategory
from students.models import Student


class ExamRoom(models.Model):
    """A room which is suitable for the exam."""

    class Meta:
        verbose_name = _('Klausurraum')
        verbose_name_plural = _('Klausurräume')
        ordering = ['available', '-capacity_1_free', '-capacity_2_free', 'room']

    room = models.OneToOneField('ophasebase.Room', models.CASCADE, verbose_name=_('Raum'),
                                limit_choices_to={"type": "HS"})
    available = models.BooleanField(verbose_name=_('Verfügbar'), default=True)
    capacity_1_free = models.IntegerField(verbose_name=_('Plätze (1 Platz Abstand)'))
    capacity_2_free = models.IntegerField(verbose_name=_('Plätze (2 Plätze Abstand)'))

    def __str__(self):
        return str(self.room)

    def capacity(self, spacing):
        return self.capacity_1_free if spacing == 1 else self.capacity_2_free

    def seats(self, spacing, ratio):
        return math.ceil(self.capacity(spacing) * ratio)


class Assignment(models.Model):
    """
    An assignment of Students to different ExamRooms

    Objects of this type cannot be changed afterwards. Changes done after first insertion in database will be
    automatically discarded
    """

    class Meta:
        verbose_name = _('Klausurzuteilung')
        verbose_name_plural = _('Klausurzuteilungen')
        get_latest_by = 'created_at'
        ordering = ['-created_at']

    SPACING_CHOICES = (
        (1, _('Ein Platz Abstand')),
        (2, _('Zwei Plätze Abstand'))
    )

    MODE_CHOICES = (
        (0, _('Gleichmäßig auf alle Räume verteilen')),
        (1, _('Möglichst wenig Räume'))
    )

    ophase = models.ForeignKey(Ophase, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    group_category = models.ForeignKey(OphaseCategory, models.CASCADE, verbose_name=_('Gruppenkategorie'))
    spacing = models.PositiveSmallIntegerField(choices=SPACING_CHOICES, default=2, verbose_name=_('Sitzplatzabstand'))
    mode = models.PositiveSmallIntegerField(choices=MODE_CHOICES, default=0, verbose_name=_('Verteilmodus'))
    count = models.PositiveIntegerField(verbose_name=_('# Zuteilungen'))

    def __str__(self):
        # see http://stackoverflow.com/a/8288298
        formatted_datetime = formats.date_format(self.created_at, 'SHORT_DATETIME_FORMAT')
        return _('Zuteilung vom %(formated_datetime)s') % {
            'formated_datetime': formatted_datetime, }

    def save(self, *args, **kwargs):
        if self.ophase_id is None:
            # set Ophase to current active one. We assume that there is only one active Ophase at the same time!
            self.ophase = Ophase.current()

        # Only allow changes (and creation of individual assignments) the first time the object is created
        # An Assignment cannot be changed afterwards
        if not self.pk:  # Object is being created, thus no primary key field yet
            # Temporarily set count to 0
            self.count = 0
            super().save(*args, **kwargs)

            # Create Person to Room Assignments
            # (this has to be done after saving since a reference to the current object is needed)
            self.count = self.assign()
            # Now the count can be updated and saved again
            super().save(*args, **kwargs)

    def assign(self):
        """
        Do the real assignment based on object properties
        """

        spacing = self.spacing
        capacity_string = 'capacity_{:d}_free'.format(spacing)
        order_by_string = "-{:s}".format(capacity_string)

        exam_rooms = ExamRoom.objects.filter(available=True).order_by(order_by_string)
        exam_students = Student.get_current(tutor_group__group_category=self.group_category, want_exam=True)
        exam_students = exam_students.order_by('name', 'prename')
        student_count = exam_students.count()

        if exam_rooms.count() == 0 or student_count == 0:
            return 0

        maximum_capacity = exam_rooms.aggregate(maximum_capacity=Sum(capacity_string)).get('maximum_capacity')

        # Set ratio so that all room gets equals percentage
        ratio = student_count / maximum_capacity

        # on minimal room mode and if the ratio is less then 90% the ratio is set to 90%
        # e.g. the first rooms get filled by 90%. The other rooms are not used
        if self.mode == 1 and ratio < 0.9:
            ratio = 0.9

        # returns each room as often as seats are available for the given ratio
        exam_room_list = chain.from_iterable(repeat(room, room.seats(spacing, ratio)) for room in exam_rooms)

        assign = partial(PersonToExamRoomAssignment, assignment=self)

        assignments = (assign(person=student, room=room) for student, room in zip(exam_students, exam_room_list))
        result = PersonToExamRoomAssignment.objects.bulk_create(assignments)

        return len(result)


class PersonToExamRoomAssignment(models.Model):
    """
    An assignment of a single student to a single room (belonging to exactly one assignment)
    """

    class Meta:
        verbose_name = _('Individuelle Klausurzuteilung')
        verbose_name_plural = _('Individuelle Klausurzuteilungen')
        ordering = ['assignment', 'room', 'person__name', 'person__prename']

    assignment = models.ForeignKey(Assignment, models.CASCADE)
    room = models.ForeignKey(ExamRoom, models.CASCADE)
    person = models.ForeignKey(Student, models.CASCADE)
