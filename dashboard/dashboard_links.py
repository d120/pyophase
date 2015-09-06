from django.core.urlresolvers import reverse_lazy


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
        return [
            ("Übersicht", cls.get_index_link()),
            ("Ersties", reverse_lazy('dashboard:students:index'))
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
