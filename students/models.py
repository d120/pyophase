from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ophasebase.models import Ophase
from staff.models import TutorGroup


class Newsletter(models.Model):
    """A newsletter."""

    class Meta:
        verbose_name = _("Newsletter")
        verbose_name_plural = _("Newsletter")
        ordering = ['-active', 'name']

    name = models.CharField(max_length=50, verbose_name=_("Newsletter"))
    description = models.TextField(verbose_name=_("Beschreibung"))
    active = models.BooleanField(default=True, verbose_name=_("Auswählbar"))

    def __str__(self):
        return "%s - %s" % (self.name, self.description)


class Student(models.Model):
    """A student who participates in the Ophase."""
    class Meta:
        verbose_name = _("Erstie")
        verbose_name_plural = _("Ersties")
        ordering = ['tutor_group', 'name', 'prename']

    prename = models.CharField(max_length=50, verbose_name=_('first name'))
    name = models.CharField(max_length=50, verbose_name=_('last name'))
    email = models.EmailField(verbose_name=_("E-Mail-Adresse"), blank=True)
    tutor_group = models.ForeignKey(TutorGroup, models.CASCADE, verbose_name=_("Kleingruppe"))
    want_exam = models.BooleanField(default=False, blank=True, verbose_name=_("Klausur mitschreiben?"), help_text=_("Die Klausur ist eine Simulation einer Uniklausur, um die Unterschiede zwischen einer Schul- und einer Universitätsklausur zu zeigen. Abgefragt werden hauptsächlich Informationen aus der Ophase. Es ist nicht verpflichtend, die Klausur zu bestehen."))
    newsletters = models.ManyToManyField(Newsletter, blank=True, verbose_name=_("Newsletter"), help_text=_("Welche Newsletter willst du abonieren (optional)?"), limit_choices_to={'active': True})
    ophase = models.ForeignKey(Ophase, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s, %s (%s)" % (self.name, self.prename, self.tutor_group)

    def want_newsletter(self):
        return self.newsletters.count() > 0

    def save(self, *args, **kwargs):
        if self.ophase_id is None:
            # set Ophase to current active one. We assume that there is only one active Ophase at the same time!
            self.ophase = Ophase.current()
        super().save(*args, **kwargs)

    @staticmethod
    def get_current(**kwargs):
        return Student.objects.filter(ophase=Ophase.current(), **kwargs)


class Settings(models.Model):
    """Configuration for Students App."""
    class Meta:
        verbose_name = _("Einstellungen")
        verbose_name_plural = _("Einstellungen")

    student_registration_enabled = models.BooleanField(default=False, verbose_name=_("Studenten Registrierung aktiv"))

    def get_name(self):
        return '%s' % _("Students Einstellungen")

    def __str__(self):
        return self.get_name()

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if Settings.objects.count() > 0 and self.id != Settings.objects.get().id:
            raise ValidationError(_("Es ist nur sinnvoll und möglich eine Instanz des Einstellungsobjekts anzulegen."))

    @staticmethod
    def instance():
        try:
            return Settings.objects.get()
        except Settings.DoesNotExist:
            return None
