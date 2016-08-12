from django.views.generic import TemplateView
from ophasebase.models import Ophase


class HomepageView(TemplateView):
    template_name = "website/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_ophase'] = Ophase.current()
        return context


class BachelorView(TemplateView):
    template_name = "website/bachelor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_ophase'] = Ophase.current()
        return context


class MasterDeView(TemplateView):
    template_name = "website/master-de.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_ophase'] = Ophase.current()
        return context


class MasterDssView(TemplateView):
    template_name = "website/master-dss.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_ophase'] = Ophase.current()
        return context


class HelfenView(TemplateView):
    template_name = "website/helfen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_ophase'] = Ophase.current()
        return context