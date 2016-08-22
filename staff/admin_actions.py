import io

from django.template import loader
from django.template.response import SimpleTemplateResponse
from django.http import HttpResponse
from django.db.models import Q, Count, Case, When
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mass_mail

from staff.models import HelperJob, OrgaJob

from collections import namedtuple

import odswriter


def mail_export(modeladmin, request, queryset):
    """Creates a list of email addresses in "prename lastname <email@example.net>" format.
    This should be suitable for mass subscription and similar purposes.
    """
    template = loader.get_template("staff/mail_export.html")
    context = {'persons' : queryset}
    return SimpleTemplateResponse(template, context)

mail_export.short_description = _('E-Mail Mass Subscription Export')


def staff_nametag_export(modeladmin, request, queryset):
    """Exports certain staff data in ods format, containing the necessary information for the name tag production application.
    The produced ods file is the input for the name tag Java aplication.
    """
    table = []
    EMPTY = '~'
    rowlength = None

    for person in queryset.filter(Q(is_tutor=True) | Q(is_orga=True)):
        tutor = EMPTY
        orga = EMPTY
        if person.is_tutor:
            if "master" in str(person.tutor_for).lower():
                tutor = 'MASTER'
            else:
                tutor = 'TUTOR'
        if person.is_orga:
            orga = 'ORGA'
        row = [person.prename, person.name, tutor, tutor[0], orga,] + [EMPTY] * 4
        table.append(row)

        if rowlength is None:
            rowlength = len(row)

    out_stream = io.BytesIO()
    with odswriter.writer(out_stream) as out:
        # need to specify number of columns for jOpenDocument compatibility
        sheet = out.new_sheet("Staff", cols=rowlength)
        sheet.writerows(table)

    response = HttpResponse(out_stream.getvalue(), content_type="application/vnd.oasis.opendocument.spreadsheet")
    # name the file according to the expectations of the Java name tag application
    response['Content-Disposition'] = 'attachment; filename="tutoren.ods"'
    return response

staff_nametag_export.short_description = _('Namensschilderexport')


def staff_overview_export(modeladmin, request, queryset):
    """Exports an overview of the staff containing contact data and field of duty.
    """
    tutors = []
    orgas = []
    helpers = []

    queryset = queryset.order_by('name', 'prename')

    common_header = [_('Vorname'), _('Nachname'), _('E-Mail'), _('Handy'),]

    for person in queryset:
        row = [person.prename, person.name, person.email, person.phone]
        if person.is_tutor:
            tutors.append(row + [str(person.tutor_for)])
        if person.is_orga:
            jobs = ' / '.join([str(job) for job in person.orga_jobs.all()])
            orgas.append(row + [jobs])
        if person.is_helper:
            jobs = ' / '.join([str(job) for job in person.helper_jobs.all()])
            helpers.append(row + [jobs])

    out_stream = io.BytesIO()
    with odswriter.writer(out_stream) as out:
        Sheetdata = namedtuple('Sheetdata', 'title extra_header rows')
        for data in (Sheetdata(_('Orgas'), _('Verantwortlich für ...'), orgas),
            Sheetdata(_('Tutoren'), _('Betreut ...'), tutors),
            Sheetdata(_('Helfer'), _('Hilft bei ...'), helpers), ):
                sheet = out.new_sheet(data.title)
                sheet.writerow(common_header + [data.extra_header])
                sheet.writerows(data.rows)

    response = HttpResponse(out_stream.getvalue(), content_type="application/vnd.oasis.opendocument.spreadsheet")
    response['Content-Disposition'] = 'attachment; filename="Personal.ods"'
    return response

staff_overview_export.short_description = _('Übersicht exportieren')


def job_overview(jobtype, modeladmin, request, queryset):
    """Display a matrix to show persons with associated jobs.
    """
    template = loader.get_template("staff/job_matrix.html")

    if jobtype == 'helper':
        persons = queryset.filter(is_helper=True)
        jobs = HelperJob.objects.all().annotate(num_person=Count(Case(When(person__is_helper=True, then=1))))
    elif jobtype == 'orga':
        persons = queryset.filter(is_orga=True)
        jobs = OrgaJob.objects.all().annotate(num_person=Count(Case(When(person__is_orga=True, then=1))))

    jobs.order_by('label')

    for person in persons:
        job_interest = []
        for j in jobs:
            if jobtype == 'helper' and person.helper_jobs.filter(id=j.id).exists() or \
               jobtype == 'orga' and person.orga_jobs.filter(id=j.id).exists():
                    job_interest.append(True)
            else:
                job_interest.append(False)
        person.job_interest = job_interest

    context = {
        'jobtype' : jobtype,
        'persons' : persons,
        'jobs' : jobs,
    }

    return SimpleTemplateResponse(template, context)

def helper_job_overview(modeladmin, request, queryset):
    """Display a matrix to show helpers with associated helper jobs.
    """
    return job_overview('helper', modeladmin, request, queryset)

helper_job_overview.short_description = _('Helfer-Übersicht anzeigen')


def orga_job_overview(modeladmin, request, queryset):
    """Display a matrix to show orga with associated orga jobs.
    """
    return job_overview('orga', modeladmin, request, queryset)

orga_job_overview.short_description = _('Orga-Übersicht anzeigen')


def tutorgroup_export(modeladmin, request, queryset):
    """Exports group names with associated tutors in ods format.
    The produced ods file serves as an input for the name tag Java aplication.
    """
    table = []
    max_number_of_tutors = max(group.tutors.count() for group in queryset)
    head_row = ['Gruppenname', 'Gruppenbild']
    for i in range(1, max_number_of_tutors+1):
        head_row.extend(['Tutor ' + str(i), "Nummer Tutor " + str(i)])
    table.append(head_row)
    for group in queryset.order_by('name'):
        row = [group.name, 'icon_' + group.name.lower()]
        for tutor in group.tutors.all():
            row.extend([str(tutor), tutor.phone])
        table.append(row)

    out_stream = io.BytesIO()
    with odswriter.writer(out_stream) as out:
        # need to specify number of columns for jOpenDocument compatibility
        sheet = out.new_sheet("Gruppen", cols=2*max_number_of_tutors+2)
        sheet.writerows(table)

    response = HttpResponse(out_stream.getvalue(), content_type="application/vnd.oasis.opendocument.spreadsheet")
    # name the file according to the expectations of the Java name tag application
    response['Content-Disposition'] = 'attachment; filename="gruppen.ods"'
    return response

tutorgroup_export.short_description = _('Kleingruppen exportieren')


def __get_fillform_email(register_view_url, person):
    """Create the mass_mail tuple for one person"""

    fillform_link = '{}{}'.format(register_view_url, person.get_fillform())

    values = {'user_prename': person.prename,
             'user_name':  person.name,
             'user_email': person.email,
             'fillform_link': fillform_link,
             }

    subject = _('Erneute Anmeldung bei der nächsten Ophase').format(**values)
    to = ['{user_prename} {user_name} <{user_email}>'.format(**values)]

    message = _("""Hallo {user_prename},

vielen Dank dass du bei dieser Ophase mitgeholfen hast. Wir würden uns freuen,
wenn du uns auch bei der nächsten Ophase wieder unterstützt.

Mit dem folgenden Link kannst die Registrierung für die nächste Ophase
beschleunigen:

{fillform_link}

Viele Grüße,
Die Ophasen-Leitung""").format(**values)

    return (subject, message, None, to)

def send_fillform_mail(modeladmin, request, queryset):
    """Send fillform informations to the user"""

    register_view_url = request.build_absolute_uri(reverse('staff:registration'))

    mails = tuple(__get_fillform_email(register_view_url, p) for p in queryset)

    send_mass_mail(mails)

    count = queryset.count()
    admin_msg = ungettext(
        'Die Fillform E-Mail wurde an %(count)d Person verschickt.',
        'Die Fillform E-Mails wurden an %(count)d Personen verschickt.',
        count) % {
        'count': count,
    }
    modeladmin.message_user(request, admin_msg, messages.SUCCESS)

send_fillform_mail.short_description = _('Fillform E-Mail an Person senden')
