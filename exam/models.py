import math

from django.db import models
from django.utils import formats
from django.utils.translation import ugettext_lazy as _

from ophasebase.models import Ophase
from staff.models import GroupCategory
from students.models import Student


class ExamRoom(models.Model):
    """A room which is suitable for the exam."""
    class Meta:
        verbose_name = _('Klausurraum')
        verbose_name_plural = _('Klausurräume')
        ordering = ['available', '-capacity_1_free', '-capacity_2_free', 'room']

    room = models.OneToOneField('ophasebase.Room', models.CASCADE, verbose_name=_('Raum'), limit_choices_to={"type": "HS"})
    available = models.BooleanField(verbose_name=_('Verfügbar'), default=True)
    capacity_1_free = models.IntegerField(verbose_name=_('Plätze (1 Platz Abstand)'))
    capacity_2_free = models.IntegerField(verbose_name=_('Plätze (2 Plätze Abstand)'))

    def __str__(self):
        return str(self.room)

    def capacity(self, spacing):
        return self.capacity_1_free if spacing == 1 else self.capacity_2_free


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
    group_category = models.ForeignKey(GroupCategory, models.CASCADE, verbose_name=_('Gruppenkategorie'))
    spacing = models.PositiveSmallIntegerField(choices=SPACING_CHOICES, default=2, verbose_name=_('Sitzplatzabstand'))
    mode = models.PositiveSmallIntegerField(choices=MODE_CHOICES, default=0, verbose_name=_('Verteilmodus'))
    count = models.PositiveIntegerField(verbose_name=_('# Zuteilungen'))

    def __str__(self):
        # see http://stackoverflow.com/a/8288298
        formatted_datetime = formats.date_format(self.created_at, 'SHORT_DATETIME_FORMAT')
        return _('Zuteilung vom %(formated_datetime)s') % {
                 'formated_datetime' : formatted_datetime,}

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

        exam_rooms = ExamRoom.objects.filter(available=True)
        exam_students = Student.get_current(tutor_group__group_category=self.group_category, want_exam=True).order_by('name', 'prename')
        student_count = len(exam_students)

        if len(exam_rooms) == 0 or student_count == 0:
            return 0

        free_places = sum([exam_room.capacity(self.spacing) for exam_room in exam_rooms])
        places_needed = len(exam_students)

        # Set ratio either to a value where all rooms are used or
        # fixed 0.9 to fill up the first rooms up to 90 percent each
        ratio = places_needed / free_places if self.mode == 0 else 0.9

        total_used_places = 0
        split_points = []

        # Divide based on mode
        for exam_room in exam_rooms:
            used_places = math.ceil(exam_room.capacity(self.spacing) * ratio)
            end = min(total_used_places + used_places - 1, places_needed - 1)
            split_points.append(end)
            total_used_places = end + 1

        # Create individual assignments per person
        current_room = 0
        for index, student in enumerate(exam_students):
            ptr_assignment = PersonToExamRoomAssignment()
            ptr_assignment.room = exam_rooms[current_room]
            ptr_assignment.person = student
            ptr_assignment.assignment = self
            ptr_assignment.save()
            if index == split_points[current_room] + 1:
                current_room += 1

        return student_count


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
