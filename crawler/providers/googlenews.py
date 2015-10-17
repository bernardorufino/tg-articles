from pyquery import PyQuery as pq
import unicodedata
import re


def read(url):
    inputs = []
    d = pq(url=url)
    for section in d(".section"):
        section_d = pq(section)
        name = section_d(".section-header").text()
        name = re.sub("\s+", " ", name, flags=re.UNICODE)
        name = re.sub("[^\w\s]", "", name, flags=re.UNICODE)
        name = name.strip()
        # TODO: Remove and handle unicode properly
        # TODO: Problem with stdout pipe or file
        if isinstance(name, unicode):
            name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore')
        for article in section_d(".esc-lead-article-title a"):
            url = article.get("href")
            inputs.append((name, url))
    return inputs

