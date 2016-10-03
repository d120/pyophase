from django.contrib import admin

from .models import Schedule, Settings, OInforz


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['helpdesk_phone_number', 'vorkurs_start_date', 'vorkurs_end_date']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['degree', 'stand']


@admin.register(OInforz)
class OInforzAdmin(admin.ModelAdmin):
    list_display = ['degree', 'stand']
