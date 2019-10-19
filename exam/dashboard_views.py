from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from dashboard.components import DashboardAppMixin
from students.models import Student

from .models import Assignment, ExamRoom, PersonToExamRoomAssignment


class ExamAppMixin(DashboardAppMixin):
    app_name_verbose = "Klausur"
    app_name = 'exam'
    permissions = ['exam.add_assignment']

    @property
    def sidebar_links(self):
        return [
            ('Zuteilungen', self.prefix_admin_reverse_lazy('assignment', 'changelist')),
            ('Neue Zuteilung', self.prefix_reverse_lazy('assignment_new')),
            ('Klausurräume', self.prefix_admin_reverse_lazy('examroom', 'changelist')),
        ]

class AssignmentNameListView(ExamAppMixin, ListView):
    template_name = "exam/dashboard/assignment_name_list.html"
    model = PersonToExamRoomAssignment

    def get_queryset(self):
        qs = super().get_queryset().filter(assignment_id=self.kwargs['assignment_id'])
        return qs.select_related('room', 'person', 'room__room', 'room__room__building')


class MakeAssignmentView(ExamAppMixin, CreateView):
    model = Assignment
    fields = ['group_category', 'spacing', 'mode']
    success_url = reverse_lazy('dashboard:exam:assignment_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam_rooms = ExamRoom.objects.filter(available=True)
        context['student_count'] = Student.get_current(want_exam=True).order_by('name', 'prename').count()
        context['free_places_1'] = sum([exam_room.capacity(1) for exam_room in exam_rooms])
        context['free_places_2'] = sum([exam_room.capacity(2) for exam_room in exam_rooms])
        return context


class MakeAssignmentSuccess(ExamAppMixin, TemplateView):
    template_name = 'exam/success.html'
