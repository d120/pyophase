from django.core.urlresolvers import reverse_lazy, reverse
from dashboard.components import TemplateWidgetComponent
from exam.models import Assignment
from ophasebase.models import Ophase
from students.models import Student
from django.utils.translation import ugettext_lazy as _
from django.utils import formats
from staff.models import GroupCategory

from django.utils.safestring import SafeText

class TimetableListWidget(TemplateWidgetComponent):
    """
    This widget lists all timetables
    """

    name = _("Stundenplaene")
    template_name = "exam/dashboard/widget_exam.html"

    @property
    def render(self):
        ophase = Ophase.current()
        if ophase is None:
            msg = _('Keine Ophase<br />in Aussicht')
        else:
            msg = ''
            for cat in GroupCategory.objects.all():
                msg += '<li><a href="' + reverse('oplan:timetable', category=cat) + '">' + str(cat) + '</a></li>'
        return SafeText(msg)

    @property
    def get_status(self):
        return "info"

