from django.contrib import admin

# Register your models here.

import exam.models


class ExamRoomAdmin(admin.ModelAdmin):
    list_display = ['available', 'room', 'capacity_1_free', 'capacity_2_free']
    list_display_links = ['room']
    list_filter = ['available']

admin.site.register(exam.models.ExamRoom, ExamRoomAdmin)
