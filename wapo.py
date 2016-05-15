#!/usr/bin/env python

from bs4 import BeautifulSoup
from scraper import Scraper
from selenium.webdriver.common.keys import Keys

class WaPoScraper(Scraper):
    """
    Derived class for scraping Washington Post articles
    """
    def __init__(self):
        super(WaPoScraper, self).__init__()
        self.base_url = 'http://www.washingtonpost.com'

    def get_urls(self, num_urls):
        """
        Returns a list of URLs to news articles using search
        """
        urls = []
        # Enter WaPo search
        self.driver.get(self.base_url)
        self.driver.find_element_by_id('search-btn').click()
        self.driver.find_element_by_id('search-field').send_keys('*', Keys.ENTER)

        while len(urls) < num_urls:
            # Get post-JavaScript
            html = self.driver.execute_script("return document.documentElement.innerHTML;")
            soup = BeautifulSoup(html, 'lxml')
            news_items = soup.find_all('div', class_='pb-feed-item ng-scope')

            # Store news urls
            for i in range(len(news_items)):
                if len(urls) < num_urls:
                    urls.append('http://' + news_items[i]['data-sid'])

            # Advance to next search page
            self.driver.find_element_by_css_selector('.page-link.next').click()

        return urls

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
            headline = self.parse_url(url, tag_headline, attrs=attrs_headline, target=target_headline, regex=regex_headline)
            labels = self.parse_url(url, tag_labels, attrs=attrs_labels, target=target_labels, regex=regex_labels)

            # Check that both were successfully retrieved and append
            if headline and labels:
                article_headlines.append(headline)
                article_labels.append(labels.split(', '))

        return article_headlines, article_labels
