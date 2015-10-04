from django.views.generic import TemplateView
from django.db.models import Count, Sum

from dashboard.components import DashboardAppMixin
from ophasebase.models import Ophase
from staff.models import TutorGroup
from .models import Student


class StudentsAppMixin(DashboardAppMixin):
    app_name_verbose = "Ersties"
    app_name = 'students'
    permissions = ['students.add_student']

    @property
    def sidebar_links(self):
        return [
            ('Übersicht', self.prefix_reverse_lazy('index')),
            ('Zertifikate erstellen', self.prefix_reverse_lazy('certificate'))
        ]


class StudentStatsView(StudentsAppMixin, TemplateView):
    template_name = "students/dashboard/view_stats.html"

    def get_context_data(self):
        context = super().get_context_data()

        current_ophase = Ophase.current()
        context['ophase_title'] = 'Ophase'
        if current_ophase is not None:
            context['ophase_title'] = str(current_ophase)

            Students = Student.objects.filter(ophase=current_ophase)

            context['count_student'] = Students.count()
            context['count_exam'] = Students.filter(want_exam=True).count()

            context['tutor_groups'] = TutorGroup.objects\
                                                    .annotate(
                                                        num=Count('student'),
                                                        num_exam=Sum('student__want_exam'))\
                                                    .order_by('name')
        return context


class ExportCertificateView(StudentsAppMixin, TemplateView):
    template_name = "students/dashboard/view_certificate.html"
