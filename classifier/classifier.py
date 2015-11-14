import argparse
from collections import defaultdict
import json
import re
import math
import sys
from utils import histogram
from utils import bytefy


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

    def dump(self):
        data = {
            'ntokens_per_tag': sorted(self._ntokens_per_tag),
            'ndocs_per_tag': sorted(self._ndocs_per_tag),
            'ndocs': self._ndocs,
            'vocab': list(sorted(self._vocab)),
            'tags': sorted(self._tags),
            'weights': sorted(self._weights)
        }
        serial_data = json.dumps(data)
        return serial_data

    @classmethod
    def load(cls, serial_data, processor):
        data = json.loads(serial_data)
        data = bytefy(data)
        instance = cls(processor)
        instance._ntokens_per_tag = data['ntokens_per_tag']
        instance._ndocs_per_tag = data['ndocs_per_tag']
        instance._ndocs = data['ndocs']
        instance._vocab = set(data['vocab'])
        instance._tags = data['tags']
        instance._weights = data['weights']
        return instance

    def train(self, data):
        self._processor.process_examples(data)

        articles_per_tag = defaultdict(lambda: [])
        for example in data:
            tag = self.normalize_tag_label(example['tag'])
            if tag in self.IGNORE_TAGS:
                continue
            articles_per_tag[tag].append(example['tokens'])

        self._ntokens_per_tag = {tag: histogram(token for article in articles for token in article)
                                 for tag, articles in articles_per_tag.iteritems()}
        self._ndocs_per_tag = {tag: len(articles) for tag, articles in articles_per_tag.iteritems()}
        self._ndocs = sum(self._ndocs_per_tag.values())
        self._vocab = set(t for tag, tokens in self._ntokens_per_tag.iteritems() for t in tokens.keys())
        self._tags = list(self._ntokens_per_tag.keys())
        self._weights = self._compute_weights()

        for tag, tokens in self._ntokens_per_tag.iteritems():
            total = sum(tokens.values())
            with open('/Users/bernardorufino/pastebin/classifier/{}.dat'.format(tag), 'w') as f:
                for token, n in sorted(tokens.iteritems(), key=lambda (t, n): n, reverse=True):
                    f.write("{:<14} {:<5} {:<5.2f} {:<5.2f}\n".format(token, n, float(n) / total, self._weights[token]))
                f.write('\n')

    def _compute_weights(self):
        weights = {}
        grs = {}

        n_tokens = sum(sum(self._ntokens_per_tag[tag].values()) for tag in self._tags)
        n_tokens_per_tag = {}
        for tag in self._tags:
            n_tokens_per_tag[tag] = sum(self._ntokens_per_tag[tag].values())
        for token in self._vocab:
            N = 0
            n_t = sum(self._ntokens_per_tag[tag][token] for tag in self._tags)
            for tag in self._tags:
                n_tc = self._ntokens_per_tag[tag].get(token, 0)
                n_c_tokens = n_tokens_per_tag[tag]
                p_tc = float(n_tc) / n_tokens
                if n_tc > 0:
                    N += p_tc * math.log(float(n_tc) * n_tokens / n_c_tokens / n_t, 2)
            p_t = float(n_t) / n_tokens
            D = - p_t * math.log(p_t, 2)
            grs[token] = N / D

        gr_avg = sum(grs.values()) / len(grs)
        for token in self._vocab:
            weights[token] = grs[token] / gr_avg

        return weights

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
                w = self._weights.get(token, 0.01)
                logp = w * math.log(float(n + alpha) / (ntokens + alpha * vocab_size))
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



