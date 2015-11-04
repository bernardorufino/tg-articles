#!/usr/bin/env python

import argparse
from collections import defaultdict
import json
import os
import re
import parameters


parser = argparse.ArgumentParser(prog='train',
                                 description="""Trains the classifier from json data formatted by parser/process.""")

parser.add_argument('data', help="The data file in json format")
parser.add_argument('-o', '--output', default=None,
                    help="Output directory where precomputed data for the classifier will be put. Defaults to "
                         "'classifier' subdirectory to the directory of <data> argument. Directory is created if not "
                         "existent")


def count(lis):
    card = defaultdict(lambda: 0)
    for item in lis:
        card[item] += 1
    return card


def main():
    args = parser.parse_args()

    with open(args.data, 'r') as f:
        data_serial = f.read()

    data_json = json.loads(data_serial)

    # tag => concatenated articles
    tagged_corpus_by_articles = defaultdict(lambda: [])

    for example in data_json:
        tag = re.sub('\s', '_', example['tag']).lower()
        tagged_corpus_by_articles[tag].append(example['content'])

    tagged_corpus = {tag: count(' '.join(articles).split()) for tag, articles in tagged_corpus_by_articles.iteritems()}

    if not args.output:
        args.output = os.path.join(os.path.dirname(args.data), 'classifier')

    if not os.path.isdir(args.output):
        os.makedirs(args.output)

    vocab = set()

    for tag, card in tagged_corpus.iteritems():
        filepath = os.path.join(args.output, tag)
        vocab |= set(card.keys())
        with open(filepath, 'w+') as f:
            for w, c in sorted(card.iteritems(), key=lambda (w, c): c, reverse=True):
                print >> f, "{} {}".format(c, w)
            print >> f

    with open(os.path.join(args.output, parameters.PRIORS_FILE), 'w+') as f:
        for tag, articles in tagged_corpus_by_articles.iteritems():
            print >> f, "{} {}".format(len(articles), tag)

    with open(os.path.join(args.output, parameters.VOCAB_FILE), 'w+') as f:
        for w in sorted(vocab):
            print >> f, w


if __name__ == '__main__':
    exit(main())
