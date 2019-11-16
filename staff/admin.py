from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import _boolean_icon
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext as _

from ophasebase.models import OphaseCategory
from .admin_actions import (
    mail_export,
    send_fillform_mail,
    staff_nametag_export,
    staff_overview_export,
    tutorgroup_export,
    update_attendees, mark_attendance_x, mark_attendance_a, mark_attendance_e, mark_phoned_x, mark_phoned_e,
    mark_phoned_n, mark_attendance_v, generate_orga_cert)
from .models import (
    HelperJob,
    OrgaJob,
    Person,
    Settings,
    TutorGroup,
    StaffFilterGroup,
    Attendance,
    AttendanceEvent,
    OrgaSelectedJob, HelperSelectedJob)


@admin.register(OrgaJob)
@admin.register(HelperJob)
class LabelSortAdmin(admin.ModelAdmin):
    """Simple ModelAdmin which just shows the field Value in the list view"""
    list_display = ['label']


class TutorFilter(admin.SimpleListFilter):
    title = _('Tutorenstatus')
    parameter_name = "tutorstatus"

    def lookups(self, request, model_admin):
        choices = [('onlytutors', _('Alle Tutoren'))]
        for gc in OphaseCategory.objects.all():
            choices.append((gc.id, gc.name))
        choices.append(('notutors', _('Keine Tutoren')))
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
             'all': ("vendor/font-awesome/css/font-awesome.min.css",)
        }

    list_display = ['prename', 'name', 'is_tutor_with_title', 'is_orga', 'is_helper', 'created_at', 'orga_annotation_status']
    list_filter = [ ("ophase", admin.RelatedOnlyFieldListFilter), TutorFilter, 'is_orga', 'is_helper']
    list_display_links = ['prename', 'name']
    search_fields = ['prename', 'name', 'phone']
    readonly_fields = ('created_at', 'updated_at')
    actions = [mail_export, staff_overview_export, staff_nametag_export, send_fillform_mail, generate_orga_cert]

    fieldsets = [
        (_('Personendaten'), {'fields':
            ['ophase', 'prename', 'name', 'email', 'user', 'tuid', 'phone', 'orga_annotation']}),
        (_('Bewerbung'), {'fields':
            ['matriculated_since', 'degree_course', 'experience_ophase', 'why_participate', 'remarks']}),
        (_('In der Ophase'), {'fields':
            ['is_tutor', 'tutor_for', 'tutor_experience', 'is_orga', 'is_helper']}),
        (_('Sonstiges'), {'fields':
            ['created_at', 'updated_at']}),
        (_('Namensschild'), {'fields':
                ['nametag_shortname', 'nametag_long'],
                'classes': ('collapse',),
                'description': _('Optionale Einträge für das Namensschild')}),
    ]

    filter_horizontal = ('orga_jobs', 'helper_jobs')

    def orga_annotation_status(self, obj):
        if obj.orga_annotation:
            return format_html('<i class="fa fa-commenting-o" title="{}"></i>', obj.orga_annotation)
        else:
            return ""
    orga_annotation_status.short_description = _('Orga-Notiz')

    def is_tutor_with_title(self, obj):
        """If the person is a tutor the tutor_for tag is set as image title"""
        if obj.is_tutor == True and obj.tutor_for is not None:
            icon_url = static('admin/img/icon-yes.svg')
            return format_html('<img src="{}" alt="{}" title="{}" /> {}',
                               icon_url, obj.is_tutor, obj.tutor_for.name, obj.tutor_for.name)
        else:
            return _boolean_icon(obj.is_tutor)

    is_tutor_with_title.short_description = _('Tutor')
    is_tutor_with_title.admin_order_field = 'tutor_for__name'


@admin.register(OrgaSelectedJob)
class OrgaSelectedJobAdmin(admin.ModelAdmin):
    list_display = ('job', 'status', 'person')
    list_filter = ('job',)


@admin.register(HelperSelectedJob)
class HelperelectedJobAdmin(admin.ModelAdmin):
    list_display = ('job', 'status', 'person')
    list_filter = ('job',)


@admin.register(StaffFilterGroup)
class StaffFilterGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_tutor', 'is_orga', 'is_helper']


@admin.register(TutorGroup)
class TutorGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_tutors', 'ophase', 'group_category']
    list_filter = ['ophase', 'group_category']
    actions = [tutorgroup_export]

    def get_tutors(self, obj):
        return ", ".join([str(t) for t in obj.tutors.all()])
    get_tutors.short_description = _('Tutoren')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['link_person', 'status', 'phone_status', 'comment', 'event']
    list_filter = ['event', 'status']
    list_display_links = ['status', 'phone_status']
    actions = [mark_attendance_a, mark_attendance_v, mark_attendance_e, mark_attendance_x, mark_phoned_x, mark_phoned_e, mark_phoned_n]

    @staticmethod
    def link_person(event):
        return format_html('<a href="{url}">{name}</a>',
                           url=reverse('admin:staff_person_change',  args=(event.person.id, )),
                           name=event.person)

    @staticmethod
    def person_phone(event):
        return event.person.phone


@admin.register(AttendanceEvent)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['name', 'begin', 'end', 'required_for', 'link_attendance_list']
    actions = [update_attendees]

    @staticmethod
    def link_attendance_list(event):
        return format_html('<a href="{url}?event__id__exact={id}">{name}</a>',
                           url=reverse('admin:staff_attendance_changelist'),
                           id=event.pk,
                           name=_('Teilnehmerliste'))


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['tutor_registration_enabled', 'orga_registration_enabled', 'helper_registration_enabled']
    list_display_links = ['tutor_registration_enabled', 'orga_registration_enabled', 'helper_registration_enabled']
