from django.http import HttpResponse
from django.template import loader
from django.template.response import SimpleTemplateResponse
from django.utils.translation import ugettext as _


def oinforz_export(modeladmin, request, queryset):
    """Create a tex file for the OInforz containing workshop information.
    """
    template = loader.get_template("workshops/admin/workshops_oinforz.tex")
    context = {'workshops': queryset}
    output = template.render(context)
    response = HttpResponse(output, content_type="application/x-tex")
    response['Content-Disposition'] = 'attachment; filename="workshops.tex"'
    return response

oinforz_export.short_description = _('OInforz Tex Export')


def workshop_tutor_list(modeladmin, request, queryset):
    """Export a list of all workshop tutors with their respective workshops.
    """
    template = loader.get_template("workshops/admin/workshop_tutor_list.html")
    context = {
        'workshops': queryset,
        'opts': modeladmin.opts
    }
    return SimpleTemplateResponse(template, context)

workshop_tutor_list.short_description = _('Liste der Workshoptutoren')


def aushang_export(modeladmin, request, queryset):
    """Create a tex file for the OInforz containing workshop information.
    """
    template = loader.get_template("workshops/admin/workshops_aushang.tex")
    context = {'workshops': queryset}
    output = template.render(context)
    response = HttpResponse(output, content_type="text/plain; charset=utf-8")
    response['Content-Disposition'] = 'inline; filename="workshops_aushang.tex"'
    return response

aushang_export.short_description = _('Aushang Tex Export')

def mail_text_export(modeladmin, request, queryset):
    """Create a tex file for the OInforz containing workshop information.
    """
    email_template = loader.get_template('workshops/mail/confirmation.txt')
    output = ""
    for workshop in queryset:
        email_body = email_template.render({
            'workshop': workshop,
        })
        output += workshop.tutor_name + " <" + workshop.tutor_mail + ">" +\
                    ("\r\n"*2) + email_body + ("\r\n"*4)
    response = HttpResponse(output, content_type="text/plain; charset=utf-8")
    #response['Content-Disposition'] = 'inline; filename="workshops_aushang.tex"'
    return response

mail_text_export.short_description = _('Bestätigungsmail Export')
