from urllib.parse import quote

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from ophasebase.models import Ophase, Room, OphaseCategory


class Job(models.Model):
    """A job during the Ophase for which persons are needed."""
    class Meta:
        abstract = True

    label = models.CharField(max_length=50, verbose_name=_('Bezeichnung'))
    description = models.TextField(verbose_name=_('Beschreibung'))
    categories = models.ManyToManyField(OphaseCategory, verbose_name=_("Kategorie(n) zu der/den der Job gehört"), blank=True)

    @classmethod
    def filter_jobs_for_ophase(cls, ophase):
        """
        Find all jobs relevant for the given ophase
        All jobs with either no category or at least one matching category will be returned
        :param ophase: ophase to find jobs for
        :return: object manager of all matching jobs
        """
        return cls.objects.filter(Q(categories=None) | Q(categories__in=ophase.categories.all())).distinct()

    @classmethod
    def filter_jobs_for_ophase_current(cls):
        """
        Find all jobs relevant for the current ophase
        All jobs with either no category or at least one matching category will be returned
        :return: object manager of all matching jobs
        """
        return cls.filter_jobs_for_ophase(Ophase.current())

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


class SelectedJob(models.Model):
    class Meta:
        abstract = True
    person = models.ForeignKey("Person", verbose_name=_("Person"), on_delete=models.CASCADE)
    comment = models.TextField(verbose_name=_("Kommentar"), blank=True)


class OrgaSelectedJob(SelectedJob):
    class Meta:
        verbose_name = _("Gewählter Orgajob")
        verbose_name_plural = _("Gewählte Orgajobs")
        ordering = ['job', 'status', 'person']

    STATUS_CHOICES = (
        ("i", _("Interessiert")),
        ("o", _("Orga")),
        ("c", _("Co-Orga")),
        ("n", _("Nicht eingeteilt")),
    )

    job = models.ForeignKey("OrgaJob", verbose_name=_("Job"), on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="i", verbose_name=_('Status'))

    def __str__(self):
        return "{} - {}: {}".format(str(self.person), str(self.job), self.get_status_display())


class HelperSelectedJob(SelectedJob):
    class Meta:
        verbose_name = _("Gewählter Helferjob")
        verbose_name_plural = _("Gewählte Helferjobs")
        ordering = ['job', 'status', 'person']

    STATUS_CHOICES = (
        ("i", _("Interessiert")),
        ("e", _("Eingeteilt")),
        ("n", _("Nicht eingeteilt")),
    )

    job = models.ForeignKey("HelperJob", verbose_name=_("Job"), on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="i", verbose_name=_('Status'))

    def __str__(self):
        return "{} - {}: {}".format(str(self.person), str(self.job), self.get_status_display())


class Person(models.Model):
    """A person which supports the Ophase."""
    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Personen")
        ordering = ['prename', 'name']
        unique_together = (('ophase', 'email'), ('ophase', 'tuid'),)

    ophase = models.ForeignKey(Ophase, models.CASCADE)
    tuid = models.ForeignKey('pyTUID.TUIDUser', on_delete=models.CASCADE, verbose_name=_("TUID User"), null=True)
    prename = models.CharField(max_length=60, verbose_name=_('first name'))
    name = models.CharField(max_length=75, verbose_name=_('last name'))
    email = models.EmailField(max_length=150, verbose_name=_("E-Mail-Adresse"))
    phone = models.CharField(max_length=30, verbose_name=_("Handynummer"), help_text=_("Deine Handynummer brauchen wir um dich schnell erreichen zu können."))
    matriculated_since = models.CharField(max_length=30, verbose_name=_("An der Uni seit"), help_text=_("Seit wann studierst du an der TU Darmstadt?"))
    degree_course = models.CharField(max_length=50, verbose_name=_("Aktuell angestrebter Abschluss"), help_text=_("Bachelor, Master, Joint Bachelor of Arts, etc."))
    experience_ophase = models.TextField(verbose_name=_("Bisherige Ophasenerfahrung"), help_text=_("Wenn du schonmal bei einer Ophase geholfen hast, schreib uns wann das war und was du gemacht hast."))
    why_participate = models.TextField(verbose_name=_("Warum möchtest du bei der Ophase mitmachen?"))
    is_tutor = models.BooleanField(default=False, verbose_name=_("Tutor"), help_text=_("Möchtest du als Tutor bei der Ophase mitmachen?"))
    is_orga = models.BooleanField(default=False, verbose_name=_("Orga"), help_text=_("Möchtest du als Orga bei der Ophase mitmachen?"))
    is_helper = models.BooleanField(default=False, verbose_name=_("Helfer"), help_text=_("Möchtest du als Helfer bei der Ophase mitmachen?"))
    tutor_for = models.ForeignKey(OphaseCategory, models.SET_NULL, blank=True, null=True, verbose_name=_("Tutor für"), help_text=_("Erstsemester welches Studiengangs möchtest du als Tutor betreuen?"))
    tutor_experience = models.PositiveSmallIntegerField(verbose_name=_("Anzahl Tutorentätigkeiten"), help_text=_("Wie oft warst du bereits Ophasentutor"), default=0, blank=True)
    orga_jobs = models.ManyToManyField(OrgaJob, blank=True, verbose_name=_("Orgaaufgaben"), help_text=_("Welche Orgaaufgaben kannst du dir vorstellen zu übernehmen?"), through="OrgaSelectedJob", related_name=u'person_orgajobs')
    helper_jobs = models.ManyToManyField(HelperJob, blank=True, verbose_name=_("Helferaufgaben"), help_text=_("Bei welchen Aufgaben kannst du dir vorstellen zu helfen?"), through="HelperSelectedJob", related_name=u'person_helperjobs')
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
    def get_current(**kwargs):
        return Person.objects.filter(ophase=Ophase.current(), **kwargs)

    @staticmethod
    def get_by_email_address(address, ophase):
        try:
            return Person.objects.get(email__iexact=address, ophase=ophase)
        except Person.DoesNotExist:
            return None

    @staticmethod
    def get_by_email_address_current(address):
        return Person.get_by_email_address(address, Ophase.current())

    @staticmethod
    def get_by_TUID(TUIDUser):
        return TUIDUser.person_set.filter(ophase=Ophase.current()).first() if TUIDUser is not None else None


class StaffFilterGroup(models.Model):
    """An abstraction mechanism to reference a complicated filter on persons."""
    class Meta:
        verbose_name = _("Staff Filtergruppe")
        verbose_name_plural = _("Staff Filtergruppen")
        ordering = ['name']

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    is_orga = models.BooleanField(default=False, verbose_name=_("Orga?"), help_text=_("Soll der Filter auf Orgas zutreffen"))
    is_helper = models.BooleanField(default=False, verbose_name=_("Helfer?"), help_text=_("Soll der Filter auf Helfer zutreffen"))
    tutor_for_all = models.BooleanField(default=False, verbose_name=_("Alle Tutorenkategorien?"), help_text=_("Soll der Filter auf alle Tutorengruppen zutreffen (sonst spezifizieren)."))
    tutor_for = models.ManyToManyField(OphaseCategory, blank=True, verbose_name=_("Tutor für"), help_text=_("Welche Tutorengruppen sollen einbezogen werden?"))

    def __str__(self):
        return self.name

    @property
    def is_tutor(self):
        return self.tutor_for_all or self.tutor_for.count() > 0

    def get_filtered_staff(self):
        queryset = Person.objects.none()

        if self.is_tutor:
            if self.tutor_for_all:
                queryset = queryset | Person.objects.filter(is_tutor=True, tutor_for__isnull=False)
            else:
                queryset = queryset | Person.objects.filter(is_tutor=True, tutor_for__in=self.tutor_for.all())
        if self.is_orga:
            queryset = queryset | Person.objects.filter(is_orga=True)
        if self.is_helper:
            queryset = queryset | Person.objects.filter(is_helper=True)

        return queryset


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
    group_category = models.ForeignKey(OphaseCategory, models.CASCADE, verbose_name=_("Gruppenkategorie"))

    def __str__(self):
        return self.name


class Attendance(models.Model):
    """Attendance of a person at an attendance event"""
    class Meta:
        verbose_name = _("Anwesenheit")
        verbose_name_plural = _("Anwesenheiten")
        ordering = ['event', 'person']
        unique_together = ('event', 'person')

    STATUS_CHOICES = (
        ("x", _("Nicht anwesend")),
        ("a", _("Anwesend")),
        ("v", _("Anwesend, verspätet")),
        ("e", _("Entschuldigt"))
    )

    PHONECALL_CHOICES = (
        ("x", _("nicht angerufen")),
        ("n", _("angerufen + nicht erreicht")),
        ("e", _("angerufen + erreicht"))
    )

    event = models.ForeignKey("AttendanceEvent", on_delete=models.CASCADE, verbose_name=_("Anwesenheitstermin"))
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name=_("Person"))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="x", verbose_name=_('Status'))
    phone_status = models.CharField(max_length=1, choices=PHONECALL_CHOICES, default="x", verbose_name=_('Telefoniestatus'))
    comment = models.TextField(verbose_name=_("Kommentar"), blank=True)

    def __str__(self):
        return "{} @ {}: {} ({})".format(self.person, self.event, self.get_status_display(), self.get_phone_status_display())


class AttendanceEvent(models.Model):
    """An attendance event"""
    class Meta:
        verbose_name = _("Anwesenheitstermin")
        verbose_name_plural = _("Anwesenheitstermine")
        ordering = ['begin']

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    begin = models.DateTimeField(verbose_name=_("Beginn"))
    end = models.DateTimeField(verbose_name=_("Ende"))
    required_for = models.ForeignKey(StaffFilterGroup, verbose_name=_("Filterkriterium: Wer muss anwesend sein?"), null=True, on_delete=models.SET_NULL)
    ophase = models.ForeignKey(Ophase, models.CASCADE)
    room = models.ForeignKey(Room, null=True, verbose_name=_("Raum"), blank=True, on_delete=models.SET_NULL)

    @staticmethod
    def get_current_events(**kwargs):
        return AttendanceEvent.objects.filter(ophase=Ophase.current(), **kwargs)

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
    group_categories_enabled = models.ManyToManyField(OphaseCategory, verbose_name=_("Freigeschaltete Kleingruppenkategorien"))
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
