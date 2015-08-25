from django.test import TestCase

from datetime import date

from students.models import Student, TutorGroup
from staff.models import GroupCategory
from ophasebase.models import Ophase

# Create your tests here.

class StudentSave(TestCase):
    def setUp(self):
        self.o1 = Ophase.objects.create(start_date=date(2014, 4, 7), end_date=date(2014, 4, 11), is_active=True)

        self.gc = GroupCategory.objects.create(label="Super Mario")
        self.assertEqual(self.gc.label, "Super Mario")

        self.tg = TutorGroup.objects.create(ophase=self.o1, name="Mario", group_category=self.gc)
        self.assertEqual(self.tg.name, "Mario")

        self.st = Student(prename="John", name="Doe", email="john@example.net",
            tutor_group=self.tg, want_exam=True, want_newsletter=False)

    def test_drop_not_needed_student_data(self):
        """Ensure Student email address is removed if newsletter is not wanted."""

        self.assertEqual(self.st.email, "john@example.net")
        self.assertEqual(self.st.want_newsletter, False)

        self.st.save()
        #check after Student is created in the db
        self.assertEqual(self.st.want_newsletter, False)
        self.assertEqual(self.st.email, '')

        self.st.email = "doe@example.net"
        self.assertEqual(self.st.email, "doe@example.net")
        self.assertEqual(self.st.want_newsletter, False)
        self.st.save()

        #check after Student is update in the db
        self.assertEqual(self.st.want_newsletter, False)
        self.assertEqual(self.st.email, '')

    def test_student_foreign_key_ophase(self):
        """Ensure Student is created with active Ophase as ForeignKey."""
        # create Student with an active Ophase
        self.st.save()
        self.assertEqual(self.st.ophase.start_date, date(2014, 4, 7))
        # create another Ophase which is active (i.e. old Ophase becomes inactive) and update old Person
        # Ophase ForeignKey should stay the same as before!
        Ophase.objects.create(start_date=date(2014, 10, 6), end_date=date(2014, 10, 10), is_active=True)
        self.o1.is_active = False
        self.o1.save()

        self.st.want_newsletter = True
        self.st.email = "doe@example.net"
        self.st.save()
        st = Student.objects.get(pk=self.st.pk)
        self.assertEqual(st.ophase.start_date, date(2014, 4, 7))
        self.assertEqual(st.email, "doe@example.net")
