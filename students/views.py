from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from ophasebase.models import Ophase

from .forms import StudentRegisterForm
from .models import Settings, Student


class StudentAdd(CreateView):
    model = Student
    success_url = reverse_lazy('students:registration_success')
    form_class = StudentRegisterForm

    def get_context_data(self, **kwargs):
        current_ophase = Ophase.current()
        settings = Settings.instance()
        context = super().get_context_data(**kwargs)
        if current_ophase is not None and settings is not None:
            context['ophase_title'] = str(current_ophase)
            context['student_registration_enabled'] = settings.student_registration_enabled
        else:
            context['ophase_title'] = 'Ophase'
            context['student_registration_enabled'] = False
        return context

    def get_initial(self):
        initial = super().get_initial()

        # we use session.pop here to be able to drop the information
        # about the pervious group by reloading the browser
        initial['tutor_group'] = self.request.session.pop('previous_tutor_group', None)

        return initial

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(StudentAdd, self).get_form_kwargs(**kwargs)
        form_kwargs['exam_enabled'] = self.kwargs.get('exam_enabled', True)
        return form_kwargs

    def form_valid(self, form):
        settings = Settings.instance()
        if settings is None or not settings.student_registration_enabled:
            return HttpResponseForbidden()

        self.request.session['previous_tutor_group'] = form.data['tutor_group']
        self.request.session['exam_enabled'] = self.kwargs.get('exam_enabled', True)
        return super().form_valid(form)

    @method_decorator(permission_required('students.add_student'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class StudentAddSuccess(TemplateView):
    template_name = 'students/success.html'

    def get_context_data(self, **kwargs):

        current_ophase = Ophase.current()

        context = super().get_context_data(**kwargs)

        context['ophase_title'] = 'Ophase'
        if current_ophase is not None:
            context['ophase_title'] = str(current_ophase)

        context['registration_form'] = 'students:registration'
        if 'exam_enabled' in self.request.session and \
            self.request.session['exam_enabled'] == False:
            context['registration_form'] = 'students:registration-master'
        return context
