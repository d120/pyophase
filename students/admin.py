from django.contrib import admin

from students.models import Student, TutorGroup, Settings


@admin.register(TutorGroup)
class TutorGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_tutors', 'group_category']
    list_filter = ['group_category']

    def get_tutors(self, obj):
        return ", ".join([str(t) for t in obj.tutors.all()])
    get_tutors.short_description = "Tutoren"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'prename', 'tutor_group', 'want_exam', 'want_newsletter']
    list_filter = ['want_exam', 'want_newsletter']
    list_display_links = ['name', 'prename']


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['student_registration_enabled']
