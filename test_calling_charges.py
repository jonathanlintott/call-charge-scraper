__author__ = 'Jonathan Lintott'

# Standard library imports
import unittest

# Web scraping imports
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# Local imports
from calling_charges import OTwoPage, fetch_external_info


class CallingChargeSearch(unittest.TestCase):
    """
    For testing of the calling charge scraping script in 'calling_charges.py'
    """
    def setUp(self):
        # Set up webdriver to use local installation of firefox
        binary = FirefoxBinary('C:/Users/jli199/AppData/Local/Mozilla Firefox/firefox.exe')
        self.driver = webdriver.Firefox(firefox_binary=binary)

    def test_calling_charges_scrape(self):
        url, countries = fetch_external_info()

        # Test url and countries have loaded correctly
        assert isinstance(url, str) and len(url)>0, 'url not loaded correctly'
        assert isinstance(countries, list) and len(countries)>0, 'countries not loaded ' \
                                                                 'correctly'

        # Test OTwoPage loads the url correctly
        page = OTwoPage(self.driver, url, countries)
        assert page.get_current_url() == url

        # Test OTwoPage can find country element and return a cost
        cost1 = page.get_country_call_price('Germany')
        assert cost1 == 150

        # Test error catching works
        cost2 = page.get_country_call_price('Lovelyland')
        assert cost2 is None

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    # Run tests defined within this script
    unittest.main()

