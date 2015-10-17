#!/usr/bin/env python

import argparse
import re
import webarticle2text
from datetime import datetime
import os

parser = argparse.ArgumentParser(prog='parser',
                                 description="""Extracts the content of a web page and stores the result""")

# Provided by the .sh entry file, thus not public
parser.add_argument('tag', help="The tag of the subject (Politics, Entertainment, Tourism, ...)")
parser.add_argument('url', help="The url of the web page that you want to parse")
parser.add_argument('-o', '--output', default="out/data.json",
                    help="Output file where the json result will be appended, a {...}, will be added to the file. "
                         "Defaults to data.json")
parser.add_argument('-i', '--index', default="out/data.idx",
                    help="File that will contain a index with the urls already crawled to avoid redundancies. "
                         "Defaults to data.idx")
parser.add_argument('-l', '--log', default="log/{}.log".format(datetime.now().strftime('%Y%m%d_%H%M%S')),
                    help="The name of the file that will receive log entries. Defaults to log/YYYYmmdd_HHMMSS.log")


def log(filepath, entry):
    ensure_directory(filepath)
    with open(filepath, 'a') as f:
        f.write('[{}] '.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')))
        f.write(entry)
        f.write(os.linesep)


def ensure_directory(filepath):
    dirpath = os.path.dirname(filepath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


def main():
    args = parser.parse_args()

    if os.path.isfile(args.index):
        with open(args.index, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            lines = [line for line in lines if line]
    else:
        lines = []

    if args.url in lines:
        print "EXISTENT"
        return 0

    try:
        content = webarticle2text.extractFromURL(args.url).strip().replace('"', "'")
    except Exception as e:
        log(args.log, args.url + ": Exception " + str(e.__class__))
        log(args.log, e.message)
        print "FAIL"
        return 1

    if len(content) < 200:
        log(args.log, args.url + ": Invalid content")
        print "FAIL"
        return 2

    try:
        m = re.match('(?:https?://)?(?:www\.)?(.+?)\..*$', args.url)
        source = m.groups()[0]
        # Post-process the content
        with open(args.output, 'a') as f:
            f.write('{' + os.linesep)
            f.write('  "tag": "{}",'.format(args.tag.upper()) + os.linesep)
            f.write('  "content": "{}",'.format(content) + os.linesep)
            f.write('  "source": "{}",'.format(source) + os.linesep)
            f.write('  "url": "{}"'.format(args.url) + os.linesep)
            f.write('},' + os.linesep)
        log(args.log, args.url + ": Data written")

        ensure_directory(args.index)
        with open(args.index, 'a+') as f:
            f.write(args.url + os.linesep)

        print "SUCCESS"
        return 0

    except Exception as e:
        log(args.log, args.url + ": Can't write file due to Exception " + str(e.__class__))
        log(args.log, args.url + ": " + e.message)
        print "FAIL"
        return 1


if __name__ == '__main__':
    code = main()
    exit(code)
