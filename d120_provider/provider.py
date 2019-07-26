from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class D120Account(ProviderAccount):
    pass


class D120Provider(OAuth2Provider):
    id = 'd120'
    name = 'D120 OAuth2 Provider'
    account_class = D120Account

    def extract_uid(self, data):
        return str(data['username'])

    def extract_common_fields(self, data):
        return dict(username=data['username'],
                    email=data.get('email', ''),
                    first_name=data.get('firstName', ''),
                    last_name=data.get('lastName', ''), )

    def get_default_scope(self):
        scope = ['read', 'microprofile-jwt']
        return scope


providers.registry.register(D120Provider)
