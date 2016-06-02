#!/usr/bin/env python

from wapo import WaPoScraper

#Instantiate scraper class
wapo = WaPoScraper()

# Get urls by crawling
num_urls = 1000
min_page = 1

wapo.crawl(num_urls, min_page, store=True)

