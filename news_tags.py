#!/usr/bin/env python

from wapo import WaPoScraper

#Instantiate scraper class
wapo = WaPoScraper()

# Get urls by crawling
urls = wapo.get_urls(100)

# Get article headlines and tags
articles, labels = wapo.get_labels(urls)

for i in range(len(articles)):
    print(articles[i])
    print(labels[i])
    print('\n')
