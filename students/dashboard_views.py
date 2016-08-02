from django.views.generic import TemplateView, ListView
from django.db.models import Count, Sum
from django.utils.translation import ugettext_lazy as _

from dashboard.components import DashboardAppMixin
from ophasebase.models import Ophase
from staff.models import TutorGroup
from students.models import Student, Newsletter


class StudentsAppMixin(DashboardAppMixin):
    app_name_verbose = _("Ersties")
    app_name = 'students'
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

            students = Student.get_current()

            context['count_student'] = students.count()
            context['count_exam'] = students.filter(want_exam=True).count()

            tutor_groups = TutorGroup.objects\
                                            .annotate(
                                                num=Count('student'),
                                                num_exam=Sum('student__want_exam'))\
                                            .order_by('group_category', 'name')

            # With some DB Backends Sum returns True instead of 1
            # int() fixes it.
            # see https://github.com/d120/pyophase/issues/47
            for group in tutor_groups:
                if group.num_exam != None:
                    group.num_exam = int(group.num_exam)

            context['tutor_groups'] = tutor_groups
        return context


class ExportCertificateView(StudentsAppMixin, ListView):
    model = Student
    template_name = "students/dashboard/view_certificate.html"

    def get_queryset(self):
        return Student.get_current(want_exam=True).order_by('tutor_group__name', 'name', 'prename')


class NewsletterOverviewView(StudentsAppMixin, ListView):
    model = Newsletter
    template_name = "students/dashboard/view_newsletter_overview.html"

    def get_queryset(self):
        return Newsletter.objects.annotate(num=Count('student'))


class ExportNewsletterSubscriptionView(StudentsAppMixin, ListView):
    model = Student
    template_name = "students/dashboard/view_export_newsletter.html"

    def get_queryset(self):
        return Student.get_current(newsletters__id=self.kwargs['newsletter_id'])

    def add_context_data(self, context):
        context = super().add_context_data(context)
        context['newsletter_name'] = Newsletter.objects.get(pk=self.kwargs['newsletter_id']).name
        return context
