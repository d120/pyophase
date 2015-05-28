from django.test import TestCase
from datetime import date

from ophasebase.models import Ophase
from staff.models import Person, DressSize

# Create your tests here.

class PersonSave(TestCase):
    """Ensure Person is created with active Ophase as ForeignKey."""

    def test_person_foreign_key_ophase(self):
        # create Person with an active Ophase
        Ophase.objects.create(start_date=date(2014, 4, 7), end_date=date(2014, 4, 11), is_active=True)
        d = DressSize.objects.create(name="S", sort_key=0)
        p = Person.objects.create(prename="John", name="Doe", email="john@example.net", phone="0123456789", matriculated_since="2011", degree_course="B.Sc.", is_tutor=True, dress_size=d)
        self.assertEqual(p.ophase.start_date, date(2014, 4, 7))
        # create another Ophase which is active (i.e. old Ophase becomes inactive) and update old Person
        # Ophase ForeignKey should stay the same as before!
        Ophase.objects.create(start_date=date(2014, 10, 6), end_date=date(2014, 10, 10), is_active=True)
        p.email = "doe@example.net"
        p.save()
        p = Person.objects.get(pk=p.pk)
        self.assertEqual(p.ophase.start_date, date(2014, 4, 7))
        self.assertEqual(p.email, "doe@example.net")
