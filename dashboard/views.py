from django.views.generic import TemplateView

from .dashboard import Dashboard
from .components import ViewComponent
from .shortcuts import check_permissions


class IndexView(ViewComponent):
    template_name = 'dashboard/overview.html'
    navigation_links = Dashboard.navigation_links

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        active_widgets_for_current_user = []
        #Check the permissions for each widget...
        for widget in Dashboard.active_widgets:
            #...only add widgets with matching permissions
            if check_permissions(user, widget.permissions):
                active_widgets_for_current_user.append(widget)

        context['widgets'] = active_widgets_for_current_user
        return context


class PermissionMissingView(TemplateView):
    template_name = 'dashboard/permission_required.html'

