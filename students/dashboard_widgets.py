from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from dashboard.components import TemplateWidgetComponent
from ophasebase.models import Ophase
from staff.models import TutorGroup
from .models import Student


class StudentCountWidget(TemplateWidgetComponent):
    permissions = ['students.add_student', 'exam.add_assignment']
    name = _("Erstie-Anmeldestatus")
    link_target = reverse_lazy('dashboard:students:index')
    template_name = "students/dashboard/widget_registration_stats.html"
    status = "success"

    def get_context_data(self):
        context = super().get_context_data()

        current_ophase = Ophase.current()
        context['ophase_title'] = 'Ophase'
        if current_ophase is not None:
            context['ophase_title'] = str(current_ophase)

            Students = Student.objects.filter(ophase=current_ophase)
            context['studentCount'] = Students.count()
            context['examCount'] = Students.filter(want_exam=True).count()

            #Get the number of Tutor Groups who have at least one Student in the current Ophase
            context['tutorGroupCount'] = TutorGroup.objects.filter(student__ophase=current_ophase).annotate(num=Count('student')).filter(num__gte=1).count()
        return context
