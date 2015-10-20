#!/usr/bin/env python
import argparse
import json

parser = argparse.ArgumentParser(prog='process',
                                 description="""Processes the output data from the crawler, tokenizing certain words or
                                                groups of words""")

parser.add_argument('data', help="The data file in json format")


def main():
    args = parser.parse_args()

    with open(args.data, 'r') as f:
        data_text = f.read()

    print data_text
    data_json = json.loads('[' + data_text + ']')
    print data_json


if __name__ == '__main__':
    exit(main())
