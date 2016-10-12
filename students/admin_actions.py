from .reports import generate_cert_response

def generate_part_cert(modeladmin, request, queryset):
    """ Generates a PDF file with exam certificates for selected students and sends it to the browser """

    response = generate_cert_response(request, queryset)

    return response

generate_part_cert.short_description = 'Klausurzertifikate drucken'
