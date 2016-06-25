#!/usr/bin/env python

from wapo import WaPoScraper

#Instantiate scraper class
chrome_path = '/home/gshine/Documents/Utilities/chromedriver'
wapo = WaPoScraper(chrome_path)

# Get urls by crawling
num_urls = 1e6
min_page = 1

wapo.crawl(num_urls, min_page, store=True)

