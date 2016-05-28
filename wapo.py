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

    def get_urls(self, num_urls, min_page):
        """
        Returns a list of URLs to news articles using search
        """
        urls = []
        # Enter WaPo search
        self.driver.get('http://www.washingtonpost.com')
        self.driver.find_element_by_id('search-btn').click()
        self.driver.find_element_by_id('search-field').send_keys('*', Keys.ENTER)

        page = 0
        while len(urls) < num_urls:
            # Get post-JavaScript
            html = self.driver.execute_script("return document.documentElement.innerHTML;")
            soup = BeautifulSoup(html, 'lxml')
            news_items = soup.find_all('div', class_='pb-feed-item ng-scope')

            # Store news urls
            for i in range(len(news_items)):
                if len(urls) < num_urls and page > min_page:
                    urls.append('http://' + news_items[i]['data-sid'])

            # Advance to next search page
            self.driver.find_element_by_css_selector('.page-link.next').click()
            page += 1

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

    def sanitize_labels(self, headlines, labels):
        """
        Removes human-annotated labels that did not occur in headlines
        """
        assert len(headlines) == len(labels)

        headline_lemmas = self.lemmatize(headlines)
        label_lemmas = self.lemmatize(labels)

        sanitized_labels = []
        for i,headline in enumerate(headline_lemmas):
            intersection = set(headline) & set(label_lemmas[i])
            sanitized_labels.append(intersection)

        return sanitized_labels

    def format_store(self, headlines, labels):
        """
        Write to files in .txt/.key format used by keyword extractors
        """
        headline_files = []
        label_files = []
        for i,headline in enumerate(headlines):
            headline_files.append('data/W_' + str(i) + '.txt')

        for i,tags in enumerate(labels):
            label_files.append('data/W_' + str(i) + '.key')

        self.write(headlines, headline_files)
        self.write(labels, label_files)
