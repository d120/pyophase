from ophasebase.dashboard_components import CountdownWidget
from students.dashboard_widgets import StudentCountWidget


class DashboardWidgets():
    active_widgets = [
        CountdownWidget(),
        StudentCountWidget()
    ]


