import datetime
from django.utils.safestring import SafeText
from dashboard.components import WidgetComponent

from .models import Ophase


class CountdownWidget(WidgetComponent):
    name = "Ophasenstatus"

    @property
    def render(self):
        ophase = Ophase.current()
        if ophase is None:
            msg = "Keine Ophase<br />in Aussicht"
        elif datetime.date.today() < ophase.start_date:
            delta = ophase.start_date - datetime.date.today()
            if delta.days < 2:
                msg = "<b>1 Tag</b><br />bis zur Ophase"
            else:
                msg = "<b>{} Tage</b><br />bis zur Ophase".format(delta.days)
        elif ophase.end_date < datetime.date.today():
            msg = "Die Ophase<br />ist vorüber"
        else:
            weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
            msg = "Es ist Ophase<br /> <b>{}</b>".format(weekdays[datetime.date.today().weekday()])
        return SafeText("<p class='text-center' style='font-size:2em; line-height:180%;'>{}</p>".format(msg))

    @property
    def get_status(self):
        ophase = Ophase.current()
        if ophase is None:
            return "warning"
        elif datetime.date.today() < ophase.start_date:
            return "info"
        elif ophase.end_date < datetime.date.today():
            return "warning"
        else:
            return "success"
