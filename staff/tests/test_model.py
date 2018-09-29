from django.test import TestCase

from ophasebase.models import Ophase
from staff.models import Person

from pyTUID.models import TUIDUser

class StaffModelTests(TestCase):
    def setUp(self):
        self.ophase = Ophase.objects.create(name="Testophase", is_active=True)

    def test_delete(self):
        """ On delete of a person object all TUIDs which are not referenced by a person object are deleted """
        tid = TUIDUser.objects.create(uid="ab42cdef", surname="John",
                                      given_name="Doe", email="john@example.net", groups="Test")

        tid2 = TUIDUser.objects.create(uid="bb42defa", surname="John",
                                given_name="Doe", email="john@example.net", groups="Test")

        TUIDUser.objects.create(uid="ab42defg", surname="John",
                                given_name="Doe", email="john@example.net", groups="Test")

        TUIDUser.objects.create(uid="ab42defh", surname="John",
                                given_name="Doe", email="john@example.net", groups="Test")

        self.assertEqual(4, TUIDUser.objects.count())

        p = Person.objects.create(prename="John", name="Doe", email="john2@example.net", phone="0123456789",
                              matriculated_since="2011", degree_course="B.Sc.", is_tutor=True, tuid=tid)

        Person.objects.create(prename="John", name="Doe", email="john@example.net", phone="0123456789",
                              matriculated_since="2011", degree_course="B.Sc.", is_tutor=True, tuid=tid2)

        # A person which dose not have a tuid associated
        Person.objects.create(prename="John", name="Doe2", email="john3@example.net", phone="0123456789",
                              matriculated_since="2011", degree_course="B.Sc.")

        p.delete()

        self.assertEqual(1, TUIDUser.objects.count())