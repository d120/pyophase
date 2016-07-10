from django.views.generic import TemplateView
from ophasebase.models import Ophase

class WelcomeView(TemplateView):
    template_name = "ophasebase/welcome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_ophase'] = Ophase.current()
        return context
