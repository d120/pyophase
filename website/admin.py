from django.contrib import admin

from .models import Settings, OInforz, CategoryDetails


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['helpdesk_phone_number', 'vorkurs_start_date', 'vorkurs_end_date']


@admin.register(CategoryDetails)
class CategoryDetailsAdmin(admin.ModelAdmin):
    list_display = ['category']


@admin.register(OInforz)
class OInforzAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_modified']
