from ophasebase.dashboard_components import CountdownWidget
from students.dashboard_components import StudentCountWidget


class Dashboard():
    active_widgets = [
        CountdownWidget(),
        StudentCountWidget()
    ]