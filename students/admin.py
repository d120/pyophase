from django.contrib import admin

from students.models import Student, Settings


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'prename', 'tutor_group', 'want_exam', 'want_newsletter']
    list_filter = ['want_exam', 'want_newsletter', 'tutor_group']
    list_display_links = ['name', 'prename']
    search_fields = ['name', 'prename']
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['student_registration_enabled']
