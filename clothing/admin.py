from django.contrib import admin

from .admin_actions import mark_paid, mark_received, mark_paid_and_received
from .models import Color, Order, Settings, Size, Type
from ophasebase.models import Ophase


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    ordering = ['-price', 'name']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']
    readonly_fields = ('size_sortable',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']


class OphaseOrderFilter(admin.SimpleListFilter):
        """
        A filter to limit the order overview to a specific ophase
        """
        title = 'Ophase'
        parameter_name = 'ophase'

        def lookups(self, request, model_admin):
            """
            Returns a tuple with all ophases
            """
            return ((o, o) for o in Ophase.objects.all())

        def queryset(self, request, queryset):
            if not self.value():
                return queryset
            return queryset.filter(person__ophase=Ophase.objects.get(name=self.value()))


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['person', 'type', 'size', 'color', 'additional']
    ordering = ['person', 'type', 'size']
    list_display_links = ['person', 'type', 'size', 'color']
    list_filter = ['additional', 'color', OphaseOrderFilter]
    search_fields = ('person__prename', 'person__name')
    readonly_fields = ('created_at', 'updated_at')
    actions = [mark_paid, mark_received, mark_paid_and_received]


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('clothing_ordering_enabled',)
