import tempfile, os, shutil
from subprocess import Popen, PIPE

from django.template.loader import get_template


class LaTeX:
    def escape(queryset):
        for item in queryset:
            for key, value in item.__dict__.items():
                if isinstance(value, str):
                    item.__dict__[key] = value.replace('_', '\_')
        return queryset

    def render(items, template_name, assets):
        template = get_template(template_name)
        rendered_tpl = template.render({'kiffels': items}).encode('utf-8')
        with tempfile.TemporaryDirectory() as tempdir:
            for asset in assets:
                shutil.copy(os.path.dirname(os.path.realpath(__file__))+'/assets/'+asset, tempdir)
            process = Popen(['pdflatex'], stdin=PIPE, stdout=PIPE, cwd=tempdir,)
            pdflatex_output = process.communicate(rendered_tpl)
            try:
                with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
                    pdf = f.read()
            except FileNotFoundError:
                pdf = None
        return (pdf, pdflatex_output)