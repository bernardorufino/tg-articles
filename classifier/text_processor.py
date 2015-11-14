from collections import defaultdict
import re
import unicodedata
import nltk


UNWANTED_WORDS = set([
    'a', 'em', 'de', 'a', 'o', 'as', 'os', 'um', 'uns', 'e', 'do', 'da'
])


class TextProcessor(object):

    def __init__(self):
        self._stemmer = nltk.stem.RSLPStemmer()

    def process_text(self, text):
        return text.split()

    def process_examples(self, examples):
        self._vocab = set()
        for example in examples:
            example['tokens'] = self.process_text(example['content'])
            for token in example['tokens']:
                self._vocab.add(token)
