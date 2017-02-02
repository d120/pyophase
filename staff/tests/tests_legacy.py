from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase, tag
from django.utils.safestring import SafeText
from selenium.common.exceptions import (
    NoAlertPresentException,
    NoSuchElementException,
)
from selenium.webdriver.firefox.webdriver import WebDriver

from ophasebase.models import Ophase
from staff.forms import PersonForm
from staff.models import Person


# Create your tests here.

class PersonSave(TestCase):
    """Ensure Person is created with active Ophase as ForeignKey."""

    def test_person_foreign_key_ophase(self):
        # create Person with an active Ophase
        Ophase.objects.create(name="Testophase 1", is_active=True)
        p = Person.objects.create(prename="John", name="Doe", email="john@example.net", phone="0123456789", matriculated_since="2011", degree_course="B.Sc.", is_tutor=True)
        self.assertEqual(p.ophase.name, "Testophase 1")
        # create another Ophase which is active (i.e. old Ophase becomes inactive) and update old Person
        # Ophase ForeignKey should stay the same as before!
        Ophase.objects.create(name="Testophase 2", is_active=True)
        p.email = "doe@example.net"
        p.save()
        p = Person.objects.get(pk=p.pk)
        self.assertEqual(p.ophase.name, "Testophase 1")
        self.assertEqual(p.email, "doe@example.net")
        self.assertEqual(p.get_fillform(), '#fillform&v=1&prename=John&'\
            'name=Doe&email=doe%40example.net&phone=0123456789'\
            '&matriculated_since=2011&degree_course=B.Sc.')


class PersonSaveDuplicate(TransactionTestCase):
    """A Person can register only once per ophase instance"""
    def test_person_register_once_per_ophase(self):
        o1 = Ophase.objects.create(name="Testophase 1", is_active=True)
        p = Person.objects.create(prename="John", name="Doe", email="john@example.net", phone="0123456789", matriculated_since="2011", degree_course="B.Sc.", is_tutor=True)
        with self.assertRaises(IntegrityError):
            p2 = Person.objects.create(prename="John", name="Doe", email="john@example.net", phone="0123456789", matriculated_since="2011", degree_course="B.Sc.", is_tutor=True)

        o2 = Ophase.objects.create(name="Testophase 2", is_active=True)
        o1 = Ophase.objects.get(pk=o1.pk)
        self.assertEqual(o2.is_active, True)
        self.assertEqual(o1.is_active, False)

        p3 = Person.objects.create(prename="John", name="Doe", email="john@example.net", phone="0123456789", matriculated_since="2011", degree_course="B.Sc.", is_tutor=True)
        self.assertEqual(p3.ophase, o2)


class AppendDescriptionTestCase(TestCase):
    """Test append of a link to a field Label"""

    def test_appendend_label_is_safe(self):
        """Test all labels that get appended a link are of type SafeText"""
        pf = PersonForm()
        #after __init__ the link was appended
        for field in ['tutor_for', 'orga_jobs', 'helper_jobs']:
            self.assertTrue(isinstance(pf.fields[field].label, SafeText),
                             field)
        #Other labels are not of type SafeText
        self.assertFalse(isinstance(pf.fields['name'].label, SafeText))

class StaffSeleniumTests(StaticLiveServerTestCase):
    fixtures = ['ophasebase.json', 'staff.json', 'students.json']

    @classmethod
    def setUpClass(cls):
        super(StaffSeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(StaffSeleniumTests, cls).tearDownClass()


    @tag('selenium')
    def test_fillform(self):
        """Test fillform with all possible fields"""
        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, '/mitmachen/#fillform&v=1&prename=Thorsten&name=Freitag&email=ThorstenFreitag@example.com&phone=0151911860119&matriculated_since=2010&degree_course=Bachelor&experience_ophase=I%20did%20something.%0ALet%20me%20do%20more.&why_participate=Because%20I%20can%20and%20want%20do%20to%20more.&remarks=Some%20remark%20better%20then%20nothing.'))
        self.assertEqual("Thorsten", driver.find_element_by_id("id_prename").get_attribute("value"))
        self.assertEqual("Freitag", driver.find_element_by_id("id_name").get_attribute("value"))
        self.assertEqual("ThorstenFreitag@example.com", driver.find_element_by_id("id_email").get_attribute("value"))
        self.assertEqual("0151911860119", driver.find_element_by_id("id_phone").get_attribute("value"))
        self.assertEqual("2010", driver.find_element_by_id("id_matriculated_since").get_attribute("value"))
        self.assertEqual("Bachelor", driver.find_element_by_id("id_degree_course").get_attribute("value"))
        self.assertEqual("I did something.\nLet me do more.", driver.find_element_by_id("id_experience_ophase").get_attribute("value"))
        self.assertEqual("Because I can and want do to more.", driver.find_element_by_id("id_why_participate").get_attribute("value"))
        self.assertEqual("Some remark better then nothing.", driver.find_element_by_id("id_remarks").get_attribute("value"))

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
