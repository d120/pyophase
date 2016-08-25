import datetime

from django.utils.dateformat import DateFormat
from django.utils.safestring import SafeText
from django.utils.translation import ugettext as _, ungettext

from dashboard.components import WidgetComponent

from .models import Ophase


class CountdownWidget(WidgetComponent):
    name = _('Ophasenstatus')

    @property
    def render(self):
        ophase = Ophase.current()
        if ophase is None:
            msg = _('Keine Ophase<br />in Aussicht')
        elif datetime.date.today() < ophase.start_date:
            delta = ophase.start_date - datetime.date.today()
            msg = ungettext(
                            '<b>%(days)d Tag</b><br />bis zur Ophase',
                            '<b>%(days)d Tage</b><br />bis zur Ophase',
                            delta.days
                            ) % {
                                 'days' : delta.days,
                                 }
        elif ophase.end_date < datetime.date.today():
            msg = _('Die Ophase<br />ist vorüber')
        else:
            df = DateFormat(datetime.datetime.now())
            msg = _('Es ist Ophase<br /> <b>%(weekday)s</b>') % {'weekday' : df.format('l'),}
        return SafeText("<p class='text-center quite-big'>{}</p>".format(msg))

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
