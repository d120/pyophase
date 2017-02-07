from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Ophase


# Create your tests here.

class OphaseIsActive(TestCase):
    """Ensure that only one Ophase is_active at the same time."""

    def test_only_one_is_active(self):
        # create Ophase - should be active
        o1 = Ophase.objects.create(name="Testophase 1", is_active=True)
        self.assertEqual(o1.is_active, True)
        # now create other Ophase - should be active while first one should be inactive
        o2 = Ophase.objects.create(name="Testophase 2", is_active=True)
        o1 = Ophase.objects.get(pk=o1.pk)
        self.assertEqual(o1.is_active, False)
        self.assertEqual(o2.is_active, True)
        # set first Ophase active again, second should be inactive
        o1.is_active = True
        o1.save()
        o1 = Ophase.objects.get(pk=o1.pk)
        o2 = Ophase.objects.get(pk=o2.pk)
        self.assertEqual(o1.is_active, True)
        self.assertEqual(o2.is_active, False)
