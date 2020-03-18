from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        path = "/mnt/c/Users/65848/documents/projects/pytest/geckodriver.exe"
        self.browser = webdriver.Firefox(executable_path=path)
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # John heard of this cool todo app so he enter the url to the homepage
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            # List comprehension to return true or false, then any return it
            # as boolean
            any(rows.text == '1: Complete CS50' for row in rows)
        )

        # There is another text box prompting him to enter another
        # to-do item

        # He wonders if the web app will remember his list, he
        # then sees that the site has generated a unique url for him

        # He visited the site again and saw his list is still there

        # He then turn off his laptop, satisfied
        self.fail('Finish the test!')


if __name__ == "__main__":
    unittest.main()