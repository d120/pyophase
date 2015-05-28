from django.db import models
from django.core.exceptions import ValidationError

from ophasebase.models import Ophase

class TutorGroup(models.Model):
    """A group of students guided by tutors."""
    class Meta:
        verbose_name = "Kleingruppe"
        verbose_name_plural = "Kleingruppen"
        ordering = ['groupCategory', 'name']

    name = models.CharField(max_length=50, verbose_name="Gruppenname")
    tutors = models.ManyToManyField('staff.Person', verbose_name="Tutoren")
    groupCategory = models.ForeignKey('ophasebase.GroupCategory', verbose_name="Gruppenkategorie")

    def __str__(self):
        return self.name


class Student(models.Model):
    """A student who participates in the Ophase."""
    class Meta:
        verbose_name = "Erstie"
        verbose_name_plural = "Ersties"
        ordering = ['tutorGroup', 'name', 'prename']

    prename = models.CharField(max_length=50, verbose_name="Vorname")
    name = models.CharField(max_length=50, verbose_name="Name")
    email = models.EmailField(verbose_name="E-Mail-Adresse", blank=True)
    tutorGroup = models.ForeignKey(TutorGroup, verbose_name="Kleingruppe")
    wantExam = models.BooleanField(default=False, blank=True, verbose_name="Klausur mitschreiben?")
    wantNewsletter = models.BooleanField(default=False, blank=True, verbose_name="Newsletter abonnieren?")
    ophase = models.ForeignKey(Ophase)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s (%s)" % (self.prename, self.name, self.tutorGroup)

    def clean(self, *args, **kwargs):
        super(Student, self).clean(*args, **kwargs)
        if self.wantNewsletter and self.email == '':
            raise ValidationError({'email': 'Um den Newsletter zu abonnieren muss eine E-Mail-Adresse angegeben werden.'})

    def save(self, *args, **kwargs):
        if not self.wantNewsletter:
            self.email = '' # remove mail address when unnecessary
        if self.ophase_id is None:
            # set Ophase to current active one. We assume that there is only one active Ophase at the same time!
            self.ophase = Ophase.objects.get(is_active=True)
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
