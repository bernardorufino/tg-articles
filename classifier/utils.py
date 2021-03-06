from collections import defaultdict
import json
import os


def histogram(lis):
    hist = defaultdict(lambda: 0)
    for item in lis:
        hist[item] += 1
    return hist


def bytefy(input):
    if isinstance(input, dict):
        return {bytefy(key): bytefy(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [bytefy(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def ensure_directory(filepath):
    dirpath = os.path.dirname(filepath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


def read_dataset(data):
    with open(data, 'r') as f:
        data_text = f.read()
    data_text = data_text.strip(', ' + os.linesep)
    data_text = '[' + data_text + ']'
    return json.loads(data_text)
