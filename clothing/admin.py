from django.contrib import admin

from .models import Color, Order, Settings, Size, Type


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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['person', 'type', 'size', 'color', 'additional']
    ordering = ['person', 'type', 'size']
    list_display_links = ['person', 'type', 'size', 'color']
    list_filter = ['additional', 'color']
    search_fields = ('person__prename', 'person__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('clothing_ordering_enabled',)
