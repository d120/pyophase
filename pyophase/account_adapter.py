from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class DisableSignUpAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return True

    def validate_disconnect(self, account, accounts):
        raise ValidationError(_("Eine Trennung des Accounts ist nicht möglich."))
