from dashboard.components import AppViewComponent
from ophasebase.models import Ophase
from .models import Student, TutorGroup
from django.db.models import Count, Sum


class StudentsView(AppViewComponent):
    app_name_verbose = "Ersties"
    app_name = 'students'

    @property
    def sidebar_links(self):
        return [
            ('Übersicht', self.prefix_reverse_lazy('index')),
            ('Zertifikate erstellen', self.prefix_reverse_lazy('certificate'))
        ]


class StudentStatsView(StudentsView):
    template_name = "students/dashboard/view_stats.html"
    permissions = ['students.add_student']

    def get_context_data(self):
        context = super().get_context_data()

        current_ophase = Ophase.current()
        context['ophase_title'] = 'Ophase'
        if current_ophase is not None:
            context['ophase_title'] = str(current_ophase)

            Students = Student.objects.filter(ophase=current_ophase)

            context['count_student'] = Students.count()
            context['count_exam'] = Students.filter(want_exam=True).count()
            context['count_newsletter'] = Students.filter(want_newsletter=True).count()

            context['tutor_groups'] = TutorGroup.objects\
                                                    .annotate(
                                                        num=Count('student'),
                                                        num_exam=Sum('student__want_exam'),
                                                        num_newsletter=Sum('student__want_newsletter'))\
                                                    .order_by('name')
        return context


class ExportCertificateView(StudentsView):
    template_name = "students/dashboard/view_certificate.html"
