from django.apps import AppConfig


class StaffConfig(AppConfig):
    name = 'staff'
    verbose_name = 'Staff'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from .signals import person_delete_tuid_user
