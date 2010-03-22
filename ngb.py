import re

import nltk.tokenize


__version__ = "0.1.0"


class Counter(dict):
    
    def add(self, other):
        for ngram in other.iterkeys():
            self[ngram] = self.get(ngram, 0) + other[ngram]

    def remove_subphrases(self):
        builder = NgramBuilder()
        to_remove = {}
        for phrase in self.keys():
            for length in range(1, len(phrase.split(" "))):
                for subphrase in builder.find_ngrams(phrase, length).keys():
                    if subphrase in self and self[subphrase] == self[phrase]:
                        to_remove[subphrase] = 1
        for subphrase in to_remove.keys():
            del self[subphrase]


class NgramBuilder(object):
    
    def __init__(self, stopwords=None):
        self.stopwords = stopwords
        
    def find_ngrams(self, text, length):
        counter = Counter()
        num_unigrams, unigrams = self.split_into_unigrams(text.lower())
        for i in xrange(num_unigrams):
            if (num_unigrams <= i + length - 1):
                break
            unigram_group = unigrams[i:i + length]
            if not self.ngram_is_filtered(unigram_group):
                ngram = " ".join(unigram_group)
                counter[ngram] = counter.get(ngram, 0) + 1
        return counter
    
    def split_into_unigrams(self, text):
        unigrams = []
        for token in nltk.tokenize.WhitespaceTokenizer().tokenize(text):
            unigram = self.token_to_unigram(token)
            if unigram:
                unigrams.append(unigram)
        return len(unigrams), unigrams
    
    def token_to_unigram(self, token):
        token = token.strip().strip(",.!|&-_()[]<>{}/\"'").strip()

        def has_no_chars(token):
            for char in token:
                if char.isalpha():
                    return False
            return True

        if len(token) == 1 or token.isdigit() or has_no_chars(token):
            return None
        return token

    def ngram_starts_or_ends_in_stopword(self, unigrams):
        if self.stopwords is None:
            return False
        return unigrams[0] in self.stopwords or unigrams[-1] in self.stopwords

    def ngram_is_filtered(self, unigrams):
        return self.ngram_starts_or_ends_in_stopword(unigrams)


stopwords = set([
    "a",
    "all",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "can",
    "do",
    "for",
    "from",
    "had",
    "has",
    "have",
    "he",
    "his",
    "if",
    "in",
    "is",
    "it",
    "its",
    "it's",
    "my",
    "no",
    "not",
    "of",
    "on",
    "or",
    "our",
    "so",
    "that",
    "the",
    "their",
    "these",
    "they",
    "this",
    "to",
    "us",
    "was",
    "we",
    "were",
    "when",
    "where",
    "which",
    "who",
    "with",
    "would",
    "you",
])
