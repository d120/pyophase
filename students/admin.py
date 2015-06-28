from django.contrib import admin

from students.models import Student, TutorGroup, Settings


@admin.register(TutorGroup)
class TutorGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_tutors', 'groupCategory']
    list_filter = ['groupCategory']

    def get_tutors(self, obj):
        return ", ".join([str(t) for t in obj.tutors.all()])
    get_tutors.short_description = "Tutoren"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'prename', 'tutorGroup', 'wantExam', 'wantNewsletter']
    list_filter = ['wantExam', 'wantNewsletter']
    list_display_links = ['name', 'prename']


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['student_registration_enabled']
