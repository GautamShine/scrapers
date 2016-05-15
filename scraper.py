#!/usr/bin/env python

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import numpy as np

class Scraper:
    """
    Base class for scraping sites with Selenium and Beautiful Soup
    """
    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse_url(self, url, tag, attrs=None, target=None, regex=None):
        """
        Retrieves a tag in a url's source, optionally extracting content
        """
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'lxml')
            parse = soup.find(tag, attrs)

            # Optionally extract a target attribute
            if target:
                parse = parse[target]

            # Optionally apply a regex
            if regex:
                parse = re.findall(regex, str(parse))

        except:
            parse = None

        return parse

    def store(self, csv, **kwargs):
        pass
