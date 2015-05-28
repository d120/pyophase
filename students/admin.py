from django.contrib import admin

import students.models


class TutorGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_tutors', 'groupCategory']
    list_filter = ['groupCategory']

    def get_tutors(self, obj):
        return ", ".join([str(t) for t in obj.tutors.all()])

    get_tutors.short_description = "Tutoren"


class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'prename', 'tutorGroup', 'wantExam', 'wantNewsletter']
    list_filter = ['wantExam', 'wantNewsletter']
    list_display_links = ['name', 'prename']


class SettingsAdmin(admin.ModelAdmin):
    list_display = ['student_registration_enabled']


admin.site.register(students.models.Student, StudentAdmin)
admin.site.register(students.models.TutorGroup, TutorGroupAdmin)
admin.site.register(students.models.Settings, SettingsAdmin)
