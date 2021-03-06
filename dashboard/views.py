from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from .components import DashboardBaseMixin, DashboardAppMixin
from .dashboard_widgets import DashboardWidgets
from .shortcuts import check_permissions


class IndexView(DashboardBaseMixin, TemplateView):
    template_name = 'dashboard/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        active_widgets_for_current_user = []
        #Check the permissions for each widget...
        for widget in DashboardWidgets.active_widgets:
            #...only add widgets with matching permissions
            if check_permissions(user, widget.permissions):
                active_widgets_for_current_user.append(widget)

        context['widgets'] = active_widgets_for_current_user
        return context


class PersonalDashboardMixin(DashboardAppMixin):
    app_name_verbose = _('Meine Übersicht')
    app_name = 'my'

    @property
    def sidebar_links(self):
        links = [
            (_('Start'), reverse_lazy("dashboard:personal_overview"))
        ]

        from clothing.models import Settings
        clothing_settings = Settings.instance()
        if clothing_settings is not None and clothing_settings.clothing_ordering_enabled:
            links.append((_('Kleidungsbestellung'), reverse_lazy('clothing:overview')))

        return links

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from staff.models import Person
        context['person'] = Person.get_by_user(self.request.user)
        return context


class PermissionMissingView(DashboardBaseMixin, TemplateView):
    template_name = 'dashboard/permission_required.html'


class PersonalOverview(PersonalDashboardMixin, TemplateView):
    template_name = 'dashboard/personal_overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        person = context['person']
        if person is not None:
            context['person_registered'] = True

            context['next_events'] = [attendance.event for attendance in
                                      person.attendance_set.filter(event__end__gte=timezone.now()).select_related(
                                          'event')]

            if person.is_tutor:
                context['tutor_group'] = person.tutorgroup_set.first()
                if context['tutor_group'] is not None:
                    context['tutor_partners'] = ", ".join(
                        t.get_name() for t in context['tutor_group'].tutors.exclude(id=person.id))

            from clothing.models import Order, Settings
            context['clothing_orders'] = Order.objects.filter(person=person).select_related('type', 'size', 'color')

            clothing_settings = Settings.instance()
            if clothing_settings is not None:
                context[
                    'show_clothing_order_warning'] = clothing_settings.clothing_ordering_enabled and Order.user_eligible_but_not_ordered_yet(
                    person)

        return context
