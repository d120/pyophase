from django.views.generic import TemplateView

class LoginSelectView(TemplateView):
    template_name = "ophasebase/login-select.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()  #
        next_url = self.request.GET.get('next', None)
        if next_url is not None:
            context['next_url'] = "?next={}".format(next_url)
        return context
