from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView

from .models import ExamRoom, Assignment
from ophasebase.models import Ophase
from students.models import Student


class MakeAssignmentView(CreateView):
    model = Assignment
    fields = ['group_category', 'spacing', 'mode']
    success_url = reverse_lazy('exam:assignment_success')

    def get_context_data(self, **kwargs):
        current_ophase = Ophase.current()
        context = super(MakeAssignmentView, self).get_context_data(**kwargs)
        if current_ophase is not None:
            context['ophase_title'] = str(current_ophase)
        else:
            context['ophase_title'] = 'Ophase'
        exam_rooms = ExamRoom.objects.filter(available=True)
        context['student_count'] = Student.objects.filter(want_exam=True).order_by('name', 'prename').count()
        context['free_places_1'] = sum([exam_room.capacity(1) for exam_room in exam_rooms])
        context['free_places_2'] = sum([exam_room.capacity(2) for exam_room in exam_rooms])
        return context

    @method_decorator(permission_required('exam.add_assignment'))
    def dispatch(self, *args, **kwargs):
        return super(MakeAssignmentView, self).dispatch(*args, **kwargs)


class MakeAssignmentSuccess(TemplateView):
    template_name = 'exam/success.html'

    def get_context_data(self, **kwargs):
        current_ophase = Ophase.current()
        context = super().get_context_data(**kwargs)

        context['ophase_title'] = 'Ophase'
        if current_ophase is not None:
            context['ophase_title'] = str(current_ophase)
        return context