from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10
path = "/mnt/c/Users/65848/documents/projects/pytest/geckodriver.exe"


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path=path)

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # John heard of this cool todo app so he enter the url to the homepage
        self.browser.get(self.live_server_url)

        # He notices the the title named To-Do to confirm
        # he is at the right url
        self.assertIn('To-Do', self.browser.title)

        # He is prompted to enter a to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Complete CS50" into a text box
        inputbox.send_keys('Complete CS50')

        # When he hits enter, the page updates and now the page lists:
        # 1: Complete CS50 in his to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Complete CS50')

        # There is another text box prompting him to enter another
        # to-do item, he enters 'Complete TDD With Django'
        # and now the page list both items

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Complete TDD With Django')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.wait_for_row_in_list_table('1: Complete CS50')
        self.wait_for_row_in_list_table('2: Complete TDD With Django')

        # He wonders if the web app will remember his list, he
        # then sees that the site has generated a unique url for him

        # He visited the site again and saw his list is still there

        # He then turn off his laptop, satisfied

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # John starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Complete CS50')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Complete CS50')

        # He notices that his list has a unique URL
        john_list_url = self.browser.current_url
        self.assertRegex(john_list_url, '/lists/.+')

        # A new user Tom comes along

        # We use a new browser to make sure no information of John's list is
        # stored eg cookies or sessions
        self.browser.quit()
        self.browser = webdriver.Firefox(executable_path=path)

        # Tom visited the home page and there is no sign of John's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Complete CS50', page_text)

        # Tom starts a new list by entering a new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Complete Math Homework')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Complete Math Homework')

        # Tom get his own unique url
        tom_list_url = self.browser.current_url
        self.assertRegex(tom_list_url, '/lists/.+')
        self.assertNotEqual(tom_list_url, john_list_url)
        
        # Again, there isnt any trace of John's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Complete CS50', page_text)
        self.assertIn('1: Complete Math Homework', page_text)