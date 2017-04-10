from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from plan.models import TimeSlot, SlotType, Event
from django.utils.translation import ugettext as _


@admin.register(SlotType)
class SlotTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['name', 'begin', 'end', 'relevant_for', 'link_attendance_list']
    #actions = [update_attendees]

    @staticmethod
    def link_attendance_list(event):
        return format_html('<a href="{url}?event__id__exact={id}">{name}</a>',
                           url=reverse('admin:staff_attendance_changelist'),
                           id=event.pk,
                           name=_('Teilnehmerliste'))


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['timeslot', 'room', 'tutorgroup']
