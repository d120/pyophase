from datetime import date

from django.contrib.auth.models import Permission, User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from ophasebase.models import Ophase
from staff.models import TutorGroup


class StudentAddViewTest(TestCase):
    fixtures = ['ophasebase.json', 'staff.json', 'students.json']

    def setUp(self):
        # Create the testuser
        self.__testuser = 'testuser'
        self.__testpw = 'test'

        u = User.objects.create_user(username=self.__testuser,
                                     password=self.__testpw,
                                     email='test@example.com')

        add_perm = Permission.objects.get(codename='add_student')
        u.user_permissions.add(add_perm)
        u.save()

    def test_register_student(self):
        """Test the registration for students"""
        c = Client()

        register_view = reverse('students:registration')

        response = c.get(register_view)
        # check for login redirect
        self.assertEqual(response.status_code, 302)

        # login returns True on success
        self.assertTrue(c.login(username=self.__testuser, password=self.__testpw))

        # Delete the Ophase from fixtures
        Ophase.current().delete()

        response = c.get(register_view)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ophase_title'], 'Ophase')
        self.assertEqual(response.context['student_registration_enabled'], False)

        # Create a ophase object
        o1 = Ophase.objects.create(
            start_date=date(2014, 4, 7), end_date=date(2014, 4, 11), is_active=True)

        response = c.get(register_view)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ophase_title'], str(o1))
        self.assertEqual(response.context['student_registration_enabled'], True)

        # create a GroupCategory
        gc = GroupCategory.objects.create(label="Super Mario")
        self.assertEqual(gc.label, "Super Mario")

        # create a TutorGroup
        tg = TutorGroup.objects.create(ophase=o1, name="Mario", group_category=gc)
        self.assertEqual(tg.name, "Mario")

        response = c.post(register_view, {'prename': 'John',
                                            'name': 'Doe',
                                            'tutor_group': tg.pk,
                                            'want_exam': True,},
                          follow=True)

        # we should get redirected to the success view
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/teilnehmer/success/', 302)])

        # second user to register. request form only
        response = c.get(register_view)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ophase_title'], str(o1))
        self.assertEqual(response.context['student_registration_enabled'], True)

        # check that setting the tutorgroup of the last user as inital data works
        self.assertEqual(response.context['form']['tutor_group'].value(), str(tg.pk))

        # this user wants some newsletters but forgot to set his email
        response = c.post(register_view, {'prename': 'Ronald',
                                          'name': 'Jones',
                                          'tutor_group': tg.pk,
                                          'want_exam': False,
                                          'newsletters': [1]},
                          follow=True)

        # a error should be rased
        self.assertFormError(response, 'form', 'email',
              _('Um Newsletter zu abonnieren muss eine E-Mail-Adresse angegeben werden.'))

        # adding the email address
        response = c.post(register_view, {'prename': 'Ronald',
                                          'name': 'Jones',
                                          'email': 'RonaldJones@example.com',
                                          'tutor_group': tg.pk,
                                          'want_exam': False,
                                          'newsletters': [1]},
                          follow=True)

        # we should get redirected to the success view
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/teilnehmer/success/', 302)])


    def test_register_student_success(self):
        """Test the success view without a registration"""

        # Delete the Ophase from fixtures
        Ophase.current().delete()

        c = Client()

        # Test whitout a ophase object
        response = c.get(reverse('students:registration_success'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ophase_title'], 'Ophase')

        # Create a ophase object
        o1 = Ophase.objects.create(
            start_date=date(2014, 4, 7), end_date=date(2014, 4, 11), is_active=True)

        response = c.get(reverse('students:registration_success'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ophase_title'], str(o1))
