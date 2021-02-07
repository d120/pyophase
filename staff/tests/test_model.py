from django.test import TestCase

from ophasebase.models import Ophase
from staff.models import Person


class StaffModelTests(TestCase):
    def setUp(self):
        self.ophase = Ophase.objects.create(name="Testophase", is_active=True)

    def test_delete(self):
        """ On delete of a person object all TUIDs which are not referenced by a person object are deleted """
        p = Person.objects.create(prename="John", name="Doe", email="john2@example.net",
                                  phone="0123456789",
                                  matriculated_since="2011", degree_course="B.Sc.", is_tutor=True)

        Person.objects.create(prename="John", name="Doe", email="john@example.net",
                              phone="0123456789",
                              matriculated_since="2011", degree_course="B.Sc.", is_tutor=True)

        # A person which dose not have a tuid associated
        Person.objects.create(prename="John", name="Doe2", email="john3@example.net",
                              phone="0123456789",
                              matriculated_since="2011", degree_course="B.Sc.")

        self.assertEqual(3, Person.objects.count())

        p.delete()

        self.assertEqual(2, Person.objects.count())

        self.ophase.delete()

        self.assertEqual(0, Person.objects.count())
