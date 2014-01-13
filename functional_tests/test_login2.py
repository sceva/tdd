from .base import FunctionalTest
import sys

from django.conf import settings

from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

TEST_EMAIL = 'testinggoat@yahoo.com'
TEST_PASSWORD = 'soFNjTMqMLEtj8W4'
WAIT_ = 1

class LoginTest(FunctionalTest):
	
	# Helper functions
			
	def switch_to_new_window(self, text_in_title):
		retries = 50
		while retries > 0:
			for handle in self.browser.window_handles:
				self.browser.switch_to_window(handle)
				if text_in_title in self.browser.title:
					return
			retries -= 1
			time.sleep(0.2)
		self.fail('could not find window')
		
	def wait_for_element_with_id(self, element_id):
		WebDriverWait(self.browser, timeout=15).until(
			lambda b: b.find_element_by_id(element_id)
		)
	
	def wait_for_element_with_link_text(self, text):
		WebDriverWait(self.browser, timeout=15).until(
			lambda b: b.find_element_by_link_text(text)
		)

                
	def test_login_with_persona(self):
		# Edith goes to the awesome superlists site
		# and notices a "Sign in" ling for the first time.
		self.browser.get(self.server_url)
		self.browser.find_element_by_id('id_login').click()
		
		# A Persona login box appears
		self.switch_to_new_window('Mozilla Persona')
		self.browser.find_element_by_id('authentication_email').send_keys(TEST_EMAIL)
		self.browser.find_element_by_tag_name('button').click()
		
		# We get redirected to te Yahoo page
		self.wait_for_element_with_id('username')
		self.browser.find_element_by_id('username').send_keys(TEST_EMAIL)
		self.browser.find_element_by_id('passwd').send_keys(TEST_PASSWORD)
		self.browser.find_element_by_id('.save').click()
		
		# The Persona window closes
		self.switch_to_new_window('To-Do')
		
		# She can see that she is logged in
		self.assert_logged_in()
		
		# Refreshing the page, she sees it's a real session login,
		# not just a one-off for that page
		self.browser.refresh()
		self.assert_logged_in()
				
		# She goes to the home page and starts a list
		self.browser.get(self.server_url)
		self.get_item_input_box().click() # added this as text and or \n was not being submitted

		
		self.get_item_input_box().send_keys('Reticulate splines\n')
		self.wait_for_element_with_id('id_text')

		self.get_item_input_box().click() # added this as text and or \n was not being submitted
		
		self.get_item_input_box().send_keys('Immanentize eschaton\n')
		
		first_list_url = self.browser.current_url
		print(first_list_url)
				
		# She notices for the first time a 'My lists' link and clicks it
		self.wait_for_element_with_id('id_my_lists_link')
		
		self.browser.find_element_by_link_text('My lists').click()
		self.browser.find_element_by_link_text('My lists').click()
		
		# She see that her list is in there, named according to its
		# first list item
		self.wait_for_element_with_link_text('Reticulate splines') #
		self.browser.find_element_by_link_text('Reticulate splines').click()
		
		try:
			self.browser.find_element_by_link_text('Reticulate splines').click()
		except:
			pass
			
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, first_list_url)
		)
		
	        # She decides to start another list, just to see
		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys('Click cows\n')
		second_list_url = self.browser.current_url
		
		self.wait_for_element_with_link_text('My lists')
		
		# Under "my lists", her new list appears
		self.browser.find_element_by_link_text('My lists').click()
		self.browser.find_element_by_link_text('My lists').click()

		self.wait_for_element_with_link_text('Click cows')

		self.browser.find_element_by_link_text('Click cows').click()
		try:
			self.browser.find_element_by_link_text('Click cows').click()
		except:
			pass

		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, second_list_url)
		)
		
		# She logs out.  The "My lists" option disappears
		self.wait_for_element_with_id('id_logout')		
		time.sleep(4)
		self.browser.find_element_by_id('id_logout').click()
		
		self.wait_for_element_with_id('id_login')		
		self.assertEqual(
		    self.browser.find_elements_by_link_text('My lists'),
		    []
        	)
		
	def assert_logged_in(self, logged_in=True):
		if logged_in:
			self.wait_for_element_with_id('id_logout')
			navbar = self.browser.find_element_by_css_selector('.navbar')
			self.assertIn(TEST_EMAIL, navbar.text)
		else:
			self.wait_for_element_with_id('id_login')
			navbar = self.browser.find_element_by_css_selector('.navbar')
			self.assertNotIn(TEST_EMAIL, navbar.text)

