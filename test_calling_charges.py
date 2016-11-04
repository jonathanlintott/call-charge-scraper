__author__ = 'Jonathan Lintott'

# Standard library imports
import unittest

# Web scraping imports
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# Local imports
from calling_charges import BasePage, fetch_external_info


class CallingChargeSearch(unittest.TestCase):
    """
    For testing of the calling charge scraping script in 'calling_charges.py'
    """
    def setUp(self):
        # Set up webdriver to use local installation of firefox
        binary = FirefoxBinary('C:/Users/jli199/AppData/Local/Mozilla Firefox/firefox.exe')
        self.driver = webdriver.Firefox(firefox_binary=binary)

    def test_external_info_load(self):
        url, countries = fetch_external_info()

        assert isinstance(url, str) and len(url)>0, 'url not loaded correctly'
        assert isinstance(countries, list) and len(countries)>0, 'countries not loaded ' \
                                                                 'correctly'

    def test_BasePage(self):
        url, countries = fetch_external_info()

        page = BasePage(self.driver, url, countries)

        assert page.get_current_url() == url

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    # Run tests defined within this script
    unittest.main()

