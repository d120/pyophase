from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _


class GroupSync(models.Model):
    external_group = models.CharField(max_length=100, verbose_name=_("Externer Gruppenname"))
    django_group = models.ForeignKey(Group, verbose_name=_("Django Gruppe"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Gruppensyncronization')
        verbose_name_plural = _('Gruppensyncronizationen')
