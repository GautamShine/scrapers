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

    def write(self, write_items, write_files):
        """
        Expects a list of lists of lists (respectively: files, rows, items in row)
        """
        files = []
        for f in write_files:
            files.append(open(f, 'w'))

        for i,item in enumerate(write_items):
            if type(item) is list:
                for row in item:
                    files[i].write(row + '\n')
            elif type(item) is str:
                files[i].write(item + '\n')
            else:
                pass

        for f in files:
            f.close()
