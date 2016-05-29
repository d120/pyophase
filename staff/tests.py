from django.test import TestCase
from django.utils.safestring import SafeText

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from datetime import date

from ophasebase.models import Ophase
from staff.models import Person, DressSize
from staff.forms import PersonForm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

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

class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['ophasebase.json', 'staff.json', 'students.json', 'exam.json']

    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_dependent_visibility_two(self):
        driver = self.selenium
        driver.get(self.live_server_url + "/mitmachen/")
        self.assertFalse(driver.find_element_by_id("id_tutor_for").is_displayed())
        self.assertFalse(driver.find_element_by_xpath("//div[@id='mainForm']/form/div[12]").is_displayed())
        self.assertFalse(driver.find_element_by_xpath("//div[@id='mainForm']/form/div[14]").is_displayed())
        self.assertFalse(driver.find_element_by_id("id_dress_size").is_displayed())
        driver.find_element_by_id("id_is_tutor").click()
        self.assertTrue(driver.find_element_by_id("id_tutor_for").is_displayed())
        self.assertTrue(driver.find_element_by_id("id_dress_size").is_displayed())
        Select(driver.find_element_by_id("id_tutor_for")).select_by_visible_text("Bachelor")
        # ERROR: Caught exception [ERROR: Unsupported command [getSelectedLabel | id=id_tutor_for | ]]
        driver.find_element_by_id("id_is_orga").click()
        self.assertTrue(driver.find_element_by_id("id_dress_size").is_displayed())
        self.assertTrue(driver.find_element_by_xpath("//div[@id='mainForm']/form/div[12]").is_displayed())
        driver.find_element_by_id("id_orga_jobs_0").click()
        self.assertTrue(driver.find_element_by_id("id_orga_jobs_0").is_selected())
        self.assertTrue(driver.find_element_by_id("id_dress_size").is_displayed())
        Select(driver.find_element_by_id("id_dress_size")).select_by_visible_text("S")
        # ERROR: Caught exception [ERROR: Unsupported command [getSelectedLabel | id=id_dress_size | ]]
        driver.find_element_by_id("id_is_orga").click()
        self.assertTrue(driver.find_element_by_id("id_dress_size").is_displayed())
        driver.find_element_by_id("id_is_orga").click()
        self.assertTrue(driver.find_element_by_id("id_dress_size").is_displayed())
        driver.find_element_by_id("id_is_orga").click()
        self.assertFalse(driver.find_element_by_id("id_orga_jobs_0").is_selected())
        driver.find_element_by_id("id_is_tutor").click()
        self.assertFalse(driver.find_element_by_id("id_dress_size").is_displayed())
        driver.find_element_by_id("id_is_tutor").click()
        driver.find_element_by_id("id_is_tutor").click()
        driver.find_element_by_id("id_is_helper").click()
        driver.find_element_by_id("id_helper_jobs_0").click()
        self.assertTrue(driver.find_element_by_id("id_helper_jobs_0").is_selected())
        driver.find_element_by_id("id_is_helper").click()
        self.assertFalse(driver.find_element_by_xpath("//div[@id='mainForm']/form/div[14]").is_displayed())
        driver.find_element_by_id("id_is_helper").click()
        self.assertTrue(driver.find_element_by_xpath("//div[@id='mainForm']/form/div[14]").is_displayed())
        self.assertFalse(driver.find_element_by_id("id_helper_jobs_0").is_selected())

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