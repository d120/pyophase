from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth_cas.providers import CASProvider


class TUIDAccount(ProviderAccount):
    pass


class TUIDProvider(CASProvider):
    id = 'tuid'  # Choose an identifier for your provider
    name = 'TU-ID CAS Provider'  # Verbose name of your provider
    account_class = TUIDAccount

    def extract_uid(self, data):
        return str(data[1]['cn'])

    def extract_common_fields(self, data):
        extra = data[1]
        return dict(username=extra.get('cn', ''),
                    email=extra.get('mail', ''),
                    first_name=extra.get('givenName', ''),
                    last_name=extra.get('surname', ''),
                    )

providers.registry.register(TUIDProvider)
