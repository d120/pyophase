from django.contrib import admin

from students.admin_actions import generate_part_cert
from .models import Newsletter, Settings, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'prename', 'tutor_group', 'want_exam']
    list_filter = ['want_exam', 'tutor_group']
    list_display_links = ['name', 'prename']
    search_fields = ['name', 'prename']
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ['newsletters']
    actions = [generate_part_cert]


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['active', 'name']
    list_filter = ['active']
    list_display_links = ['name']


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['student_registration_enabled']
