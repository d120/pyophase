import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView)
from .provider import D120Provider
from allauth.socialaccount import app_settings


class D120Adapter(OAuth2Adapter):
    provider_id = D120Provider.id

    provider_default_url = 'https://sso.d120.de'

    settings = app_settings.PROVIDERS.get(provider_id, {})
    provider_base_url = settings.get('URL', provider_default_url)

    # Fetched programmatically, must be reachable from container
    access_token_url = '{}/o/token/'.format(provider_base_url)
    profile_url = '{}/profile/'.format(provider_base_url)

    # Accessed by the user browser, must be reachable by the host
    authorize_url = '{}/o/authorize/'.format(provider_base_url)

    # NOTE: trailing slashes in URLs are important, don't miss it

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(D120Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(D120Adapter)
