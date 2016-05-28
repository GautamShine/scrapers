#!/usr/bin/env python

from wapo import WaPoScraper

#Instantiate scraper class
wapo = WaPoScraper()

# Get urls by crawling
num_urls = 50
min_page = 0
urls = wapo.get_urls(num_urls, min_page)

# Get article headlines and tags
headlines, labels = wapo.get_labels(urls)

# Remove labels that don't occur in headline and any empty label headlines
headlines, labels = wapo.sanitize_labels(headlines, labels)

wapo.format_store(headlines, labels, 'W')
