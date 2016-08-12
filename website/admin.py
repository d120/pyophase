from django.contrib import admin
from website.models import Settings


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['helpdesk_phone_number']