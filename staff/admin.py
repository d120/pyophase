from django.contrib import admin

import staff.models

class PersonAdmin(admin.ModelAdmin):
    list_display = ['prename', 'name', 'is_tutor', 'is_orga', 'is_helper', 'created_at']
    list_filter = ['is_tutor', 'is_orga', 'is_helper']
    list_display_links = ['prename', 'name']
    search_fields = ['prename', 'name']
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = [
        ('Stammdaten', {'fields':
            ['ophase', 'prename', 'name', 'email', 'phone', 'dress_size', 'remarks']}),
        ('Bewerbung', {'fields':
            ['matriculated_since', 'degree_course', 'experience_ophase', 'why_participate']}),
        ('In der Ophase', {'fields':
            ['is_tutor', 'tutor_for', 'is_orga', 'orga_jobs', 'is_helper', 'helper_jobs']}),
        ('Sonstiges', {'fields': ['created_at', 'updated_at']}),
    ]

    filter_horizontal = ('orga_jobs', 'helper_jobs')


class SettingsAdmin(admin.ModelAdmin):
    list_display = ['tutor_registration_enabled', 'orga_registration_enabled', 'helper_registration_enabled']
    list_display_links = ['tutor_registration_enabled', 'orga_registration_enabled', 'helper_registration_enabled']


admin.site.register(staff.models.Person, PersonAdmin)
admin.site.register(staff.models.DressSize)
admin.site.register(staff.models.Settings, SettingsAdmin)
