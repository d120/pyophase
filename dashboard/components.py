from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from dashboard.dashboard_links import DashboardLinks

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
        """
        Should return the status of the current widget content.
        At the moment, these are the possible bootstrap panel states.
        default, primary, success, info, warning, danger
        """
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
    """
    Base class for dashboard views (complete page inside of dashboard).
    """

    permissions = []
    redirect_target = DashboardLinks.get_permission_missing_link()
    navigation_links = DashboardLinks.get_navigation_links()
    app_name = ""
    app_name_verbose = ""
    action_name = ""

    def dispatch(self, request, *args, **kwargs):
        if not check_permissions(request.user, self.permissions):
            return redirect(self.redirect_target)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navigation_links'] = self.navigation_links
        context['app_name_verbose'] = self.app_name_verbose
        context['action_name'] = self.action_name
        return context


class AppViewComponent(ViewComponent):
    """
    Base class for dashboard views with app name and sidebar links
    """
    sidebar_links = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_links'] = self.sidebar_links
        return context

    def prefix_reverse_lazy(self, target):
        """
        Adds necessary prefixes and calls reverse_lazy

        :param target: target name (without prefixes)
        :return: lazily resolved URL
        """
        return reverse_lazy('%s:%s:%s' % (DashboardLinks.get_prefix(), self.app_name, target))
