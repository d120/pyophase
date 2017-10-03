import tempfile
import os
import shutil
from subprocess import Popen, PIPE
from base64 import b64encode

from django.http import HttpResponse
from django.shortcuts import render

from ophasebase.helper import LaTeX
from ophasebase.models import Ophase


def generate_nametags(queryset, template='staff/reports/tutorenschilder.tex', context=None):
    """ Generates a PDF file with nametags for students in the queryset"""
    if context is None:
        context = {}
    context['items'] = queryset
    context['current_ophase'] = Ophase.current()
    (pdf, pdflatex_output) = LaTeX.render(context,
                                          template, [
                                              'OPhasenWesen.png'],
                                          'staff')
    return (pdf, pdflatex_output)


def generate_nametag_response(request, queryset, filename='tutorenschilder.pdf'):
    """ Generates a PDF file with nametags for students in the queryset and sends it to the browser"""
    (pdf, pdflatex_output) = generate_nametags(queryset)

    if not pdf:
        return render(request, "staff/reports/rendering-error.html", {"content": pdflatex_output[0].decode("utf-8")})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    response.write(pdf)
    return response


def generate_pdf_with_group_pictures(request, groups, filename, template, context=None):
    if context is None:
        context = {}
    context['groups'] = groups
    (pdf, pdflatex_output) = LaTeX.render(context, template,
                                          [], 'staff', [group.picture.path for group in groups if group.picture])
    if not pdf:
        return render(request, "staff/reports/rendering-error.html", {"content": pdflatex_output[0].decode("utf-8")})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    response.write(pdf)
    return response
