from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from .shortcuts import check_permissions


class WidgetComponent():
    """
    Base class for a dashboard widget.
    """

    permissions = []
    name = ""
    link_target = ""
    status = "default"

    @property
    def render(self):
        """
        Create a chunk of html to be displayed in panel for this widget.

        :return: SafeText
        """
        raise NotImplementedError

    @property
    def get_status(self):
        return self.status


class TemplateWidgetComponent(WidgetComponent):
    """
    Base class for a dashboard widget that uses templates.
    """

    template_name = ""

    @property
    def render(self):
        return render_to_string(self.template_name, self.get_context_data())

    def get_context_data(self):
        return {}


class ViewComponent(TemplateView):
    permissions = []
    redirect_target = reverse_lazy('dashboard:missing_permission')
    navigation_links = []

    def dispatch(self, request, *args, **kwargs):
        if not check_permissions(request.user, self.permissions):
            return redirect(self.redirect_target)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navigation_links'] = self.navigation_links
        return context

