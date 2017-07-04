from staff.models import Attendance
from django.utils.translation import ugettext as _


def update_attendees(modeladmin, request, queryset):
    for event in queryset:
        existing_pesons = event.attendance_set.values("person")
        relevant_for_queryset = event.relevant_for.get_filtered_staff()
        new_attendees = relevant_for_queryset.exclude(pk__in=existing_pesons)

        Attendance.objects.bulk_create([Attendance(event=event, person=person, status='x') for person in new_attendees])
    modeladmin.message_user(request, _("Teilnehmerliste aktualisiert."))
update_attendees.short_description = _("Liste der Teilnehmer aktualisieren (anhand des Zielgruppenfilters)")
