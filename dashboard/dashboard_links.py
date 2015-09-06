from django.core.urlresolvers import reverse_lazy

__author__ = 'adminht'


class DashboardLinks():
    navigation_links = [
        ("Übersicht", reverse_lazy('dashboard:index')),
        ("Ersties", reverse_lazy('dashboard:students:index'))
    ]