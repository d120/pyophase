from django.contrib import admin

from exam.models import ExamRoom


@admin.register(ExamRoom)
class ExamRoomAdmin(admin.ModelAdmin):
    list_display = ['available', 'room', 'capacity_1_free', 'capacity_2_free']
    list_display_links = ['room']
    list_filter = ['available']
