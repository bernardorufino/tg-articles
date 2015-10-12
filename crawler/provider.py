#!/usr/bin/env python

import providers.googlenews as prov
import sys


def main():
    url = sys.argv[1]
    inputs = prov.read(url)
    for input in inputs:
        print(u'"{}" "{}"'.format(input[0], input[1]))


if __name__ == '__main__':
    exit(main())


