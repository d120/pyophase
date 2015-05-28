from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count

from ophasebase.models import Ophase
from students.models import Student, TutorGroup, Settings


class StudentAdd(CreateView):
    model = Student
    fields = ['prename', 'name', 'tutorGroup', 'wantExam', 'wantNewsletter', 'email']
    success_url = reverse_lazy('students:registration_success')

    def get_context_data(self, **kwargs):
        
        current_ophase_qs = Ophase.objects.filter(is_active=True)
        settings_qs = Settings.objects.all()
        
        context = super(StudentAdd, self).get_context_data(**kwargs)
        
        context['ophase_title'] = 'Ophase'
        
        if len(current_ophase_qs) == 1:
            context['ophase_title'] = current_ophase_qs[0].__str__()
        
        if len(settings_qs) == 1:
            settings = settings_qs[0]
            
            context['student_registration_enabled'] = settings.student_registration_enabled
        else:
            context['student_registration_enabled'] = False
        
        return context


class StudentAddSuccess(TemplateView):
    template_name = 'students/success.html'

    def get_context_data(self, **kwargs):
        
        current_ophase_qs = Ophase.objects.filter(is_active=True)
        
        context = super(StudentAddSuccess, self).get_context_data(**kwargs)
        
        context['ophase_title'] = 'Ophase'
        if len(current_ophase_qs) == 1:
            context['ophase_title'] = current_ophase_qs[0].__str__()
        return context


class StudentRegistrationCount(TemplateView):
    template_name = 'students/counts.html'

    def get_context_data(self, **kwargs):
        context = super(StudentRegistrationCount, self).get_context_data(**kwargs)

        current_ophase_qs = Ophase.objects.filter(is_active=True)
        context['ophase_title'] = 'Ophase'
        if len(current_ophase_qs) == 1:
            current_ophase = current_ophase_qs[0]
            context['ophase_title'] = current_ophase.__str__()
        
            Students = Student.objects.filter(ophase=current_ophase)
            context['studentCount'] = Students.count()
            context['examCount'] = Students.filter(wantExam=True).count()
            context['newsletterCount'] = Students.filter(wantNewsletter=True).count()
            
            #Get the number of Tutor Groups who have at least one Student in the current Ophase            
            context['tutorGroupCount'] = TutorGroup.objects.filter(student__ophase=current_ophase).annotate(num=Count('student')).filter(num__gte=1).count()
        return context
