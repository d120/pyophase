from exam.dashboard_widgets import ExamWidget
from ophasebase.dashboard_components import CountdownWidget
from staff.dashboard_widgets import StaffCountWidget
from students.dashboard_widgets import StudentCountWidget
from oplan.dashboard_widgets import *

class DashboardWidgets():
    active_widgets = [
        CountdownWidget(),
        StaffCountWidget(),
        StudentCountWidget(),
        ExamWidget(),
        TimetableListWidget()
    ]
