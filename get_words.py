import os
import pickle
from itertools import product
import enchant


dictionary = enchant.Dict('en_US')

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

five_strings = [''.join(p) for p in list(product(chars, repeat=5))]

english_words = [string for string in five_strings if dictionary.check(string)]

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'english_words.pkl', 'wb')) as fw:
    pickle.dump(english_words, fw)
