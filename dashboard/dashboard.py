from django.core.urlresolvers import reverse_lazy
from ophasebase.dashboard_components import CountdownWidget
from students.dashboard_components import StudentCountWidget


class Dashboard():
    active_widgets = [
        CountdownWidget(),
        StudentCountWidget()
    ]

    navigation_links = [
        ("Übersicht", reverse_lazy('dashboard:index')),
        ("Ersties", reverse_lazy('dashboard:students:index'))
    ]