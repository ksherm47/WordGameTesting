import os
import pickle

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'english_words.pkl'), 'rb') as fr:
    all_words = pickle.load(fr)

char_frequencies = {char: 0 for char in chars}

for word in all_words:
    for char in word:
        char_frequencies[char] += 1

print(char_frequencies)

with open(os.path.join(dir_path, 'char_frequencies.pkl'), 'wb') as fw:
    pickle.dump(char_frequencies, fw)
