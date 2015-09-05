class WidgetComponent():
    permissions = []
    name = ""
    link_target = ""

    @property
    def render(self):
        """
        Create a chuck of html to be displayed in panel for this widget

        :return: SafeText
        """
        raise NotImplementedError

    @property
    def status(self):
        return "OK"