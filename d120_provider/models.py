from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class GroupSync(models.Model):
    external_group = models.CharField(max_length=100, verbose_name=_("Externer Gruppenname"))
    django_group = models.ForeignKey(Group, verbose_name=_("Django Gruppe"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Gruppen-Synchronization')
        verbose_name_plural = _('Gruppen-Synchronizationen')

    def __str__(self):
        return "{} -> {}".format(self.external_group, self.django_group)
