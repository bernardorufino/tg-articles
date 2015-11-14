import argparse
from collections import defaultdict
import json
import re
import math
import sys


class Classifier(object):

    IGNORE_TAGS = ['brasil', 'mundo', 'mais_noticias_principais', 'ultimas_noticias', '=']

    def __init__(self, processor):
        self._processor = processor
        self._ntokens_per_tag = None
        self._ndocs_per_tag = None
        self._ndocs = None
        self._vocab = None
        self._tags = None
        self._weights = {}
        pass

    def train(self, data):
        self._processor.process_examples(data)

        articles_per_tag = defaultdict(lambda: [])
        for example in data:
            tag = self.normalize_tag_label(example['tag'])
            if tag in self.IGNORE_TAGS:
                continue
            articles_per_tag[tag].append(example['tokens'])

        self._ntokens_per_tag = {tag: self._histogram(token for article in articles for token in article)
                                 for tag, articles in articles_per_tag.iteritems()}
        self._ndocs_per_tag = {tag: len(articles) for tag, articles in articles_per_tag.iteritems()}
        self._ndocs = sum(self._ndocs_per_tag.values())
        self._vocab = set(t for tag, tokens in self._ntokens_per_tag.iteritems() for t in tokens.keys())
        self._tags = list(self._ntokens_per_tag.keys())

        for tag, tokens in self._ntokens_per_tag.iteritems():
            total = sum(tokens.values())
            with open('/Users/bernardorufino/pastebin/classifier/{}.dat'.format(tag), 'w') as f:
                for token, n in sorted(tokens.iteritems(), key=lambda (t, n): n, reverse=True):
                    f.write("{:<14} {:<5} {:<5.2f} {:<5.2f}\n".format(token, n, float(n) / total, self._weights[token]))
                f.write('\n')

    def save(self, dir):
        raise NotImplementedError()

    def classify(self, text, alpha=1, verbose=False):
        if verbose:
            print '-- Classifier.classify() --'
        tokens = self._processor.process_text(text)
        vocab_size = len(self._vocab)
        max_tag = (-float('inf'), None)
        for tag in self._tags:
            ntokens = sum(self._ntokens_per_tag[tag].values())
            logp_prior = math.log(float(self._ndocs_per_tag[tag]) / self._ndocs)
            logp_likelihood = 0
            for token in tokens:
                n = self._ntokens_per_tag[tag].get(token, 0)
                logp = math.log(float(n + alpha) / (ntokens + alpha * vocab_size))
                logp_likelihood += logp
            logp_tag = logp_prior + logp_likelihood
            if verbose:
                print 'tag = {}, p = {}, p_prior = {}, p_likelihood = {}'.format(tag, logp_tag, logp_prior, logp_likelihood)
            max_tag = max(max_tag, (logp_tag, tag))
        _, tag = max_tag
        if verbose:
            print
        return tag

    def normalize_tag_label(self, tag):
        return re.sub('\s', '_', tag).lower()

    def _histogram(self, lis):
        hist = defaultdict(lambda: 0)
        for item in lis:
            hist[item] += 1
        return hist

