from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import D120Provider

urlpatterns = default_urlpatterns(D120Provider)
