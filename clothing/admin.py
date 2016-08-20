from clothing.models import Type, Size, Color
from django.contrib import admin


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    ordering = ['-price', 'name']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    ordering = ['-price', 'name']
