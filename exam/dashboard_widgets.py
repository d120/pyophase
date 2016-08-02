from django.urls import reverse_lazy
from django.utils import formats
from django.utils.translation import ugettext_lazy as _

from dashboard.components import TemplateWidgetComponent
from exam.models import Assignment
from ophasebase.models import Ophase
from students.models import Student


class ExamWidget(TemplateWidgetComponent):
    """
    This widgets allows to see if there is a valid assignment at a glance
    """

    permissions = ['exam.add_assignment']
    name = _("Klausurzuteilung")
    link_target = reverse_lazy('dashboard:exam:assignment')
    template_name = "exam/dashboard/widget_exam.html"

    def _get_latest_assignment(self):
        return Assignment.objects.latest()

    def _correct_count(self, assignment):
        return assignment.count == Student.get_current(want_exam=True, tutor_group__group_category=assignment.group_category).count()

    def get_context_data(self):
        context = super().get_context_data()

        current_ophase = Ophase.current()
        assignment = self._get_latest_assignment()

        if current_ophase is None:
            context['message'] = _("Keine Ophase, keine Zuteilung")
            context['status_icon'] = "ok"
            context['submessage'] = ""
        elif assignment is None:
            context['message'] = _("Noch keine gültige Zuteilung")
            context['status_icon'] = "remove"
            context['submessage'] = ""
        elif self._correct_count(assignment):
            context['message'] = _("Gültige Zuteilung")
            context['status_icon'] = "ok"
            formatted_datetime = formats.date_format(assignment.created_at, 'SHORT_DATETIME_FORMAT')
            context['submessage'] = _('Erstellt am %(formated_datetime)s') % {
                     'formated_datetime' : formatted_datetime,}
        else:
            context['message'] = _("Achtung: Zuteilung ist ungültig")
            context['status_icon'] = "remove"
            context['submessage'] = ""

        return context

    def get_status(self):
        current_ophase = Ophase.current()
        if current_ophase is None:
            return "default"

        assignment = self._get_latest_assignment()
        if assignment is None:
            return "warning"

        if self._correct_count(assignment):
            return "success"
        return "danger"
