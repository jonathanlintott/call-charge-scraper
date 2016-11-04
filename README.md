# call-charge-scraper
Scrapes a web page for the cost of calling a landline for select countries for a specific o2 website.

Run from directory with calling_charges.py. Firefox webdriver by default.

>> python calling_charges.py

Optional argument allowed to set specific firefox binary. For example:

>> python calling_charges.py "/usr/dave/local/Mozilla Firefox/firefox.exe"

To use different webdriver, please set up your own webdriver and import 'scrape_costs_and_print' from the package.
