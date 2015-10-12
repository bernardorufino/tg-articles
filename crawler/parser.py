#!/usr/bin/env python

import argparse
import webarticle2text

parser = argparse.ArgumentParser(prog='parser',
                                 description="""Extracts the content of a web page and stores the result""")

# Provided by the .sh entry file, thus not public
parser.add_argument('tag', help="The tag of the subject (Politics, Entertainment, Tourism, ...)")
parser.add_argument('url', help="The url of the web page that you want to parse")
parser.add_argument('-o', '--output', default="parser.out",
                    help="Output file where the json result will be appended, a {...}, will be added to the file. "
                         "Defaults to parser.out")


def main():
    args = parser.parse_args()
    content = webarticle2text.extractFromURL(args.url).strip().replace('"', "'")
    if len(content) < 200:
        return 1
    # Post-process the content
    with open(args.output, 'a') as f:
        f.write('{\n')
        f.write('  "tag": "{}",\n'.format(args.tag.upper()))
        f.write('  "content": "{}",\n'.format(content))
        f.write('},\n')


if __name__ == '__main__':
    exit(main())
