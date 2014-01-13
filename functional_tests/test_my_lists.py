from django.conf import settings
from .base import FunctionalTest
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

WAIT_ = 3

class MyListsTest(FunctionalTest):

	def create_pre_authenticated_session(self):
		if self.against_staging:
			session_key = create_session_on_server(self.server_host)
		else:
			session_key = create_pre_authenticated_session()
		## to set a cookie we need to first visit the domain.
		## 404 pages load the quickest!
		self.browser.get(self.server_url + "/404_no_such_url/")
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session_key,
			path='/',
		))
		print(self.browser.get_cookies())

	def wait_for_element_with_id(self, element_id):
		WebDriverWait(self.browser, timeout=15).until(
			lambda b: b.find_element_by_id(element_id)
		)
		
	def wait_for_element_with_link_text(self, text):
		WebDriverWait(self.browser, timeout=15).until(
			lambda b: b.find_element_by_link_text(text)
		)
	
	def wait_here(self, wait_message):
		print('starting wait - %s' % (wait_message,))
		time.sleep(WAIT_)
		print('ending wait')
		
	def test_logged_in_users_lists_are_saved_as_my_lists(self):
		# Edith is a logged in user
		self.create_pre_authenticated_session()

		# She goes to the home page and starts a list
		self.browser.get(self.server_url)
		self.get_item_input_box().click() # added this as text and or \n was not being submitted
		
		self.get_item_input_box().send_keys('Reticulate splines\n')
		self.wait_for_element_with_id('id_text')

		self.get_item_input_box().click() # added this as text and or \n was not being submitted
		
		self.get_item_input_box().send_keys('Immanentize eschaton\n')
		
		first_list_url = self.browser.current_url
				
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
		self.wait_for_element_with_id('id_logout')	
		self.wait_here('after clicking log out')
		
		# She logs out.  The "My lists" option disappears
		self.browser.find_element_by_id('id_logout').click()
		
		self.wait_for_element_with_id('id_login')		
		self.assertEqual(
		    self.browser.find_elements_by_link_text('My lists'),
		    []
        	)
