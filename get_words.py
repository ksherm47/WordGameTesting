import os
import pickle
from itertools import product
from enum import Enum


class Dictionary(Enum):
    ENCHANT = 0
    NLTK = 1


WORD_LENGTH = 5
DICTIONARY_TO_USE = Dictionary.NLTK

if DICTIONARY_TO_USE == Dictionary.ENCHANT:
    import enchant

    dictionary = enchant.Dict('en_US')

    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    strings = [''.join(p) for p in list(product(chars, repeat=WORD_LENGTH))]

    english_words = [string for string in strings if dictionary.check(string)]

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'english_words.pkl'), 'wb') as fw:
        pickle.dump(english_words, fw)

elif DICTIONARY_TO_USE == Dictionary.NLTK:
    from nltk.corpus import words

    # chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    #          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    #
    # strings = [''.join(p) for p in list(product(chars, repeat=WORD_LENGTH))]

    english_words = [word for word in set(words.words()) if len(word) == WORD_LENGTH]
    print(len(english_words))
    print(english_words[:20])

