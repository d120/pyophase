from django.db import models
from django.core.exceptions import ValidationError

from ophasebase.models import Ophase, GroupCategory, OrgaJob, HelperJob

class DressSize(models.Model):
    """A dress size for a Person"""
    class Meta:
        verbose_name = "Kleidergröße"
        verbose_name_plural = "Kleidergrößen"
        unique_together = ("name", "sort_key")
        ordering = ["sort_key"]

    name = models.CharField(max_length=75, verbose_name="Kleidergröße", unique=True)
    sort_key =  models.PositiveSmallIntegerField(verbose_name="Position in Auflistung", unique=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    """A person which supports the Ophase."""
    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Personen"
        ordering = ['prename', 'name']
        unique_together = ('ophase', 'prename', 'name', 'email')

    ophase = models.ForeignKey(Ophase)
    prename = models.CharField(max_length=60, verbose_name="Vorname")
    name = models.CharField(max_length=75, verbose_name="Name")
    email = models.EmailField(verbose_name="E-Mail-Adresse")
    phone = models.CharField(max_length=30, verbose_name="Handynummer", help_text="Deine Handynummer brauchen wir um dich schnell erreichen zu können.")
    matriculated_since = models.CharField(max_length=30, verbose_name="An der Uni seit", help_text="Seit wann studierst du an der TU Darmstadt?")
    degree_course = models.CharField(max_length=50, verbose_name="Aktuell angestrebter Abschluss", help_text="Bachelor, Master, Joint Bachelor of Arts, etc.")
    experience_ophase = models.TextField(verbose_name="Bisherige Ophasenerfahrung", help_text="Wenn du schonmal bei einer Ophase geholfen hast, schreib uns wann das war und was du gemacht hast.")
    why_participate = models.TextField(verbose_name="Warum möchtest du bei der Ophase mitmachen? ")
    is_tutor = models.BooleanField(default=False, verbose_name="Tutor", help_text="Möchtest du als Tutor bei der Ophase mitmachen?")
    is_orga = models.BooleanField(default=False, verbose_name="Orga", help_text="Möchtest du als Orga bei der Ophase mitmachen?")
    is_helper = models.BooleanField(default=False, verbose_name="Helfer", help_text="Möchtest du als Helfer bei der Ophase mitmachen?")
    tutor_for = models.ForeignKey(GroupCategory, blank=True, null=True, verbose_name="Tutor für", help_text="Erstsemester welches Studiengangs möchtest du als Tutor betreuen?")
    orga_jobs = models.ManyToManyField(OrgaJob, blank=True, verbose_name="Orgaaufgaben", help_text="Welche Orgaaufgaben kannst du dir vorstellen zu übernehmen?")
    helper_jobs = models.ManyToManyField(HelperJob, blank=True, verbose_name="Helferaufgaben", help_text="Bei welchen Aufgaben kannst du dir vorstellen zu helfen?")
    dress_size = models.ForeignKey(DressSize, null=True, blank=True, verbose_name = "Kleidergröße", help_text="Mitwirkende bekommen T-Shirts um sie besser zu erkennen. Damit dein T-Shirt passt brauchen wir deine Größe.")
    remarks = models.TextField(blank=True, verbose_name="Anmerkungen",  help_text="Was sollten wir noch wissen?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eingetragen am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Verändert am")

    def get_name(self):
        return "%s %s" % (self.prename, self.name)
    get_name.short_description = "Name"
    get_name.admin_order_field = 'prename'

    def __str__(self):
        return self.get_name()

    def save(self, *args, **kwargs):
        if self.ophase_id is None:
            # set Ophase to current active one. We assume that there is only one active Ophase at the same time!
            self.ophase = Ophase.objects.get(is_active=True)
        super(Person, self).save(*args, **kwargs)


class Settings(models.Model):
    """Configuration for Staff App."""
    class Meta:
        verbose_name = "Einstellungen"
        verbose_name_plural = "Einstellungen"

    tutor_registration_enabled = models.BooleanField(default=False, verbose_name="Tutor Registrierung aktiv")
    orga_registration_enabled = models.BooleanField(default=False, verbose_name="Orga Registrierung aktiv")
    helper_registration_enabled = models.BooleanField(default=False, verbose_name="Helfer Registrierung aktiv")

    def get_name(self):
        return "Staff Einstellungen"

    def __str__(self):
        return self.get_name()

    def clean(self, *args, **kwargs):
        super(Settings, self).clean(*args, **kwargs)
        if Settings.objects.count() > 0 and self.id != Settings.objects.get().id:
            raise ValidationError("Es ist nur sinnvoll und möglich eine Instanz des Einstellungsobjekts anzulegen.")
