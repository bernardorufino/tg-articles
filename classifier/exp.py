#!/usr/bin/env python

import argparse
import json
import sys
from text_processor import TextProcessor
from classifier import Classifier
import os
import random


parser = argparse.ArgumentParser(prog='classify',
                                 description="""Classifies an unclassified text""")

parser.add_argument('data', help="The data file in json format")


def read_data(data):
    with open(data, 'r') as f:
        data_text = f.read()
    data_text = data_text.strip(', ' + os.linesep)
    data_text = '[' + data_text + ']'
    return json.loads(data_text)


def main():
    args = parser.parse_args()
    data_json = read_data(args.data)
    random.shuffle(data_json)

    training_set_ratio = 0.7
    training_set_size = int(training_set_ratio * len(data_json) + 0.5)

    training_set = data_json[:training_set_size]
    test_set = data_json[training_set_size:]

    processor = TextProcessor()
    classifier = Classifier(processor)
    classifier.train(training_set)

    # for w in sorted(classifier._vocab):
    #      print w

    corrects = 0
    total = 0
    for example in test_set:
        text = example['content']
        predicted_tag = classifier.classify(text)
        expected_tag = classifier.normalize_tag_label(example['tag'])
        if expected_tag in Classifier.IGNORE_TAGS:
            continue
        if predicted_tag == expected_tag:
            corrects += 1
        else:
            #print 'expected = {}, predicted = {}'.format(expected_tag, predicted_tag)
            pass
        total += 1

    #print '{} {}'.format(len(data_json), float(corrects) / total)


if __name__ == '__main__':
    exit(main())
