from django.http import HttpResponse
from django.shortcuts import render

from ophasebase.helper import LaTeX
from ophasebase.models import Ophase


def generate_part_cert(modeladmin, request, queryset):
    """ Generates a PDF file with exam certificates for selected students and sends it to the browser """
    current_ophase = Ophase.current()
    (pdf, pdflatex_output) = LaTeX.render({"items": queryset.prefetch_related('tutor_group', 'tutor_group__tutors', ), "current_ophase": current_ophase},
                                          'students/reports/exam-report.tex', ['scheine.sty', 'OPhasenWesen.png'],
                                          'students')
    if pdf is None:
        return render(request, "students/reports/rendering-error.html", {"content": pdflatex_output[0].decode("utf-8")})
    r = HttpResponse(content_type='application/pdf')
    r['Content-Disposition'] = 'attachment; filename=ophase-exam-reports.pdf'
    r.write(pdf)
    return r


generate_part_cert.short_description = 'Klausurzertifikate drucken'
