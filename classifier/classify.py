#!/usr/bin/env python

import argparse
import os

from utils import read_dataset
from text_processor import TextProcessor
from classifier import Classifier


parser = argparse.ArgumentParser(prog='classify',
                                 description="""Classifies an unclassified text""")

parser.add_argument('data', help="The data file in json format")

parser.add_argument('-c', '--classifier', default=os.path.join('out', 'classifier.dat'),
                    help="File where precomputed data for the classifier was put. Defaults to "
                         "out/classifier.dat")


def main():
    args = parser.parse_args()

    with open(args.classifier, 'r') as f:
        serialized_classifier = f.read()

    processor = TextProcessor()
    classifier = Classifier.load(serialized_classifier, processor)

    for example in read_dataset(args.data):
        text = example['content']
        predicted_tag = classifier.classify(text)
        print predicted_tag


if __name__ == '__main__':
    exit(main())
