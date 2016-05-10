#!/usr/bin/env python

from scraper import Scraper
from selenium import Chrome

class WaPoScraper(Scraper):
    def __init__:
        pass

    def get_urls(base_url):
        pass

    def get_labels(urls):

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
