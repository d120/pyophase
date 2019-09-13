from datetime import timedelta

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models import Q
from django.dispatch import receiver
from django.utils import timezone

from d120_provider.provider import D120Provider
from tuid_provider.provider import TUIDProvider
from .models import Person


@receiver(user_logged_in, dispatch_uid="e3e975a5-3f47-4b2e-bde6-71efb55e4fb4")
def person_delete_tuid_user(sender, user, request, **kwargs):
    """
    Remove all users with a linked tuid account that are not registered as staff, have not logged in for one day
    and do not have also a d120 account connected.
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    registered_staff = (p.user.username for p in Person.objects.exclude(user=None).select_related('user'))

    # all user which do not have a related staff.Person object
    no_staff_user = User.objects.filter(~Q(username__in=registered_staff), is_superuser=False, is_staff=False)

    # only the users which logged in the last time more then one day ago
    no_staff_user = no_staff_user.filter(last_login__lt=timezone.now() - timedelta(days=1))

    # get social accounts for this user
    social_accounts = SocialAccount.objects.filter(user__in=no_staff_user).select_related('user')

    user_tuid = set(s.user for s in social_accounts.filter(provider=TUIDProvider.id))
    user_d120 = set(s.user for s in social_accounts.filter(provider=D120Provider.id))

    # remove all user which do not have an additional d120 account connected
    to_delete = (u.pk for u in user_tuid.difference(user_d120))
    User.objects.filter(pk__in=to_delete).delete()
