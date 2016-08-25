from django.contrib import admin

from workshops.models import WorkshopSlot, Workshop, Settings
from workshops.admin_actions import oinforz_export

admin.site.register(WorkshopSlot)

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'tutor_name', 'created_at')
    search_fields = ('title', 'tutor_name', 'tutor_mail')
    actions = (oinforz_export,)

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('workshop_submission_enabled', 'orga_email')
