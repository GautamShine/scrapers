#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import re
import numpy as np

class Scraper:
    """
    Base class for scraping sites with Beautiful Soup and regexes
    """
    def __init__(self):
        pass

    def get_urls(self, base_url):
        urls = None
        return urls

    def parse_url(self, url, tag, attrs=None, target=None, regex=None):
        """
        Applies a regex to a tag in a url's source
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        parse = soup.find(tag, attrs)

        # Optionally extract a target attribute
        if target:
            parse = parse[target]

        # Optionally apply a regex
        if regex:
            parse = re.findall(regex, str(parse))

        return parse

    def store(self, csv, **kwargs):
        pass
