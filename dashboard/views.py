from django.views.generic import TemplateView

from .dashboard import Dashboard


class IndexView(TemplateView):
    template_name = 'dashboard/overview.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['widgets'] = Dashboard.active_widgets
        return context