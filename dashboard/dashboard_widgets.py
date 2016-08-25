from clothing.dashboard_widgets import ClothingOrderWidget
from exam.dashboard_widgets import ExamWidget
from ophasebase.dashboard_components import CountdownWidget
from staff.dashboard_widgets import StaffCountWidget
from students.dashboard_widgets import StudentCountWidget
from workshops.dashboard_widgets import WorkshopCountWidget


class DashboardWidgets():
    active_widgets = [
        CountdownWidget(),
        StaffCountWidget(),
        StudentCountWidget(),
        WorkshopCountWidget(),
        ExamWidget(),
        ClothingOrderWidget()
    ]
