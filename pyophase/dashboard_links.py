from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _



class DashboardLinks():
    """
    Hold all kind of dashboard global navigation elements
    """

    @classmethod
    def get_navigation_links(cls):
        """
        Get a list of links to be displayed in main navigation bar.
        :return: List(String, String) - a list of (name, URL)-tuples
        """

        from clothing.dashboard_views import ClothingAppMixin
        from dashboard.views import PersonalDashboardMixin
        from exam.dashboard_views import ExamAppMixin
        from staff.dashboard_views import StaffAppMixin
        from students.dashboard_views import StudentsAppMixin
        from workshops.views import WorkshopAppMixin

        return [
            (_("Start"), cls.get_index_link(), None),
            (_("Meine Übersicht"), reverse_lazy('dashboard:personal_overview'), None),
            (_("Personal"), reverse_lazy('dashboard:staff:index'), StaffAppMixin),
            (_("Ersties"), reverse_lazy('dashboard:students:index'), StudentsAppMixin),
            (_("Klausur"), reverse_lazy('dashboard:exam:assignment'), ExamAppMixin),
            (_("Kleidung"), reverse_lazy('dashboard:clothing:order_overview'), ClothingAppMixin),
            (_("Workshops"), reverse_lazy('admin:workshops_workshop_changelist'), WorkshopAppMixin),
        ]

    @classmethod
    def get_index_link(cls):
        """
        Get an URL to the start page of the dashboard.
        :return: string - url to startpage
        """
        return reverse_lazy('dashboard:index')

    @classmethod
    def get_permission_missing_link(cls):
        return reverse_lazy('dashboard:missing_permission')

    @classmethod
    def get_prefix(cls):
        return 'dashboard'
