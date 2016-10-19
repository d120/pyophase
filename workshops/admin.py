from django.contrib import admin

from workshops.admin_actions import oinforz_export, workshop_tutor_list
from workshops.models import Settings, Workshop, WorkshopSlot


admin.site.register(WorkshopSlot)

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'tutor_name', 'created_at')
    search_fields = ('title', 'tutor_name', 'tutor_mail')
    actions = (oinforz_export, workshop_tutor_list)

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('workshop_submission_enabled', 'orga_email')
