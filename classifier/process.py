#!/usr/bin/env python
import argparse
import json
import os
import re


parser = argparse.ArgumentParser(prog='process',
                                 description="""Processes the output data from the crawler, tokenizing certain words or
                                                groups of words""")

parser.add_argument('data', help="The data file in json format")
parser.add_argument('-o', '--output', default=None,
                    help="Output file where the processed data will be put. Defaults to <data>.out")


def process_content(content):
    content = re.sub('\d+', '<number>', content)

    # Money: maybe revisit initial processing?
    content = re.sub('\sr\s<number>', ' <money>', content)
    content = re.sub('\su\s<number>', '<money>', content)

    return content


def main():
    args = parser.parse_args()

    with open(args.data, 'r') as f:
        data_text = f.read()

    data_text = data_text.strip(', ' + os.linesep)
    data_text = '[' + data_text + ']'
    data_json = json.loads(data_text)
    for example in data_json:
        example['content'] = process_content(example['content'])

    data_processed = json.dumps(data_json, indent=4)

    output_file = args.output
    if not output_file:
        output_file = '{}.processed'.format(args.data)

    with open(output_file, 'w') as f:
        f.write(data_processed)

    print "{} processed examples on {}".format(len(data_json), output_file)

    return 0


if __name__ == '__main__':
    exit(main())
