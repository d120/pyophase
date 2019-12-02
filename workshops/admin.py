from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html_join, format_html, escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from workshops.admin_actions import oinforz_export, workshop_tutor_list, aushang_export, mail_text_export
from workshops.models import Settings, Workshop, WorkshopSlot, WorkshopAssignment

admin.site.register(WorkshopSlot)


@admin.register(WorkshopAssignment)
class WorkshopAssignmentAdmin(admin.ModelAdmin):
    list_display = ('workshop', 'assigned_slot', 'assigned_room', 'assigned_location')
    class Media:
        js = (
            'workshops/workshop_adm.js',   # app static folder
        )
    def response_change(self, request, obj):
        response = super().response_change(request, obj)
        if (isinstance(response, HttpResponseRedirect) and
                request.GET.get('source') == 'ws_list'):
            response['location'] = reverse('admin:workshops_workshop_changelist')
        return response

    def response_add(self, request, obj):
        response = super().response_change(request, obj)
        if (isinstance(response, HttpResponseRedirect) and
                request.GET.get('source') == 'ws_list'):
            response['location'] = reverse('admin:workshops_workshop_changelist')
        return response


class WorkshopAssignmentInline(admin.TabularInline):
    model = WorkshopAssignment
    extra = 1


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('_title', '_tutor_name', '_created_at', '_possible_slots')
    search_fields = ('title', 'tutor_name', 'tutor_mail')

    actions = (oinforz_export, aushang_export, workshop_tutor_list, mail_text_export)
    inlines = (WorkshopAssignmentInline,)

    def _title(self, item):
        return format_html("{}<br><span style='font-weight:normal;color:grey;' title='Material: {}\nAnmerkungen: {}'><b style='{}'>&nbsp;M&nbsp;</b> <b style='{}'>&nbsp;A&nbsp;</b> {}x | {} {}</span>",
                           item.title,
                           item.equipment,
                           item.remarks,
                           "background:#ffaaff;color:black;" if item.equipment != "" else "color:#dddddd",
                           "background:#aaffaa;color:black;" if item.remarks != "" else "color:#dddddd",
                           item.how_often,
                           (str(item.max_participants)+" TN | ") if item.max_participants>0 else "",
                           item.workshop_type,)
    _title.admin_order_field = 'title'
    _title.short_description = _('Workshoptitel')

    def _tutor_name(self, item):
        return format_html("{}<small style='color:grey'> &lt;{}&gt;</small>", item.tutor_name, item.tutor_mail)
    _tutor_name.admin_order_field = 'tutor_name'
    _tutor_name.short_description = _("Tutor*in")

    def _possible_slots(self, item):
        possible = item.possible_slots.all()
        assigned = item.workshopassignment_set.all()
        slots = dict()
        for slot in possible: slots[slot] = ("grey", None, None, reverse("admin:workshops_workshopassignment_add") + "?source=ws_list&workshop={}&assigned_slot={}".format(item.id, slot.id))
        for info in assigned:
            link = reverse("admin:workshops_workshopassignment_change", args=(info.id,)) + "?source=ws_list"
            location = format_html("<b>{}</b> ({})", info.assigned_room, info.assigned_room.capacity) if info.assigned_room else format_html("<i>{}</i>", info.assigned_location)
            color = "green"
            if info.assigned_room is not None and info.assigned_room.capacity < item.max_participants:
                color = "#ff9900"
            if not info.assigned_slot in slots:
                color = "red"

            slots[info.assigned_slot] = (color, location, info.id, link)

        return mark_safe("<div data-workshop-id='" + str(item.id) + "'>" +
            "".join("<a href='{}' style='color:{}' data-assignment-id='{}' data-slot-id='{}'><u>{:%a} {:%H:%M}</u> <span>{}</span></a><br>".format(link, color, assg_id, slot.id, slot.date, slot.start_time, location)
                                               for (slot, (color, location, assg_id, link)) in slots.items())
                         + "</div>")
    _possible_slots.mark_safe = True
    _possible_slots.short_description = _("Mögliche/Zugewiesene Slots")

    def _created_at(self, item):
        return '{:%a, %d.%m.}'.format(item.created_at)
    _created_at.admin_order_field = 'created_at'
    _created_at.short_description = _("Eingetragen")

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('workshop_submission_enabled', 'orga_email')
