#!/usr/bin/env python

from wapo import WaPoScraper

#Instantiate scraper class
wapo = WaPoScraper()

# Get urls by crawling
num_urls = 5
min_page = 0
urls = wapo.get_urls(num_urls, min_page)

# Get article headlines and tags
headlines, labels = wapo.get_labels(urls)

sanitized_labels = wapo.sanitize_labels(headlines, labels)

for i in range(len(headlines)):
    print(headlines[i])
    print(labels[i])
    print(sanitized_labels[i])
    print('\n')

wapo.format_store(headlines, labels)


