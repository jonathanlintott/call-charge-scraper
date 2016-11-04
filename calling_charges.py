__author__ = 'Jonathan Lintott'


# Standard library imports
import sys
import json

# Web scraping imports
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def _convert_string_price_to_pence(string):
    if string[-1] == 'p':
        string = string[:-1]

    try:
        int(string[0])
    except ValueError:
        string = string[1:]

    parts = string.split('.')
    if len(parts) == 1:
        pence = int(parts[0])
    else:
        pence = int(parts[0])*100 + int(parts[1])

    return pence


class BasePage(object):

    def __init__(self, driver, url, countries):
        """
        Parameters
        ----------
        driver : webdriver instance
        url : string
            URL to retrieve call cost data from
        countries : list of strings
            Countries to retrieve call cost data for
        """
        self.driver = driver
        self.countries = countries

        self.driver.get(url)

    def get_current_url(self):
        """
        Returns the current url as a string.
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
        Int, cost of call in pence sterling.
        """
        # Set names of plan and receiver types for xpaths later on
        if contract_type.lower() == 'pay monthly':
            plan_name = 'paymonthlyTariffPlan'
        elif contract_type.lower() == 'pay as you go':
            plan_name = 'payandgoTariffPlan'
        else:
            raise ValueError('Do not recognise {} as a contract type.'.format(contract_type))

        if receiver_type.lower() == 'landline':
            receiver = 'Landline'
        elif receiver_type.lower() == 'mobile':
            receiver = 'Mobiles'
        else:
            raise ValueError('Do not recognise {} as a contract type.'.format(receiver_type))

        # Get main content element
        content_element = self.driver.find_element_by_xpath("//div[@id='content']")

        # Get country entry field element
        country_element = content_element.find_element_by_xpath("//input[@id='countryName']")

        # Enter country name
        country_element.clear()
        country_element.send_keys(country)
        country_element.send_keys(Keys.RETURN)

        # Class attribute changes to include error if country not recognised
        if 'error' in country_element.get_attribute('class'):
            return None

        # Get link to click from contract tabs once country specific data loaded
        contract_tab = WebDriverWait(content_element, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, "div[@class='tabs clearfix ui-tabs ui-widget ui-widget-content ui-corner-all']")
            )
        )
        link = contract_tab.find_element_by_partial_link_text('Pay Monthly')
        link.click()

        # Fetch standard rates table
        standard_rates = contract_tab.find_element_by_xpath(
            "div[@id='{}']/div[@id='standardRates']/table[@id='standardRatesTable']".format(plan_name)
        )

        # Find appropriate calling charge
        charge_string = None
        for element in standard_rates.find_elements_by_tag_name('tr'):
            split_text = element.text.split(' ')
            if receiver in split_text:
                charge_string = split_text[-1]
                break

        # Convert string of cost to pence
        if charge_string is not None:
            result = _convert_string_price_to_pence(charge_string)
        else:
            result = None

        # Reset page
        self.driver.get(self.driver.current_url)

        return result


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
def scrape_costs_and_print(driver):
    """
    Uses webdriver to scrape landline calling costs information for Pay Monthly customers from the URL specified in
    'charges_url.txt' for the countries specified in 'countries.txt' and prints result to screen.

    Parameters
    ----------
    driver : webdriver instance
    """

    # Fetch external information
    url, countries = fetch_external_info()

    # Set up page
    page = OTwoPage(driver, url, countries)

    # Attempt to scrape cost information from page
    costs = []
    try:
        for country in countries:
            costs.append(page.get_country_call_price(country))
    except NoSuchElementException as e:
        print('Cannot scrape information from page given by URL.')
    else:
        for country, cost in zip(countries, costs):
            if cost is None:
                print('A cost could not be found for country {}'.format(country))
            else:
                print('The cost to call {} is {} pence per minute.'.format(country, cost))


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
        scrape_costs_and_print(driver)
        driver.close()