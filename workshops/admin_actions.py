from django.template import loader
from django.http import HttpResponse
from django.utils.translation import ugettext as _

def oinforz_export(modeladmin, request, queryset):
    template = loader.get_template("workshops/admin/workshops.tex")
    context = {'workshops' : queryset}
    output = template.render(context)
    response = HttpResponse(output, content_type="application/x-tex")
    response['Content-Disposition'] = 'attachment; filename="workshops.tex"'
    return response

oinforz_export.short_description = _('OInforz Tex Export')
