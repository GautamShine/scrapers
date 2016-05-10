#!/usr/bin/env python

from scraper import Scraper
from selenium.webdriver.common.keys import Keys

class WaPoScraper(Scraper):
    """
    Derived class for scraping Washington Post articles
    """
    def __init__(self):
        super(WaPoScraper, self).__init__()
        self.base_url = 'http://www.washingtonpost.com'

    def get_urls(self):
        self.driver.get(self.base_url)
        self.driver.find_element_by_id('search-btn').click()
        self.driver.find_element_by_id('search-field').send_keys('*', Keys.ENTER)
        # get urls
        self.driver.find_element_by_css_selector('.page-link.next').click()

    def get_labels(self, urls):

        # Tag in source
        tag_headline = 'meta'
        tag_labels = 'meta'

        # Attributes of tags for searching
        attrs_headline = {'property': 'og:title'}
        attrs_labels = {'name': 'news_keywords'}

        # Attributes of tags to return
        target_headline = 'content'
        target_labels = 'content'

        # Regex to apply to result
        regex_headline = None
        regex_labels = None

        article_headlines = []
        article_labels = []

        for url in urls:
            headline = scr.parse_url(url, tag_headline, attrs=attrs_headline, target=target_headline, regex=regex_headline)
            labels = scr.parse_url(url, tag_labels, attrs=attrs_labels, target=target_labels, regex=regex_labels)

            article_headlines.append(headline)
            article_labels.append(labels.split(', '))
