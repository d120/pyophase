from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from pyTUID.models import TUIDUser

from tuid_provider.provider import TUIDProvider


class Command(BaseCommand):
    help = 'Migrate pytuid user to the allauth tuid provider'

    def handle(self, *args, **options):
        if not "pyTUID" in settings.INSTALLED_APPS:
            raise CommandError('pyTUID is not installed.')

        tuids = TUIDUser.objects.all()

        for tuid in tuids:
            try:
                user = User.objects.create_user(tuid.uid, tuid.email)
            except IntegrityError:
                user = User.objects.get(username=tuid.uid)
            user.fist_name = tuid.given_name
            user.last_name = tuid.surname
            user.save()

            SocialAccount.objects.get_or_create(user=user, uid=tuid.uid, provider=TUIDProvider.id)
