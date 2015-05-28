from django.views.generic import TemplateView

# Create your views here.

class WelcomeView(TemplateView):
    template_name = "ophasebase/welcome.html"
