from clothing.models import Type, Size, Color, Order, Settings
from django.contrib import admin


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    ordering = ['-price', 'name']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['person', 'type', 'size', 'color', 'additional']
    ordering = ['person', 'type', 'size']
    list_display_links = ['type', 'size', 'color']
    list_filter = ['additional', 'color']

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('clothing_ordering_enabled',)
