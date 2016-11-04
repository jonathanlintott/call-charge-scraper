__author__ = 'Jonathan Lintott'

# Standard library imports
import unittest

# Web scraping imports
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class CallingChargeSearch(unittest.TestCase):
    """
    For testing of the calling charge scraping script in 'calling_charges.py'
    """
    def setUp(self):
        binary = FirefoxBinary('C:/Users/jli199/AppData/Local/Mozilla Firefox/firefox.exe')
        self.driver = webdriver.Firefox(firefox_binary=binary)

    def test_wait(self):
        self.driver.get('http://www.python.org')

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    # Run tests defined within this script
    unittest.main()

