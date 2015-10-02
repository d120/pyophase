from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from ophasebase.models import Ophase
from students.forms import StudentRegisterForm
from students.models import Student, Settings


class StudentAdd(CreateView):
    model = Student
    success_url = reverse_lazy('students:registration_success')
    form_class = StudentRegisterForm

    def get_context_data(self, **kwargs):
        current_ophase = Ophase.current()
        settings = Settings.instance()
        context = super(StudentAdd, self).get_context_data(**kwargs)
        if current_ophase is not None and settings is not None:
            context['ophase_title'] = str(current_ophase)
            context['student_registration_enabled'] = settings.student_registration_enabled
        else:
            context['ophase_title'] = 'Ophase'
            context['student_registration_enabled'] = False
        return context

    def get_initial(self):
        initial = super(StudentAdd, self).get_initial()

        if 'previous_tutor_group' in self.request.session:
            initial['tutor_group'] = self.request.session['previous_tutor_group']

        return initial

    def form_valid(self, form):
        self.request.session['previous_tutor_group'] = form.data['tutor_group']
        return super(StudentAdd, self).form_valid(form)

    @method_decorator(permission_required('students.add_student'))
    def dispatch(self, *args, **kwargs):
        return super(StudentAdd, self).dispatch(*args, **kwargs)


class StudentAddSuccess(TemplateView):
    template_name = 'students/success.html'

    def get_context_data(self, **kwargs):

        current_ophase = Ophase.current()

        context = super(StudentAddSuccess, self).get_context_data(**kwargs)

        context['ophase_title'] = 'Ophase'
        if current_ophase is not None:
            context['ophase_title'] = str(current_ophase)
        return context
