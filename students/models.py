from django.db import models
from django.core.exceptions import ValidationError

from ophasebase.models import Ophase
from staff.models import TutorGroup


class Newsletter(models.Model):
    """A newsletter."""

    class Meta:
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletter"
        ordering = ['-active', 'name']

    name = models.CharField(max_length=50, verbose_name="Newsletter")
    description = models.TextField(verbose_name="Beschreibung")
    active = models.BooleanField(default=True, verbose_name="Auswählbar")

    def __str__(self):
        return "%s - %s" % (self.name, self.description)


class Student(models.Model):
    """A student who participates in the Ophase."""
    class Meta:
        verbose_name = "Erstie"
        verbose_name_plural = "Ersties"
        ordering = ['tutor_group', 'name', 'prename']

    prename = models.CharField(max_length=50, verbose_name="Vorname")
    name = models.CharField(max_length=50, verbose_name="Name")
    email = models.EmailField(verbose_name="E-Mail-Adresse", blank=True)
    tutor_group = models.ForeignKey(TutorGroup, verbose_name="Kleingruppe")
    want_exam = models.BooleanField(default=False, blank=True, verbose_name="Klausur mitschreiben?")
    newsletters = models.ManyToManyField(Newsletter, blank=True, verbose_name="Newsletter", help_text="Welche Newsletter willst du abonieren (optional)?", limit_choices_to={'active': True})
    ophase = models.ForeignKey(Ophase)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s, %s (%s)" % (self.name, self.prename, self.tutor_group)

    def want_newsletter(self):
        print(self.newsletters.count())
        return self.newsletters.count() > 0

    def save(self, *args, **kwargs):
        if self.ophase_id is None:
            # set Ophase to current active one. We assume that there is only one active Ophase at the same time!
            self.ophase = Ophase.current()
        super(Student, self).save(*args, **kwargs)


class Settings(models.Model):
    """Configuration for Students App."""
    class Meta:
        verbose_name = "Einstellungen"
        verbose_name_plural = "Einstellungen"

    student_registration_enabled = models.BooleanField(default=False, verbose_name="Klausuranmeldung aktiv")

    def get_name(self):
        return "Students Einstellungen"

    def __str__(self):
        return self.get_name()

    def clean(self, *args, **kwargs):
        super(Settings, self).clean(*args, **kwargs)
        if Settings.objects.count() > 0 and self.id != Settings.objects.get().id:
            raise ValidationError("Es ist nur sinnvoll und möglich eine Instanz des Einstellungsobjekts anzulegen.")

    @staticmethod
    def instance():
        try:
            return Settings.objects.get()
        except Settings.DoesNotExist:
            return None
