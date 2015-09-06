from django.core.urlresolvers import reverse_lazy
from dashboard.components import TemplateWidgetComponent, ViewComponent
from ophasebase.models import Ophase
from students.models import Student, TutorGroup
from django.db.models import Count, Sum


class StudentCountWidget(TemplateWidgetComponent):
    permissions = ['students.add_student']
    name = "Erstie-Anmeldung"
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


class StudentStatsView(ViewComponent):
    template_name = "students/dashboard/view_stats.html"
    permissions = ['students.add_student']
    app_name = "Ersties"

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