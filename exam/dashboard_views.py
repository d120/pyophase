from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DetailView
from dashboard.components import DashboardAppMixin

from exam.models import ExamRoom, Assignment, PersonToExamRoomAssignment
from ophasebase.models import Ophase
from students.models import Student


class ExamAppMixin(DashboardAppMixin):
    app_name_verbose = "Klausur"
    app_name = 'exam'
    permissions = ['exam.add_assignment']

    @property
    def sidebar_links(self):
        return [
            ('Zuteilungen', self.prefix_reverse_lazy('assignment')),
            ('Neue Zuteilung', self.prefix_reverse_lazy('assignment_new'))
        ]


class AssignmentIndexView(ExamAppMixin, ListView):
    template_name = "exam/dashboard/assignment_overview.html"
    model = Assignment


class AssignmentDetailView(ExamAppMixin, DetailView):
    template_name = "exam/dashboard/assignment_detail.html"
    model = Assignment


class AssignmentNameListView(ExamAppMixin, ListView):
    template_name = "exam/dashboard/assignment_name_list.html"
    model = PersonToExamRoomAssignment

    def get_queryset(self):
        return super().get_queryset().filter(assignment_id=self.kwargs['assignment_id'])


class MakeAssignmentView(ExamAppMixin, CreateView):
    model = Assignment
    fields = ['group_category', 'spacing', 'mode']
    success_url = reverse_lazy('dashboard:exam:assignment_success')

    def get_context_data(self, **kwargs):
        context = super(MakeAssignmentView, self).get_context_data(**kwargs)
        exam_rooms = ExamRoom.objects.filter(available=True)
        context['student_count'] = Student.objects.filter(ophase=Ophase.current(), want_exam=True).order_by('name', 'prename').count()
        context['free_places_1'] = sum([exam_room.capacity(1) for exam_room in exam_rooms])
        context['free_places_2'] = sum([exam_room.capacity(2) for exam_room in exam_rooms])
        return context


class MakeAssignmentSuccess(ExamAppMixin, TemplateView):
    template_name = 'exam/success.html'
