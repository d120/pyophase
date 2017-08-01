from django.http import HttpResponse
from django.shortcuts import render

from ophasebase.helper import LaTeX
from ophasebase.models import Ophase

def generate_nametags(queryset):
    """ Generates a PDF file with nametags for students in the queryset """
    current_ophase = Ophase.current()
    (pdf, pdflatex_output) = LaTeX.render({"items": queryset, "current_ophase": current_ophase},
                                          'staff/reports/tutorenschilder.tex', ['OPhasenWesen.png'],
                                          'staff')
    return (pdf, pdflatex_output)

def generate_nametag_response(request, queryset):
    """ Generates a PDF file with exam certificates for students in the queryset and sends it to the browser """
    (pdf, pdflatex_output) = generate_nametags(queryset)

    if not pdf:
        return render(request, "staff/reports/rendering-error.html", {"content": pdf}) #pdflatex_output[0].decode("utf-8")})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=tutorenschilder.pdf'
    response.write(pdf)
    return response
