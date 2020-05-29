from django.contrib.auth.models import User
from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _


class StaffAddView(TestCase):
    fixtures = ['ophasebase.json', 'staff.json', 'students.json']

    def setUp(self):
        self.username = 'testuser'
        self.password = 'secret'
        self.credentials = {
            'username': self.username,
            'password': self.password}
        User.objects.create_user(**self.credentials)

    def test_redirect(self):
        """Test for Redirect to SSO Login page"""
        c = Client()
        suffix = urlencode({"next": reverse('staff:registration')})
        redirect_url = "{}?{}".format(reverse('tuid_login'), suffix)

        response = c.get(reverse('staff:registration'))

        self.assertRedirects(response, redirect_url, target_status_code=302)

    def test_send_email(self):
        """Sending an email after successfull register"""
        c = self.client
        c.login(username=self.username, password=self.password)

        register_view = reverse('staff:registration')

        self.assertEqual(len(mail.outbox), 0)

        testdata = {'prename': 'Leah',
                    'name': 'Bayer',
                    'email': 'leah.bayer@example.com',
                    'phone': '016031368212',
                    'matriculated_since': 'today',
                    'degree_course': 'Bachelor',
                    'experience_ophase': 'Nothing until now',
                    'is_helper': True,
                    'helper_jobs': 1, }

        response = c.get(register_view)
        self.assertEqual(response.status_code, 200)

        # sending a incomplet form should not send a email
        response = self.client.post(register_view, testdata, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'why_participate', _('This field is required.'))

        self.assertEqual(len(mail.outbox), 0)

        # a complete form should send one email
        testdata['why_participate'] = 'You need testdata'

        response = self.client.post(register_view, testdata, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [(reverse('staff:registration_success'), 302)])

        self.assertEqual(len(mail.outbox), 1)
        smail = mail.outbox[0]
        self.assertEqual(len(smail.to), 1)
        self.assertEqual(smail.to[0], 'Leah Bayer <leah.bayer@example.com>')
