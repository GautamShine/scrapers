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

    def crawl(self, num_urls, min_page, store=False):
        """
        Returns a list of URLs to news articles using search
        Optionally stores the target data while collecting urls
        """
        urls = []
        # Enter WaPo search
        self.driver.get('http://www.washingtonpost.com')
        self.driver.find_element_by_id('search-btn').click()
        self.driver.find_element_by_id('search-field').send_keys('the or to or of or a', Keys.ENTER)

        # Order search results by date
        dropdown = self.driver.find_element_by_class_name('pb-filter-sort')
        dropdown.click()
        dropdown.find_elements_by_tag_name('li')[1].click()
        self.driver.find_elements_by_id('updateResults')[0].click()

        page = 1
        count = 0
        while count < num_urls:
            # Get post-JavaScript
            html = self.driver.execute_script("return document.documentElement.innerHTML;")
            soup = BeautifulSoup(html, 'lxml')
            news_items = soup.find_all('div', class_='pb-feed-item ng-scope')

            # Store news urls
            for i in range(len(news_items)):
                if count < num_urls and page > min_page:
                    urls.append('http://' + news_items[i]['data-sid'])
                    count += 1

            # Store continously while getting urls if desired
            if store:
                orig_headlines, orig_labels = self.get_labels(urls)
                if orig_labels:
                    suffix = list(range(count - len(orig_labels), count))
                    self.format_store(orig_headlines, orig_labels, 'data/orig/', 'O', suffix)

                    # Sanitized data
                    headlines, labels, appears = self.sanitize_labels(orig_headlines, orig_labels)
                    if labels:
                        suffix = [suffix[i] for i in range(len(orig_labels)) if appears[i]]
                        self.format_store(headlines, labels, 'data/', 'W', suffix)
                        urls = []

            # Advance to next search page
            self.driver.find_element_by_css_selector('.page-link.next').click()
            page += 1

        if store:
            return None
        else:
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
        sanitized_headlines = []
        sanitized_labels = []
        lems = lambda x: {w.lemma_ for w in self.nlp(x) if not (w.is_stop or w.is_punct)}

        # boolean vector denoting whether a headline,label pair is included
        appears = [False]*len(labels)

        for i,headline in enumerate(headline_lemmas):
            intersection = set(headline) & set(label_lemmas[i])
            # include only non-empty intersections
            if intersection:
               label_list = []
               # return original tags, not lemmas
               for label in labels[i]:
                   # include a label its lemmas are a subset of the intersection
                   if label and (lems(label) <= intersection):
                       label_list.append(label)
               if label_list:
                   appears[i] = True
                   sanitized_headlines.append(headlines[i])
                   sanitized_labels.append(label_list)

        return sanitized_headlines, sanitized_labels, appears

    def format_store(self, headlines, labels, path, prefix, suffix):
        """
        Write to files in .txt/.key format used by keyword extractors
        """
        assert len(headlines) == len(labels)

        headline_files = []
        label_files = []

        if type(suffix) is not list:
            suffix = [suffix]*len(labels)
        if type(suffix[0]) is not str:
            suffix = [str(x) for x in suffix]

        for i,headline in enumerate(headlines):
            headline_files.append(path + prefix + '_' + suffix[i] + '.txt')
            label_files.append(path + prefix + '_' + suffix[i] + '.key')

        self.write(headlines, headline_files)
        self.write(labels, label_files)
