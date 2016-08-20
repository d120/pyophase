from urllib.parse import quote

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from ophasebase.models import Ophase


class GroupCategory(models.Model):
    """Group category like "Bachelor", "Master german", "Master english", ..."""
    class Meta:
        verbose_name = _("Gruppenkategorie")
        verbose_name_plural = _("Gruppenkategorien")
        ordering = ['label']

    label = models.CharField(max_length=50, verbose_name=_('Bezeichnung'))

    def __str__(self):
        return self.label


class Job(models.Model):
    """A job during the Ophase for which persons are needed."""
    class Meta:
        abstract = True

    label = models.CharField(max_length=50, verbose_name=_('Bezeichnung'))
    description = models.TextField(verbose_name=_('Beschreibung'))

    def __str__(self):
        return self.label

class OrgaJob(Job):
    """Job for an organizer."""
    class Meta:
        verbose_name = _("Orgajob")
        verbose_name_plural = _("Orgajobs")
        ordering = ['label']

class HelperJob(Job):
    """Job for a helper."""
    class Meta:
        verbose_name = _("Helferjob")
        verbose_name_plural = _("Helferjobs")
        ordering = ['label']


class DressSize(models.Model):
    """A dress size for a Person"""
    class Meta:
        verbose_name = _("Kleidergröße")
        verbose_name_plural = _("Kleidergrößen")
        unique_together = ("name", "sort_key")
        ordering = ["sort_key"]

    name = models.CharField(max_length=75, verbose_name=_("Kleidergröße"), unique=True)
    sort_key = models.PositiveSmallIntegerField(verbose_name=_("Position in Auflistung"), unique=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    """A person which supports the Ophase."""
    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Personen")
        ordering = ['prename', 'name']
        unique_together = ('ophase', 'email')

    ophase = models.ForeignKey(Ophase, models.CASCADE)
    prename = models.CharField(max_length=60, verbose_name=_('first name'))
    name = models.CharField(max_length=75, verbose_name=_('last name'))
    email = models.EmailField(verbose_name=_("E-Mail-Adresse"), unique=True)
    phone = models.CharField(max_length=30, verbose_name=_("Handynummer"), help_text=_("Deine Handynummer brauchen wir um dich schnell erreichen zu können."))
    matriculated_since = models.CharField(max_length=30, verbose_name=_("An der Uni seit"), help_text=_("Seit wann studierst du an der TU Darmstadt?"))
    degree_course = models.CharField(max_length=50, verbose_name=_("Aktuell angestrebter Abschluss"), help_text=_("Bachelor, Master, Joint Bachelor of Arts, etc."))
    experience_ophase = models.TextField(verbose_name=_("Bisherige Ophasenerfahrung"), help_text=_("Wenn du schonmal bei einer Ophase geholfen hast, schreib uns wann das war und was du gemacht hast."))
    why_participate = models.TextField(verbose_name=_("Warum möchtest du bei der Ophase mitmachen?"))
    is_tutor = models.BooleanField(default=False, verbose_name=_("Tutor"), help_text=_("Möchtest du als Tutor bei der Ophase mitmachen?"))
    is_orga = models.BooleanField(default=False, verbose_name=_("Orga"), help_text=_("Möchtest du als Orga bei der Ophase mitmachen?"))
    is_helper = models.BooleanField(default=False, verbose_name=_("Helfer"), help_text=_("Möchtest du als Helfer bei der Ophase mitmachen?"))
    tutor_for = models.ForeignKey(GroupCategory, models.SET_NULL, blank=True, null=True, verbose_name=_("Tutor für"), help_text=_("Erstsemester welches Studiengangs möchtest du als Tutor betreuen?"))
    orga_jobs = models.ManyToManyField(OrgaJob, blank=True, verbose_name=_("Orgaaufgaben"), help_text=_("Welche Orgaaufgaben kannst du dir vorstellen zu übernehmen?"))
    helper_jobs = models.ManyToManyField(HelperJob, blank=True, verbose_name=_("Helferaufgaben"), help_text=_("Bei welchen Aufgaben kannst du dir vorstellen zu helfen?"))
    dress_size = models.ForeignKey(DressSize, models.SET_NULL, null=True, blank=True, verbose_name=_("Kleidergröße"), help_text=_("Mitwirkende bekommen T-Shirts um sie besser zu erkennen. Damit dein T-Shirt passt brauchen wir deine Größe."))
    remarks = models.TextField(blank=True, verbose_name=_("Anmerkungen"), help_text=_("Was sollten wir noch wissen?"))
    orga_annotation = models.TextField(blank=True, verbose_name=_("Orga-Anmerkungen"), help_text=_("Notizen von Leitung und Orgas."))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Eingetragen am"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Verändert am"))

    def get_name(self):
        return "%s %s" % (self.prename, self.name)
    get_name.short_description = _("Name")
    get_name.admin_order_field = 'prename'

    def get_fillform(self):
        """Return the fillform serialized information of the Person.
        To build a one click registration the full path to the
        staff registration view must be added at the beginning"""

        allowed_keys = ['prename', 'name', 'email', 'phone', 'matriculated_since',
                         'degree_course', 'experience_ophase',
                         'why_participate', 'remarks']

        prefix = '#fillform&v=1'

        user_values = ''
        for key in allowed_keys:
            value = str(getattr(self, key))
            if value:
                user_values += ("&{}={}".format(key, quote(value)))

        return '{}{}'.format(prefix, user_values)

    def __str__(self):
        return self.get_name()

    def save(self, *args, **kwargs):
        if self.ophase_id is None:
            # set Ophase to current active one. We assume that there is only one active Ophase at the same time!
            self.ophase = Ophase.current()
        # ensure tutor flag is set when group is selected
        if self.tutor_for is not None:
            self.is_tutor = True
        super().save(*args, **kwargs)

    @property
    def eligible_for_clothing(self):
        return self.is_orga or self.is_tutor

    @staticmethod
    def get_by_email_address(address):
        try:
            return Person.objects.get(email__iexact=address)
        except Person.DoesNotExist:
            return None


class TutorGroup(models.Model):
    """A group of students guided by tutors."""
    class Meta:
        verbose_name = _("Kleingruppe")
        verbose_name_plural = _("Kleingruppen")
        ordering = ['group_category', 'name']
        unique_together = ('ophase', 'name')

    ophase = models.ForeignKey(Ophase, models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=_("Gruppenname"))
    tutors = models.ManyToManyField(Person, blank=True, verbose_name=_("Tutoren"))
    group_category = models.ForeignKey(GroupCategory, models.CASCADE, verbose_name=_("Gruppenkategorie"))

    def __str__(self):
        return self.name


class Settings(models.Model):
    """Configuration for Staff App."""
    class Meta:
        verbose_name = _("Einstellungen")
        verbose_name_plural = _("Einstellungen")

    tutor_registration_enabled = models.BooleanField(default=False, verbose_name=_("Tutor Registrierung aktiv"))
    orga_registration_enabled = models.BooleanField(default=False, verbose_name=_("Orga Registrierung aktiv"))
    helper_registration_enabled = models.BooleanField(default=False, verbose_name=_("Helfer Registrierung aktiv"))
    group_categories_enabled = models.ManyToManyField(GroupCategory, verbose_name=_("Freigeschaltete Kleingruppenkategorien"))
    orga_jobs_enabled = models.ManyToManyField(OrgaJob, verbose_name=_("Freigeschaltete Orgajobs"))
    helper_jobs_enabled = models.ManyToManyField(HelperJob, verbose_name=_("Freigeschaltete Helferjobs"))

    def get_name(self):
        return '%s' % _("Staff Einstellungen")

    def __str__(self):
        return self.get_name()

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if Settings.objects.count() > 0 and self.id != Settings.objects.get().id:
            raise ValidationError(_("Es ist nur sinnvoll und möglich eine Instanz des Einstellungsobjekts anzulegen."))

    def any_registration_enabled(self):
        """Returns true if any of tutor, orga or helper registration is set to True. Otherwise False"""
        return self.tutor_registration_enabled or self.orga_registration_enabled or self.helper_registration_enabled

    @staticmethod
    def instance():
        try:
            return Settings.objects.get()
        except Settings.DoesNotExist:
            return None
