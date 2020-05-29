from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Assignment, ExamRoom, PersonToExamRoomAssignment


@admin.register(ExamRoom)
class ExamRoomAdmin(admin.ModelAdmin):
    list_display = ['available', 'room', 'capacity_1_free', 'capacity_2_free']
    list_display_links = ['room']
    list_filter = ['available']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'count', 'group_category', 'spacing', 'mode', '_export']
    readonly_fields = ['ophase', 'created_at', 'count', 'group_category', 'spacing', 'mode']

    def _export(self, item):
        return format_html('<a href="{}">Raumzuteilung exportieren</a>', reverse('dashboard:exam:assignment_name_list', args=(item.pk,)))

@admin.register(PersonToExamRoomAssignment)
class PersonToRoomAssingmentAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'room', 'person']
    readonly_fields = ['assignment', 'room', 'person']
