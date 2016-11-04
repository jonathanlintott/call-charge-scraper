__author__ = 'Jonathan Lintott'


# Standard library imports
import sys
import json

# Web scraping imports
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

class BasePage(object):

    def __init__(self, driver, url, countries):
        self.driver = driver
        self.countries = countries

        self.driver.get(url)

    def get_current_url(self):
        """
        Returns the current url as a string
        """
        return self.driver.current_url


class OTwoPage(BasePage):

    def get_country_call_price(self, country, contract_type='pay monthly', receiver_type='landline'):
        """
        Scrapes the page to find the price of calling that country in pence sterling.

        Parameters
        ----------
        country : string
            Name of country to call
        contract_type : string
            Either 'pay monthly' or 'pay as you go'
        receiver_type : string
            Either 'landline' or 'mobile'

        Returns
        -------
        Float, cost of call in pence sterling.
        """
        driver = self.driver

        content_element = driver.find_element_by_xpath("//div[@id='content']")

        country_element = content_element.find_element_by_xpath("//input[@id='countryName']")

        # Enter country name
        country_element.clear()
        country_element.send_keys(country)
        country_element.send_keys(Keys.RETURN)

        price_element = WebDriverWait(content_element, 10).until(
            EC.presence_of_element_located((By.ID, 'landLine'))
        )


def fetch_external_info():
    """
    Fetches url and country list and returns them

    Returns
    -------
    Tuple of (url as string, countries as list of strings)
    """

    # Opens 'charges_url.txt' and gets url as string
    with open('charges_url.txt', 'r') as url_file:
        url = url_file.readline()

    # Opens 'countries.txt' and gets countries as a list of strings
    with open('countries.txt', 'r') as countries_file:
        countries = json.load(countries_file)

    return url, countries


# Accepts a webdriver instance and preforms the web scraping
def main(driver):
    url, countries = fetch_external_info()

    page = OTwoPage(driver, url, countries)

    page.get_country_call_price('Germany')


if __name__ == '__main__':
    from selenium import webdriver
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    from selenium.common.exceptions import WebDriverException

    # Default webdriver is firefox
    # Will allow user to set a specific binary location if desired
    if len(sys.argv) > 1:
        binary = FirefoxBinary(sys.argv[1])
    else:
        binary = None

    try:
        driver = webdriver.Firefox(firefox_binary=binary)
    except WebDriverException as e:
        print(e)
    else:
        main(driver)
        # driver.close()

    if False:
        from selenium import webdriver
        from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        binary = FirefoxBinary('C:/Users/jli199/AppData/Local/Mozilla Firefox/firefox.exe')
        driver = webdriver.Firefox(firefox_binary=binary)
        url, _ = fetch_external_info()
        driver.get(url)
        content_element = driver.find_element_by_xpath("//div[@id='content']")

        country_element = content_element.find_element_by_xpath("//input[@id='countryName']")
        country_element.clear()
        country_element.send_keys('Germany')
        country_element.send_keys(Keys.RETURN)

        element = WebDriverWait(content_element, 10).until(
            EC.presence_of_element_located((By.ID, 'landLine'))
        )