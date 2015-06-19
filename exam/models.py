from django.db import models


class ExamRoom(models.Model):
    """A room which is suitable for the exam."""
    class Meta:
        verbose_name = "Klausurraum"
        verbose_name_plural = "Klausurräume"
        ordering = ['available', '-capacity_1_free', '-capacity_2_free', 'room']

    room = models.OneToOneField('ophasebase.Room', verbose_name="Raum", limit_choices_to={"type": "HS"})
    available = models.BooleanField(verbose_name="Verfügbar", default=True)
    capacity_1_free = models.IntegerField(verbose_name="Plätze (1 Platz Abstand)")
    capacity_2_free = models.IntegerField(verbose_name="Plätze (2 Plätze Abstand)")

    def __str__(self):
        return str(self.room)
