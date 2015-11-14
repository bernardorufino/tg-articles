#!/usr/bin/env python

import argparse
import os

from utils import read_dataset, ensure_directory
from text_processor import TextProcessor
from classifier import Classifier


parser = argparse.ArgumentParser(prog='classify',
                                 description="""Classifies an unclassified text""")

parser.add_argument('data', help="The data file in json format")

parser.add_argument('-o', '--output', default=os.path.join(os.path.dirname(__file__), 'out', 'classifier.dat'),
                    help="Output file where precomputed data for the classifier will be put. Defaults to "
                         "out/classifier.dat")


def main():
    args = parser.parse_args()
    data_json = read_dataset(args.data)

    processor = TextProcessor()
    classifier = Classifier(processor)
    classifier.train(data_json)

    serialized_classifier = classifier.dump()

    ensure_directory(args.output)
    with open(args.output, 'w') as f:
        f.write(serialized_classifier)
        f.write(os.linesep)


if __name__ == '__main__':
    exit(main())
