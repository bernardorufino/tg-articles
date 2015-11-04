#!/usr/bin/env python
import argparse
import json
import os
import math
import parameters

parser = argparse.ArgumentParser(prog='classify',
                                 description="""Classifies an unclassified text""")

parser.add_argument('parameters', help="Directory where train.py has written its output to.")
parser.add_argument('data', help="The data file in json format without tags. If the json file has tags, they will be "
                                 "ignored")


class Classifier(object):
    def __init__(self, vocab, tags, ndocs_per_tag, words_per_tag):
        self.vocab = vocab
        self.tags = tags
        self.ndocs_per_tag = ndocs_per_tag
        self.ndocs = reduce(lambda a, b: a + b, self.ndocs_per_tag.values())
        self.words_per_tag = words_per_tag
        self.nwords_per_tag = {}
        for tag, words in words_per_tag.iteritems():
            self.nwords_per_tag[tag] = reduce(lambda a, b: a + b, words.values())

    def classify(self, text):
        # print '--'
        words = text.split()
        max_tag = (-float('inf'), None)
        for tag in self.tags:
            logp_prior = math.log(float(self.ndocs_per_tag[tag]) / self.ndocs)
            logp_likelihood = 0
            for word in words:
                n = self.words_per_tag[tag][word] if word in self.words_per_tag[tag] else 0
                logp = math.log(float(n + 1) / self.nwords_per_tag[tag])
                logp_likelihood += logp
                # print 'p_likelihood = {}, p = {}'.format(p_likelihood, p)
            logp_tag = logp_prior + logp_likelihood
            # print 'tag = {}, p = {}, p_prior = {}, p_likelihood = {}'.format(tag, logp_tag, logp_prior, logp_likelihood)
            max_tag = max(max_tag, (logp_tag, tag))
        logp_tag, tag = max_tag
        # print ''
        return tag


def main():
    args = parser.parse_args()

    with open(os.path.join(args.parameters, parameters.VOCAB_FILE), 'r') as f:
        vocab = [line.rstrip() for line in f]  # sorted

    # {tag => number_of_documents}
    ndocs_per_tag = {}
    with open(os.path.join(args.parameters, parameters.PRIORS_FILE), 'r') as f:

        for line in f:
            n, tag = line.rstrip().split(' ', 1)
            ndocs_per_tag[tag] = int(n)


    # {tag => {word => occurrences}}
    words_per_tag = {}
    tags = []
    for filename in os.listdir(args.parameters):
        filepath = os.path.join(args.parameters, filename)
        if not os.path.isfile(filepath) or filename in [parameters.VOCAB_FILE, parameters.PRIORS_FILE]:
            continue
        tag = filename.split('.')[0]
        tags.append(tag)
        with open(filepath, 'r') as f:
            words_per_tag[tag] = {}
            for line in f:
                if not line.strip():
                    continue

                n, word = line.rstrip().split(' ', 1)
                words_per_tag[tag][word] = int(n)

    classifier = Classifier(vocab, tags, ndocs_per_tag, words_per_tag)

    with open(args.data, 'r') as f:
        data_serial = f.read()

    data_json = json.loads(data_serial)

    for example in data_json:
        content = example['content']
        predicted_tag = classifier.classify(content)
        print predicted_tag


if __name__ == '__main__':
    exit(main())
