from django.contrib import admin

from ophasebase.models import Building, GroupCategory, OrgaJob, HelperJob, Ophase, Room


admin.site.register(GroupCategory)
admin.site.register(OrgaJob)
admin.site.register(HelperJob)


@admin.register(Ophase)
class OphaseAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'start_date', 'end_date', 'is_active')


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'label')
    list_filter = ['area', 'subarea']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'type', 'capacity', 'hasBeamer')
    list_filter = ['building', 'type', 'hasBeamer']

    fieldsets = [
        (None, {'fields': ['building', 'number']}),
        ('Ausstattung', {'fields': ['type', 'capacity', 'hasBeamer']}),
        ('Position', {'fields': ['lat', 'lng']})
    ]
