from django.http import HttpResponse
from django.shortcuts import render

from ophasebase.helper import LaTeX
from ophasebase.models import Ophase

def generate_cert(queryset):
    """ Generates a PDF file with exam certificates for students in the queryset """
    current_ophase = Ophase.current()
    (pdf, pdflatex_output) = LaTeX.render({"items": queryset.prefetch_related('tutor_group', 'tutor_group__tutors', ), "current_ophase": current_ophase},
                                          'students/reports/exam-report.tex', ['scheine.sty', 'OPhasenWesen.png'],
                                          'students')
    return (pdf, pdflatex_output)

def generate_cert_response(request, queryset):
    """ Generates a PDF file with exam certificates for students in the queryset and sends it to the browser """
    (pdf, pdflatex_output) = generate_cert(queryset)

    if pdf is None:
        return render(request, "students/reports/rendering-error.html", {"content": pdflatex_output[0].decode("utf-8")})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=ophase-exam-reports.pdf'
    response.write(pdf)
    return response