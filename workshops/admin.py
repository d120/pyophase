from django.contrib import admin

from workshops.models import WorkshopSlot, Workshop, Settings

admin.site.register(WorkshopSlot)

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'tutor_name', 'created_at')

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['workshop_submission_enabled', 'orga_email']
