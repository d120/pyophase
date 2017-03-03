from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Building, Ophase, Room, OphaseCategory, OphaseActiveCategory, GroupNotificationFilter, Notification


@admin.register(Ophase)
class OphaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'label')
    list_filter = ['area', 'subarea']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'type', 'capacity', 'has_beamer')
    list_filter = ['building', 'type', 'has_beamer']

    fieldsets = [
        (None, {'fields': ['building', 'number']}),
        (_('Ausstattung'), {'fields': ['type', 'capacity', 'has_beamer']}),
        (_('Position'), {'fields': ['lat', 'lng']})
    ]


@admin.register(OphaseCategory)
class OphaseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority')


@admin.register(OphaseActiveCategory)
class OphaseActiveCategoryAdmin(admin.ModelAdmin):
    list_display = ('ophase', 'category', 'start_date', 'end_date')
    list_display_links = ('ophase', 'category')


@admin.register(GroupNotificationFilter)
class GroupNotificationFilterAdmin(admin.ModelAdmin):
    list_display = ('group', 'app', 'action')
    list_display_links = ('app', 'action')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('app', 'action', 'timestamp')
    list_display_links = ('app', 'action')
