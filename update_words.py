import os
import pickle

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'english_words.txt'), 'r') as fr:
    words_from_txt = fr.read().split('\n')

os.remove(os.path.join(dir_path, 'english_words.pkl'))
with open(os.path.join(dir_path, 'english_words.pkl'), 'wb') as fw:
    pickle.dump(words_from_txt, fw)
