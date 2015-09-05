import datetime
from django.utils.safestring import SafeText
from dashboard.components import WidgetComponent

from .models import Ophase

class CountdownWidget(WidgetComponent):
    permissions = []
    name = "Überblick"
    link_target = ""

    @property
    def render(self):
        #current_ophase = Ophase.current()
        #time_delta = current_ophase.start_date.day - datetime.date.today()
        #return "<span style='font-size:50px'>%i</span>" % time_delta.days
        return SafeText("<h3>Noch 5 Tage</h3>")