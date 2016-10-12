from django.db.models import Count, Sum
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView

from dashboard.components import DashboardAppMixin
from ophasebase.models import Ophase
from staff.models import TutorGroup

from .models import Newsletter, Student

from .reports import generate_cert_response

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

            t_groups = TutorGroup.objects
            t_groups = t_groups.annotate(num=Count('student'))
            t_groups = t_groups.annotate(num_exam=Sum('student__want_exam'))
            t_groups = t_groups.order_by('group_category', 'name')

            # With some DB Backends Sum returns True instead of 1
            # int() fixes it.
            # see https://github.com/d120/pyophase/issues/47
            for group in t_groups:
                if group.num_exam is not None:
                    group.num_exam = int(group.num_exam)

            context['tutor_groups'] = t_groups
        return context


class ExportCertificateView(StudentsAppMixin, TemplateView):
    template_name = "students/dashboard/view_certificate.html"

    def get_context_data(self, **kwargs):
        context = super(ExportCertificateView, self).get_context_data(**kwargs)
        context['count_student'] = Student.get_current(want_exam=True).count()
        return context

    def post(self, request, *args, **kwargs):
        queryset = Student.get_current(want_exam=True).order_by('tutor_group__name', 'name', 'prename')
        return generate_cert_response(request, queryset)

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
