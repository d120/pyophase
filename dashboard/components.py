from django.template.loader import render_to_string


class WidgetComponent():
    """
    Base class for a dashboard widget.
    """

    permissions = []
    name = ""
    link_target = ""
    status = "default"

    @property
    def render(self):
        """
        Create a chunk of html to be displayed in panel for this widget.

        :return: SafeText
        """
        raise NotImplementedError

    @property
    def get_status(self):
        return self.status


class TemplateWidgetComponent(WidgetComponent):
    """
    Base class for a dashboard widget that uses templates.
    """

    template_name = ""

    @property
    def render(self):
        return render_to_string(self.template_name, self.get_context_data())

    def get_context_data(self):
        return {}
