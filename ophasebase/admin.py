from django.contrib import admin

from ophasebase.models import Building, Ophase, Room


@admin.register(Ophase)
class OphaseAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'start_date', 'end_date', 'is_active')


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
        ('Ausstattung', {'fields': ['type', 'capacity', 'has_beamer']}),
        ('Position', {'fields': ['lat', 'lng']})
    ]
