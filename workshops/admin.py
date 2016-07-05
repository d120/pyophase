from django.contrib import admin

from workshops.models import WorkshopSlot, Workshop

admin.site.register(WorkshopSlot)

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'tutor_name')
