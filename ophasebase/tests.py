from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Ophase


# Create your tests here.

class OphaseIsActive(TestCase):
    """Ensure that only one Ophase is_active at the same time."""

    def test_only_one_is_active(self):
        # create Ophase - should be active
        o1 = Ophase.objects.create(start_date=date(2014, 4, 7), end_date=date(2014, 4, 11), is_active=True)
        self.assertEqual(o1.is_active, True)
        # now create other Ophase - should be active while first one should be inactive
        o2 = Ophase.objects.create(start_date=date(2014, 10, 6), end_date=date(2014, 10, 10), is_active=True)
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

class OphaseBeginBeforeEnd(TestCase):
    """Ensure that an Ophase does not end before it begins."""

    def test_fail_on_wrong(self):
        o = Ophase.objects.create(start_date=date(2014, 4, 8), end_date=date(2014, 4, 1))
        self.assertRaises(ValidationError, o.clean)

    def test_pass_on_right(self):
        try:
            o = Ophase.objects.create(start_date=date(2014, 4, 1), end_date=date(2014, 4, 5))
            o.clean()
        except ValidationError:
            self.fail("Creation of Ophase raised ValidationError unexpectedly.")
