from django.http import HttpResponse
from django.shortcuts import render

from ophasebase.helper import LaTeX


def generate_part_cert(modeladmin, request, queryset):
    """ Generates a PDF file with exam certificates for selected students and sends it to the browser """
    (pdf, pdflatex_output) = LaTeX.render(queryset, 'students/reports/exam-report.tex', ['scheine.sty', 'kif_logo.png'], 'students')
    if pdf == None:
        return render(request, "students/reports/rendering-error.html", { "content": pdflatex_output[0].decode("utf-8") })
    r = HttpResponse(content_type='application/pdf')
    r['Content-Disposition'] = 'attachment; filename=ophase-exam-reports.pdf'
    r.write(pdf)
    return r

generate_part_cert.short_description = 'Klausurzertifikate drucken'