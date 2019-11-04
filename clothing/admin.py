from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

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
            The first value is the name for the url parameter,
            the second one is the name shown in the sidebar
            """
            return ((o.id, o.name) for o in Ophase.objects.all())

        def queryset(self, request, queryset):
            if not self.value():
                return queryset
            return queryset.filter(person__ophase=Ophase.objects.get(id=self.value()))


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['person', 'type', 'size', 'color', '_additional', '_received']
    ordering = ['person', 'type', 'size']
    list_display_links = ['person', 'type', 'size', 'color']
    list_filter = ['additional', 'color', OphaseOrderFilter]
    search_fields = ('person__prename', 'person__name')
    readonly_fields = ('created_at', 'updated_at')
    actions = [mark_paid, mark_received, mark_paid_and_received]

    def _additional(self, order):
        if order.additional:
            if order.paid:
                return format_html("<span class='fa fa-money-bill-wave'></span> <span class='fa fa-check' title='{}'></span> ", _("Bereits bezahlt"))
            else:
                return format_html("<span class='fa fa-money-bill-wave'></span> <span class='fa fa-exclamation-circle' title='{}'></span> ", _("Noch nicht bezahlt"))
        else:
            return ""
    _additional.admin_order_field = 'additional'

    def _received(self, order):
        if order.received_at:
            return format_html("<span class='fa fa-check' title='{}'></span>", order.received_at)
        else:
            return format_html("<span class='fa fa-times' title='{}'></span>", order.received_at)
    _received.admin_order_field = 'received_at'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['count_orders'] = Order.get_current().count()
        extra_context['count_orders_free'] = Order.get_current().filter(additional=False).count()
        extra_context['count_orders_paid'] = extra_context['count_orders'] - extra_context['count_orders_free']
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('clothing_ordering_enabled',)
