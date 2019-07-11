from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth_cas.providers import CASProvider


class TUIDAccount(ProviderAccount):
    pass


class TUIDProvider(CASProvider):
    id = 'tuid'  # Choose an identifier for your provider
    name = 'TU-ID CAS Provider'  # Verbose name of your provider
    account_class = TUIDAccount


providers.registry.register(TUIDProvider)
