from django.contrib import admin

from staff.models import Person, DressSize, Settings, GroupCategory, OrgaJob, HelperJob, TutorGroup
from staff.admin_actions import mail_export, staff_nametag_export, staff_overview_export, helper_job_overview


admin.site.register(GroupCategory)
admin.site.register(OrgaJob)
admin.site.register(HelperJob)
admin.site.register(DressSize)


class TutorFilter(admin.SimpleListFilter):
    title = "Tutorenstatus"
    parameter_name = "tutorstatus"

    def lookups(self, request, model_admin):
        choices = [('onlytutors', 'Alle Tutoren')]
        for gc in GroupCategory.objects.all():
            choices.append((gc.id, gc.label))
        choices.append(('notutors', 'Keine Tutoren'))
        return choices

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        if self.value() == 'onlytutors':
            return queryset.filter(is_tutor=True)
        if self.value() == 'notutors':
            return queryset.filter(is_tutor=False)
        return queryset.filter(tutor_for__id=self.value())


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    class Media:
        css = {
             'all': ("ophasebase/components/font-awesome/css/font-awesome.min.css",)
        }

    list_display = ['prename', 'name', 'is_tutor', 'is_orga', 'is_helper', 'created_at', 'orga_annotation_status']
    list_filter = [TutorFilter, 'is_orga', 'is_helper']
    list_display_links = ['prename', 'name']
    search_fields = ['prename', 'name']
    readonly_fields = ('created_at', 'updated_at')
    actions = [mail_export, staff_overview_export, staff_nametag_export, helper_job_overview]

    fieldsets = [
        ('Personendaten', {'fields':
            ['ophase', 'prename', 'name', 'email', 'phone', 'dress_size', 'orga_annotation']}),
        ('Bewerbung', {'fields':
            ['matriculated_since', 'degree_course', 'experience_ophase', 'why_participate', 'remarks']}),
        ('In der Ophase', {'fields':
            ['is_tutor', 'tutor_for', 'is_orga', 'orga_jobs', 'is_helper', 'helper_jobs']}),
        ('Sonstiges', {'fields':
            ['created_at', 'updated_at']}),
    ]

    filter_horizontal = ('orga_jobs', 'helper_jobs')

    def orga_annotation_status(self, obj):
        if obj.orga_annotation:
            return "<i class='fa fa-commenting-o'></i>"
        else:
            return ""
    orga_annotation_status.short_description = "Orga-Notiz"
    orga_annotation_status.allow_tags = True


@admin.register(TutorGroup)
class TutorGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_tutors', 'group_category']
    list_filter = ['group_category']

    def get_tutors(self, obj):
        return ", ".join([str(t) for t in obj.tutors.all()])
    get_tutors.short_description = "Tutoren"


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['tutor_registration_enabled', 'orga_registration_enabled', 'helper_registration_enabled']
    list_display_links = ['tutor_registration_enabled', 'orga_registration_enabled', 'helper_registration_enabled']
