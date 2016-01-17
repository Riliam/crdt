import copy
import string
from datetime import datetime
from collections import defaultdict, Counter
from base import CvRDTBase


class CounterPN(CvRDTBase):

    def reinitialize(self):
        self.pos = [0] * self.replicas_count
        self.neg = [0] * self.replicas_count

    def get_value(self):
        return sum(self.pos) - sum(self.neg)

    def merge(self, other):
        for i in range(self.replicas_count):
            self.pos[i] = max([self.pos[i], other.pos[i]])
            self.neg[i] = max([self.neg[i], other.neg[i]])

    @CvRDTBase.send_state_to_other_replicas
    def inc(self, value=1):
        self.pos[self.id] += value

    @CvRDTBase.send_state_to_other_replicas
    def dec(self, value=1):
        self.neg[self.id] += value


class Set2P(CvRDTBase):

    def __init__(self):
        self.added = set()
        self.removed = set()

    def lookup(self, el):
        return (el in self.added) and (el not in self.removed)

    @CvRDTBase.send_state_to_other_replicas
    def add(self, el):
        self.added.add(el)

    @CvRDTBase.send_state_to_other_replicas
    def remove(self, el):
        if self.lookup(el):
            self.removed.add(el)

    def merge(self, other):
        self.added.update(other.added)
        self.removed.update(other.removed)


class WordCountMap(CvRDTBase):

    def __init__(self):
        self.storage = defaultdict(lambda: defaultdict(lambda: 0))

    @staticmethod
    def _process_text(text):
        punct_to_space_table = {ord(c): ' ' for c in string.punctuation}
        cleaned_text = text.lower().translate(punct_to_space_table)
        words_list = cleaned_text.split()
        return Counter(words_list)

    @CvRDTBase.send_state_to_other_replicas
    def add(self, text):
        frequencies = self._process_text(text)
        for word, count in frequencies.items():
            self.storage[word][self.id] += count

    def get_top(self, count=10):
        top = sorted(self.storage.items(), key=lambda x: -sum(x[1].values()))[:count]
        return [(word, sum(counts.values())) for word, counts in top]

    def merge(self, other):
        target = self.storage
        source = other.storage
        
        # update words data which are in both storages
        for word in target.keys():
            if word in source:
                for i in range(self.replicas_count):
                    target[word][i] = max(target[word][i], source[word][i])

        # copy words data that is in `other.storage` but not in `self.storage`
        for word in source.keys():
            if word not in target:
                target[word] = copy.copy(source[word])
