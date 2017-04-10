from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models import Q
from django.utils import formats
from django.utils.translation import ugettext_lazy as _


class GroupNotificationFilter(models.Model):
    class Meta:
        ordering = ['group', 'app', 'action']
        verbose_name = _("Benachrichtigungsfilter für Gruppe")
        verbose_name_plural = _("Benachrichtigungsfilter für Gruppen")

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    app = models.CharField(max_length=50, verbose_name=_("Django App Name"))
    action = models.CharField(max_length=100, verbose_name=_("Aktion"), blank=True, default="", help_text=_("Generelle Aktion. Kann leer gelassen werden um alle Benachrichtigungen der APP zu empfangen"))
    digest = models.BooleanField(default=False, blank=True, verbose_name=_("Als Digest verschicken?"))

    def __str__(self):
        if self.action == "":
            return "{}: {}".format(self.group, self.app)
        return "{}: {}.{}".format(self.group, self.app, self.action)

    @classmethod
    def filter_by_groups(cls, groups):
        return cls.objects.filter(group__in=groups)

    @classmethod
    def filter_by_notification(cls, notification):
        return cls.objects.filter(app=notification.app).filter(Q(action=notification.action) | Q(action=""))


class Notification(models.Model):
    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("Benachrichtigung")
        verbose_name_plural = _("Benachrichtigungen")

    app = models.CharField(max_length=50, verbose_name=_("Django App Name"))
    action = models.CharField(max_length=100, verbose_name=_("Aktion"), help_text=_("Generelle Aktion"))
    event = models.TextField(verbose_name=_("Ereignis"), help_text=_("Textuelle Beschreibung des genauen Ereignisses"))
    timestamp = models.DateTimeField(auto_now_add=True)
    detail_url = models.URLField(blank=True, default="", verbose_name=_("Detail URL"))
    icon = models.CharField(max_length=20, blank=True, default="", verbose_name=_("Icon (Font Awesome)"), help_text=_("FA class (ohne fa-)"))
    digest_sent = models.BooleanField(default=False, blank=True, verbose_name=_("Digest gesendet?"), help_text=_("Wurde diese Benachrichtigung bereits als Digest versandt?"))

    def __str__(self):
        return "{}.{} @ {}".format(self.app, self.action, formats.date_format(self.timestamp, 'SHORT_DATETIME_FORMAT'))

    @classmethod
    def filter_by_groups(cls, groups):
        filters = GroupNotificationFilter.filter_by_groups(groups)
        #TODO Insert great filter here
        return cls.objects.filter()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

        # Send notification mails immediately
        subscribed_groups = GroupNotificationFilter.filter_by_notification(self)
        #subscribed_users = User.objects.filter(groups__in=subscribed_groups)
        #print(subscribed_groups)
