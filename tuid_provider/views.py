from allauth_cas.views import CASAdapter, CASCallbackView, CASLoginView, CASLogoutView
from .provider import TUIDProvider


class TUIDAdapter(CASAdapter):
    provider_id = TUIDProvider.id
    url = 'https://sso.tu-darmstadt.de'
    version = 3


login = CASLoginView.adapter_view(TUIDAdapter)
callback = CASCallbackView.adapter_view(TUIDAdapter)
logout = CASLogoutView.adapter_view(TUIDAdapter)