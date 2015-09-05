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
        ophase = Ophase.current()
        if ophase is None:
            msg = "Keine Ophase in Aussicht"
        elif datetime.date.today() < ophase.start_date:
            delta = ophase.start_date - datetime.date.today()
            msg = "Noch {} Tage bis zur Ophase".format(delta.days)
        elif ophase.end_date < datetime.date.today():
            msg = "Die Ophase ist vorüber"
        else:
            weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
            msg = "Es ist Ophase<br />- {} -".format(weekdays[datetime.date.today().weekday()])
        return SafeText("<h3 class='text-center'>{}</h3>".format(msg))
