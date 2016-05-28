#!/usr/bin/env python

from spacy.en import English
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import numpy as np

class Scraper:
    """
    Base class for scraping sites with Selenium and Beautiful Soup
    """
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.nlp = English()

    def lemmatize(self, texts, flatten=False):
        """
        Lemmatizes each word, i.e. lower case and no inflection
        """
        if type(texts) is str:
            text_lemmas = [w.lemma_ for w in self.nlp(text) if not w.is_stop]

        elif type(texts) is list:
            text_lemmas = []
            for text in texts:
                if type(text) is str: 
                    text_lemmas.append([w.lemma_ for w in self.nlp(text) if not w.is_stop])
                elif type(text) is list:
                    text_item_lemmas = []
                    for text_item in text:
                        print(text_item)
                        text_item_lemmas.extend([w.lemma_ for w in self.nlp(text_item) if not w.is_stop])
                    print(text_item_lemmas)
                    text_lemmas.append(text_item_lemmas)
 
                else:
                    raise TypeError('Lemmatize input not a list of lists or strings')

        return text_lemmas

    def parse_url(self, url, tag, attrs=None, target=None, regex=None):
        """
        Retrieves a tag in a url's source, optionally extracting content
        """
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'lxml')
            parse = soup.find(tag, attrs)

            # Optionally extract a target attribute
            if target:
                parse = parse[target]

            # Optionally apply a regex
            if regex:
                parse = re.findall(regex, str(parse))

        except:
            parse = None

        return parse

    def write(self, write_items, write_files):
        """
        Writes a string to file or a list of strings separated by newlines
        """
        files = []
        for f in write_files:
            files.append(open(f, 'w'))

        for i,item in enumerate(write_items):
            if type(item) is list:
                for row in item:
                    files[i].write(row + '\n')
            elif type(item) is str:
                files[i].write(item + '\n')
            else:
                raise TypeError('Write input not a string or list of strings')

        for f in files:
            f.close()
