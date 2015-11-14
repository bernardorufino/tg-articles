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

    def _process_text(self, text):

        # Unicode to ascii
        text = text.decode('utf-8')
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')

        # Lower case
        text = text.lower()

        # Compact spaces
        text = re.sub('\s+', ' ', text)

        # Time and dates
        text = re.sub('\d+min([^\d]|$)', '<time>\\1', text)
        text = re.sub('\d?\d:\d\d([^\d]|$)', '<time>\\1', text)
        text = re.sub('\d?\dh(?:\d\d)?([^\d]|$)', '<time>\\1', text)
        text = re.sub('\d\d/\d\d(?:/\d\d(?:\d\d)?)?', '<date>', text)

        # Drop specials, only letters, numbers and spaces
        text = re.sub('[^\w\s]', '', text)

        # Numbers and money
        text = re.sub('\d+', '<number>', text)
        text = re.sub('<number>bi\s', '<money> ', text)
        text = re.sub('<number>\sreais', '<money>', text)
        text = re.sub('<number>\sdolares', '<money>', text)
        text = re.sub('\sr\s<number>', ' <money>', text)
        text = re.sub('\su\s<number>', ' <money>', text)

        # Trim
        text.strip()

        return text


