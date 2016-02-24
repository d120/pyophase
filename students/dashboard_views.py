from django.views.generic import TemplateView, DetailView, ListView
from django.db.models import Count, Sum
from django.utils.translation import ugettext_lazy as _

from dashboard.components import DashboardAppMixin
from ophasebase.models import Ophase
from staff.models import TutorGroup
from .models import Student, Newsletter


class StudentsAppMixin(DashboardAppMixin):
    app_name_verbose = _("Ersties")
    app_name = _('students')
    permissions = ['students.add_student', 'exam.add_assignment']

    @property
    def sidebar_links(self):
        return [
            (_('Übersicht'), self.prefix_reverse_lazy('index')),
            (_('Zertifikate erstellen'), self.prefix_reverse_lazy('certificate')),
            (_('Newsletter'), self.prefix_reverse_lazy('newsletter'))
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


class ExportCertificateView(StudentsAppMixin, ListView):
    model = Student
    template_name = "students/dashboard/view_certificate.html"

    def get_queryset(self):
        return Student.objects.filter(want_exam=True).order_by('tutor_group__name', 'name', 'prename')


class NewsletterOverviewView(StudentsAppMixin, ListView):
    model = Newsletter
    template_name = "students/dashboard/view_newsletter_overview.html"

    def get_queryset(self):
        return Newsletter.objects.annotate(num=Count('student'))


class ExportNewsletterSubscriptionView(StudentsAppMixin, ListView):
    model = Student
    template_name = "students/dashboard/view_export_newsletter.html"

    def get_queryset(self):
        return Student.objects.filter(newsletters__id=self.kwargs['newsletter_id'])

    def add_context_data(self, context):
        context = super().add_context_data(context)
        context['newsletter_name'] = Newsletter.objects.get(pk=self.kwargs['newsletter_id']).name
        return context
