from allauth.socialaccount import app_settings
from allauth_cas.views import CASAdapter, CASCallbackView, CASLoginView, CASLogoutView

from .provider import TUIDProvider


class TUIDAdapter(CASAdapter):
    provider_id = TUIDProvider.id

    default_url = 'https://sso.tu-darmstadt.de'
    settings = app_settings.PROVIDERS.get(provider_id, {})
    url = settings.get('URL', default_url)

    version = 3


login = CASLoginView.adapter_view(TUIDAdapter)
callback = CASCallbackView.adapter_view(TUIDAdapter)
logout = CASLogoutView.adapter_view(TUIDAdapter)