from django.core.urlresolvers import reverse_lazy
from dashboard.components import TemplateWidgetComponent
from exam.models import Assignment
from ophasebase.models import Ophase
from students.models import Student


class ExamWidget(TemplateWidgetComponent):
    """
    This widgets allows to see if there is a valid assignment at a glance
    """

    permissions = ['exam.add_assignment']
    name = "Klausurzuteilung"
    link_target = reverse_lazy('dashboard:exam:assignment')
    template_name = "exam/dashboard/widget_exam.html"

    def _get_latest_assignment(self):
        return Assignment.objects.latest()

    def _correct_count(self, assignment):
        current_ophase = Ophase.current()
        return assignment.count == Student.objects.filter(ophase=current_ophase, want_exam=True, tutor_group__group_category=assignment.group_category).count()

    def get_context_data(self):
        context = super().get_context_data()

        current_ophase = Ophase.current()
        assignment = self._get_latest_assignment()

        if current_ophase is None:
            context['message'] = "Keine Ophase, keine Zuteilung"
            context['status_icon'] = "ok"
            context['submessage'] = ""
        elif assignment is None:
            context['message'] = "Noch keine gültige Zuteilung"
            context['status_icon'] = "remove"
            context['submessage'] = ""
        elif self._correct_count(assignment):
            context['message'] = "Gültige Zuteilung"
            context['status_icon'] = "ok"
            context['submessage'] = assignment.created_at.strftime("Erstellt am %d.%m.%y um %H:%M")
        else:
            context['message'] = "Achtung: Zuteilung ist ungültig"
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
