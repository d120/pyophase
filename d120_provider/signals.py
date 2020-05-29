from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.dispatch import receiver

from .models import GroupSync
from .provider import D120Provider


@receiver(user_logged_in, dispatch_uid="6760a6e0-8d7a-466e-bdea-91bdd70da93a")
def sig_sync_user_to_groups(sender, user, request, **kwargs):
    try:
        social_account = SocialAccount.objects.get(user=user, provider=D120Provider.id)
    except ObjectDoesNotExist:
        pass
    else:
        external_groups = social_account.extra_data.get('groups', list())
        sync_groups = GroupSync.objects
        groups_to_remove = sync_groups.filter(~Q(external_group__in=external_groups))
        groups_to_add = sync_groups.filter(external_group__in=external_groups)

        for group in groups_to_remove:
            user.groups.remove(group.django_group)

        for group in groups_to_add:
            user.groups.add(group.django_group)

        user.save()
