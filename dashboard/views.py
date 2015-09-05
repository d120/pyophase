from django.views.generic import TemplateView

from .dashboard import Dashboard


class IndexView(TemplateView):
    template_name = 'dashboard/overview.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)

        user = self.request.user

        active_widgets_for_current_user = []
        #Check the permission for each widget - only add widgets...
        for widget in Dashboard.active_widgets:
            #...without special permissions...
            if len(widget.permissions) == 0:
                active_widgets_for_current_user.append(widget)
            #...or those with at least one matching permission
            else:
                for permission in widget.permissions:
                    if user.has_perm(permission):
                        active_widgets_for_current_user.append(widget)
                        break

        context['widgets'] = active_widgets_for_current_user
        return context