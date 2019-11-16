from django.contrib import admin

from .models import GroupSync


@admin.register(GroupSync)
class GroupSyncAdmin(admin.ModelAdmin):
    list_display = ('external_group', 'django_group')
