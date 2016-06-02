from django.test import TestCase

from django.contrib.auth.models import User, Permission

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from students.models import Newsletter

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class StudentSeleniumTests(StaticLiveServerTestCase):
    fixtures = ['ophasebase.json', 'staff.json', 'students.json']

    @classmethod
    def setUpClass(cls):
        super(StudentSeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(StudentSeleniumTests, cls).tearDownClass()
        
    def setUp(self):
        # Create the second newsletter
        news2 = Newsletter.objects.create(name='Number 2', description='Just a test', active=True)
        news2.save()

    def test_show_hide_email(self):
        """Test that showing and hiding of the email field for students"""

        # Create the testuser
        __testuser = 'testuser'
        __testpw = 'test'
        
        u = User.objects.create_user(username=__testuser,
                    password=__testpw,
                    email='test@example.com')

        add_perm = Permission.objects.get(codename='add_student')
        u.user_permissions.add(add_perm)
        u.save()
    
        # Start Selenium Test
        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, '/teilnehmer/'))
        
        # first login
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(__testuser)
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(__testpw)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        
        # Intial the email field is hidden
        self.assertFalse(driver.find_element_by_id("id_email").get_attribute("required"))
        self.assertFalse(driver.find_element_by_id("id_email").is_displayed())
        
        # The user want a newsletter show the field
        driver.find_element_by_id("id_newsletters_0").click()
        self.assertTrue(driver.find_element_by_id("id_email").get_attribute("required"))
        self.assertTrue(driver.find_element_by_id("id_email").is_displayed())
        driver.find_element_by_id("id_email").clear()
        # User input
        driver.find_element_by_id("id_email").send_keys("hallo@")
        self.assertEqual("hallo@", driver.find_element_by_id("id_email").get_attribute("value"))
        
        # But then change his mind so hide the field
        driver.find_element_by_id("id_newsletters_0").click()
        self.assertFalse("", driver.find_element_by_id("id_email").get_attribute("required"))
        self.assertFalse(driver.find_element_by_id("id_email").is_displayed())
        
        # Then change his mind again so show the field but no data should be there
        driver.find_element_by_id("id_newsletters_0").click()
        self.assertTrue(driver.find_element_by_id("id_email").get_attribute("required"))
        self.assertEqual("", driver.find_element_by_id("id_email").get_attribute("value"))
        self.assertTrue(driver.find_element_by_id("id_email").is_displayed())
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("hallo@")
        self.assertEqual("hallo@", driver.find_element_by_id("id_email").get_attribute("value"))
        
        # Lets get a second newsletter
        driver.find_element_by_id("id_newsletters_1").click()
        self.assertTrue(driver.find_element_by_id("id_email").get_attribute("required"))
        self.assertEqual("hallo@", driver.find_element_by_id("id_email").get_attribute("value"))
        self.assertTrue(driver.find_element_by_id("id_email").is_displayed())
        
        # but not the first one 
        driver.find_element_by_id("id_newsletters_0").click()
        self.assertTrue(driver.find_element_by_id("id_email").get_attribute("required"))
        self.assertEqual("hallo@", driver.find_element_by_id("id_email").get_attribute("value"))
        self.assertTrue(driver.find_element_by_id("id_email").is_displayed())
        
        # and not the second one
        driver.find_element_by_id("id_newsletters_1").click()
        self.assertFalse(driver.find_element_by_id("id_email").is_displayed())
        self.assertFalse(driver.find_element_by_id("id_email").get_attribute("required"))
        
        # oh a mistake but the data should not be there
        driver.find_element_by_id("id_newsletters_1").click()
        self.assertTrue(driver.find_element_by_id("id_email").get_attribute("required"))
        self.assertEqual("", driver.find_element_by_id("id_email").get_attribute("value"))
        self.assertTrue(driver.find_element_by_id("id_email").is_displayed())
        
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
