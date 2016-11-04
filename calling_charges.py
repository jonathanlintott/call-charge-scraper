__author__ = 'Jonathan Lintott'


# Standard library imports
import sys
import json


# Basepage for o2 class to inherit
class BasePage(object):

    def __init__(self, driver, url, countries):
        self.driver = driver
        self.countries = countries

        self.driver.get(url)


# o2 class implements logic specific to o2's calling charge url
class OTwoPage(BasePage):
    pass


# Accepts a webdriver instance and preforms the web scraping
def main(driver):

    # Opens 'charges_url.txt' and gets url as string
    with open('charges_url.txt', 'r') as url_file:
        url = url_file.readline()

    # Opens 'countries.txt' and gets countries as a list of strings
    with open('countries.txt', 'r') as countries_file:
        countries = json.load(countries_file)

    print url
    print countries


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
        driver.close()
