from datetime import datetime


def mark_paid(modeladmin, request, queryset):
    queryset.update(paid=True)
mark_paid.short_description = 'Status "Bezahlt" setzen'


def mark_received(modeladmin, request, queryset):
    queryset.update(received_at=datetime.now())
mark_received.short_description = 'Status "Ausgegeben" setzen'


def mark_paid_and_received(modeladmin, request, queryset):
    queryset.update(paid=True, received_at=datetime.now())
mark_paid_and_received.short_description = 'Status "Bezahlt" und "Ausgegeben" setzen'