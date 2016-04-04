from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from oplan.models import Event, RoomOpening

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('kommentar', 'room', 'start_time', 'duration')

@admin.register(RoomOpening)
class RoomOpeningAdmin(admin.ModelAdmin):
    list_display = ('status', 'room', 'start_time', 'duration', 'kommentar')



