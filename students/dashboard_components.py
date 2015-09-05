from django.utils.safestring import SafeText
from dashboard.components import WidgetComponent


class StudentCountWidget(WidgetComponent):
    permissions = []
    name = "Erstie-Anmeldung"
    link_target = "#"

    @property
    def render(self):
        return SafeText("<h3>5</h3>")