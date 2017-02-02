from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from ophasebase.models import Ophase, OphaseCategory
from staff.models import TutorGroup
from students.models import Newsletter, Settings, Student


class NewsletterModelTests(TestCase):
    def test_newsletter_create(self):
        """Ensure creating of newsletter object works"""
        # check that there is no newsletter at the beginning
        self.assertEqual(Newsletter.objects.count(), 0)

        # first newsletter Object
        n1 = Newsletter(name='Test Newsletter',
                        description='This newsletter is only for test')
        n1.save()

        # check that the newsletter is stored
        self.assertEqual(Newsletter.objects.count(), 1)

        # check that save do only store the data
        self.assertEqual(n1.name, 'Test Newsletter')
        self.assertEqual(n1.description, 'This newsletter is only for test')

        # Check that the default of active is True
        self.assertEqual(n1.active, True)

        # Check that get return the same object
        n1_get = Newsletter.objects.all()[0]
        self.assertEqual(n1, n1_get)

        # check __str__
        self.assertEqual(n1.__str__(),
                         'Test Newsletter - This newsletter is only for test')

        n2 = Newsletter(name='The new letter',
                        description='another fu bar',
                        active=False)

        n2.save()

        # check that the newsletter is stored
        self.assertEqual(Newsletter.objects.count(), 2)

        # check that save do only store the data
        self.assertEqual(n2.name, 'The new letter')
        self.assertEqual(n2.description, 'another fu bar')
        self.assertEqual(n2.active, False)

        # check that they both are different
        self.assertNotEqual(n1, n2)

    def test_newsletter_modify(self):
        """Ensure modifying of a newsletter object works"""
        # check that there is no newsletter at the beginning
        self.assertEqual(Newsletter.objects.count(), 0)

        # first newsletter Object
        n1 = Newsletter(name='Test Newsletter',
                        description='This newsletter is only for test')
        n1.save()

        # check that save do only store the data
        self.assertEqual(n1.name, 'Test Newsletter')
        self.assertEqual(n1.description, 'This newsletter is only for test')

        # Check that the default of active is True
        self.assertEqual(n1.active, True)

        # Change the data
        n1.name = 'New Name'
        n1.description = 'some description'
        n1.active = False
        n1.save()

        # check that save do only store the data
        self.assertEqual(n1.name, 'New Name')
        self.assertEqual(n1.description, 'some description')
        self.assertEqual(n1.active, False)


class StudentModelTests(TestCase):

    def setUp(self):
        self.o1 = Ophase.objects.create(name="Testophase 1", is_active=True)

        self.gc = OphaseCategory.objects.create(name="Super Mario")
        self.assertEqual(self.gc.name, "Super Mario")

        self.tg = TutorGroup.objects.create(
            ophase=self.o1, name="Mario", group_category=self.gc)
        self.assertEqual(self.tg.name, "Mario")

        self.st = Student(prename="John", name="Doe", email="john@example.net",
                          tutor_group=self.tg, want_exam=True)

        self.n1 = Newsletter(name='Test Newsletter',
                        description='This newsletter is only for test')

    def test_student_create(self):
        """Ensure creating of a student object works"""
        stud1 = Student.objects.create(
            prename='Cora',
            name='Nickerson',
            email='somemail@helloworld.com',
            tutor_group=self.tg,
            want_exam=True,
        )

        stud1.save()

        # check that save works
        self.assertEqual(stud1.prename, 'Cora')
        self.assertEqual(stud1.name, 'Nickerson')
        self.assertEqual(stud1.tutor_group, self.tg)
        self.assertEqual(stud1.want_exam, True)
        self.assertEqual(stud1.ophase, self.o1)

        # test __str__
        tg_string = self.tg.__str__()
        self.assertEqual(stud1.__str__(), 'Nickerson, Cora (%s)' % (tg_string))

        # The E-Mail is stored even if the student did not select any
        # newsletter
        self.assertEqual(stud1.email, 'somemail@helloworld.com')
        
        self.assertEqual(stud1.want_newsletter(), False)

        # Add a newsletter
        self.n1.save()
        stud1.newsletters.add(self.n1)
        self.assertEqual(stud1.want_newsletter(), True)
        

    def test_student_update(self):
        """Ensure update of a student object works"""

        stud1 = self.st

        stud1.save()

        # check values
        self.assertEqual(stud1.prename, 'John')
        self.assertEqual(stud1.name, 'Doe')
        self.assertEqual(stud1.email, 'john@example.net')
        self.assertEqual(stud1.tutor_group, self.tg)
        self.assertEqual(stud1.want_exam, True)
        self.assertEqual(stud1.ophase, self.o1)

        stud1.prename = 'John Peter'

        stud1.save()

        self.assertEqual(stud1.prename, 'John Peter')
        self.assertEqual(stud1.name, 'Doe')
        self.assertEqual(stud1.email, 'john@example.net')
        self.assertEqual(stud1.tutor_group, self.tg)
        self.assertEqual(stud1.want_exam, True)
        self.assertEqual(stud1.ophase, self.o1)

    def test_student_foreign_key_ophase(self):
        """Ensure Student is created with active Ophase as ForeignKey."""
        # create Student with an active Ophase
        self.st.save()
        self.assertEqual(self.st.ophase.name, "Testophase 1")
        # create another Ophase which is active (i.e. old Ophase becomes inactive) and update old Person
        # Ophase ForeignKey should stay the same as before!
        Ophase.objects.create(name="Testophase 2", is_active=True)
        self.o1.is_active = False
        self.o1.save()

        self.st.email = "doe@example.net"
        self.st.save()
        st = Student.objects.get(pk=self.st.pk)
        self.assertEqual(st.name, "Testophase 1")
        self.assertEqual(st.email, "doe@example.net")

        self.assertEqual(Student.objects.count(), 1)

        # Delete the Ophase object
        self.o1.delete()

        # The students object should be deleted too
        self.assertEqual(Student.objects.count(), 0)


class SettingsModelTests(TestCase):
    def test_settings_create(self):
        """Ensure creating of a settings object works"""
        
        self.assertEqual(Settings.objects.count(), 0)

        self.assertEqual(Settings.instance(), None)

        set = Settings(student_registration_enabled=True)
        set.save()

        self.assertEqual(Settings.objects.count(), 1)
        self.assertEqual(set.student_registration_enabled, True)

        self.assertEqual(set, Settings.instance())

        set.student_registration_enabled = False
        set.save()

        self.assertEqual(set.__str__(), _('Students Einstellungen'))

        self.assertEqual(Settings.objects.count(), 1)
        self.assertEqual(set.student_registration_enabled, False)

        set2 = Settings(student_registration_enabled=True)

        # check for validation error
        with self.assertRaises(ValidationError):
            set2.clean()
