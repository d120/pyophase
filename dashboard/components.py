from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from .dashboard_links import DashboardLinks
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


class DashboardBaseMixin:
    """
    Base mixin to transform django generic views into dashboard views

    This should handle all common functionality that is needed in every generic view
    """
    action_name = ""
    app_name_verbose = ""
    app_name = ""
    navigation_links = DashboardLinks.get_navigation_links()
    redirect_target = DashboardLinks.get_permission_missing_link()
    permissions = []

    def add_context_data(self, context):
        """
        Add additional data to the given context object.

        This should be used in all childs of DashboardBaseView instead of directly overriding get_context_data()
        """
        context['navigation_links'] = self.navigation_links
        context['app_name_verbose'] = self.app_name_verbose
        context['action_name'] = self.action_name
        return context

    def dispatch(self, request, *args, **kwargs):
        if not check_permissions(request.user, self.permissions):
            return redirect(self.redirect_target)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.add_context_data(context)


class DashboardAppMixin(DashboardBaseMixin):
    """
    Base class for dashboard views with app name and sidebar links
    """
    sidebar_links = []

    def add_context_data(self, context):
        context = super().add_context_data(context)
        context['sidebar_links'] = self.sidebar_links
        context['current_page'] = '/dashboard/' + self.app_name
        return context

    def prefix_reverse_lazy(self, target):
        """
        Adds necessary prefixes and calls reverse_lazy

        :param target: target name (without prefixes)
        :return: lazily resolved URL
        """
        return reverse_lazy('%s:%s:%s' % (DashboardLinks.get_prefix(), self.app_name, target))
