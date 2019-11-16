from allauth_cas.urls import default_urlpatterns
from .provider import TUIDProvider

urlpatterns = default_urlpatterns(TUIDProvider)
