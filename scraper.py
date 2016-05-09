#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import re
import numpy as np

class Scraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_urls(self):
        urls = None
        return urls

    def parse_src(self, url, tag, regex):
        """
        Applies a regex to a tag in a url's source
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        parse = soup.find_all(class_=tag)
        target = re.findall(regex, str(parse))

        return target

    def store(self, csv, **kwargs):
        pass
