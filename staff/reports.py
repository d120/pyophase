from django.http import HttpResponse
from django.shortcuts import render

from ophasebase.helper import LaTeX


def generate_orga_cert(queryset):
    """ Generates a PDF file with orga certificates for staff people in the queryset """
    (pdf, pdflatex_output) = LaTeX.render({"items": queryset},
                                          'staff/reports/orga-report.tex', ['orgacerts.sty', 'logos_combined.png'],
                                          'staff')
    return (pdf, pdflatex_output)


def generate_orga_cert_response(request, queryset):
    """ Generates a PDF file with orga certificates for staff people in the queryset and sends it to the browser """
    (pdf, pdflatex_output) = generate_orga_cert(queryset)

    if pdf is None:
        return render(request, "staff/reports/rendering-error.html", {"content": pdflatex_output[0].decode("utf-8")})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=ophase-orga-reports.pdf'
    response.write(pdf)
    return response