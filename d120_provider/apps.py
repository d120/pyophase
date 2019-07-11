from django.apps import AppConfig


class D120ProviderConfig(AppConfig):
    name = 'd120_provider'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from .signals import sig_sync_user_to_groups
