from datetime import date

from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

from ophasebase.models import Ophase
from staff.models import Person


class MailExport(TestCase):
    def setUp(self):
        # Create the testuser
        self.__testuser = 'testuser'
        self.__testpw = 'test'

        u = User.objects.create_superuser(username=self.__testuser,
                                     password=self.__testpw,
                                     email='test@example.com')

        u.save()

    def test_export(self):
        Ophase.objects.create(start_date=date(2014, 4, 7), end_date=date(2014, 4, 11), is_active=True)
        Person.objects.create(prename="John", name="Doe", email="john@example.net", phone="0123456789", matriculated_since="2011", degree_course="B.Sc.", is_tutor=True)

        Person.objects.create(prename="John", name="Doe", email="john@example.com", phone="0123456789", matriculated_since="2011", degree_course="B.Sc.", is_tutor=True)

        c = Client()

        # login returns True on success
        self.assertTrue(c.login(username=self.__testuser, password=self.__testpw))

        # the url of the view
        change_url = reverse('admin:staff_person_changelist')

        self.assertEqual(len(mail.outbox), 0)
        users = [1, 2]
        response = c.post(change_url, {'action': 'mail_export',
                                       '_selected_action': users},
                          follow=True)
        self.assertEqual(response.status_code, 200)

class SendFillformMail(TestCase):
    fixtures = ['ophasebase.json', 'staff.json', 'students.json', 'persons.json']

    def setUp(self):
        # Create the testuser
        self.__testuser = 'testuser'
        self.__testpw = 'test'

        u = User.objects.create_superuser(username=self.__testuser,
                                     password=self.__testpw,
                                     email='test@example.com')

        u.save()

    def test_send_fillform_email(self):
        """Sends Fillform information to a set of users"""
        c = Client()

        # login returns True on success
        self.assertTrue(c.login(username=self.__testuser, password=self.__testpw))

        # the url of the view
        change_url = reverse('admin:staff_person_changelist')

        self.assertEqual(len(mail.outbox), 0)
        recipient = [5, 6, 7]
        response = c.post(change_url, {'action': 'send_fillform_mail',
                                       '_selected_action': recipient},)
        
        # If the post work we get to the confirmation page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/fillform_email_confirm.html')

        # Send the post again with confirmation
        response = c.post(change_url, {'action': 'send_fillform_mail',
                                       'post': 'yes',
                                       '_selected_action': recipient},
                          follow=True)

        # If the post work we get back to the changelist via a redirect
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, change_url)

        # One email per recipient was sent
        self.assertEqual(len(mail.outbox), len(recipient))
        # Registerview url is in the email message body
        self.assertTrue(reverse('staff:registration') in mail.outbox[0].body)

        # that the message was displayed to the admin
        msgs = list(response.context['messages'])
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0].level, messages.SUCCESS)
