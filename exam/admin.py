from django.contrib import admin

from .models import Assignment, ExamRoom, PersonToExamRoomAssignment


@admin.register(ExamRoom)
class ExamRoomAdmin(admin.ModelAdmin):
    list_display = ['available', 'room', 'capacity_1_free', 'capacity_2_free']
    list_display_links = ['room']
    list_filter = ['available']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'count', 'group_category', 'spacing', 'mode']
    readonly_fields = ['ophase', 'created_at', 'count', 'group_category', 'spacing', 'mode']

@admin.register(PersonToExamRoomAssignment)
class PersonToRoomAssingmentAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'room', 'person']
    readonly_fields = ['assignment', 'room', 'person']
