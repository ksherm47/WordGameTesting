import os
import pickle
import random
from enum import Enum
import matplotlib.pyplot as plt

# How english_words was created
# from itertools import product
# import enchant
#
#
# dictionary = enchant.Dict('en_US')
#
# chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
#          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
#
# five_strings = [''.join(p) for p in list(product(chars, repeat=5))]
#
# english_words = [string for string in five_strings if dictionary.check(string)]
#
# print(len(english_words))
# [print(w) for w in english_words]
#
# with open('H:\\python scripts\\word_game\\english_words.pkl', 'wb') as fw:
#     pickle.dump(english_words, fw)


class Feedback(Enum):
    INCORRECT = 1,
    WRONG_PLACE = 2,
    CORRECT = 3,
    TOO_MANY_OCCURRENCES = 4


def filter_out_words(words, feedback):

    for idx in feedback:
        guessed_char, feedback_response, num_occurrences = None, None, None

        if feedback[idx][1] == Feedback.TOO_MANY_OCCURRENCES:
            guessed_char, feedback_response, num_occurrences = feedback[idx]
        else:
            guessed_char, feedback_response = feedback[idx]

        if feedback_response == Feedback.CORRECT:
            words = [word for word in words if word[idx] == guessed_char]
        elif feedback_response == Feedback.WRONG_PLACE:
            words = [word for word in words if word[idx] != guessed_char and guessed_char in word]
        elif feedback_response == Feedback.INCORRECT:
            words = [word for word in words if guessed_char not in word]
        elif feedback_response == Feedback.TOO_MANY_OCCURRENCES:
            words = [word for word in words if word.count(guessed_char) == num_occurrences]

    return words


def word_game(vocab, verbose=True, word_length=5, target=None, initial=None):

    random.shuffle(vocab)
    target_word = target if target else random.choice(vocab)

    remaining_words = list(vocab)
    guess = initial if initial else random.choice(remaining_words)
    num_guesses = 1

    if verbose:
        print(f'Target Word: {target_word}')
        print(f'Initial Guess: {guess}\n')

    while guess != target_word:
        if verbose:
            print(f'INCORRECT Guess: {guess}')

        prev_num_remaining_words = len(remaining_words)
        remaining_words.remove(guess)

        feedback = dict.fromkeys(list(range(word_length)))
        wrong_place_occurrences = {char: 0 for char in guess}

        for i, (guess_char, target_char) in enumerate(zip(guess, target_word)):
            if guess_char != target_char:
                if guess_char in target_word:
                    wrong_place_occurrences[guess_char] += 1
                    if wrong_place_occurrences[guess_char] <= target_word.count(guess_char):
                        feedback[i] = (guess_char, Feedback.WRONG_PLACE)
                    else:
                        feedback[i] = (guess_char, Feedback.TOO_MANY_OCCURRENCES, target_word.count(guess_char))
                else:
                    feedback[i] = (guess_char, Feedback.INCORRECT)




                # feedback[i] = (guess_char, Feedback.WRONG_PLACE) \
                #     if guess_char in target_word else (guess_char, Feedback.INCORRECT)
            else:
                feedback[i] = (guess_char, Feedback.CORRECT)

        remaining_words = filter_out_words(remaining_words, feedback)
        new_num_remaining_words = len(remaining_words)

        if verbose:
            print(f'Removing {prev_num_remaining_words - new_num_remaining_words} potential words...')
            print(f'Possible Words: {remaining_words}')
        guess = random.choice(remaining_words)
        num_guesses += 1
        if verbose:
            print(f'Guess #{num_guesses}: {guess}\n')

    if verbose:
        print(f'CORRECT Guess: {guess}')
        print(f'Required {num_guesses} guesses')
    return num_guesses


dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'english_words.pkl'), 'rb') as fr:
    all_words = pickle.load(fr)

WORD_LENGTH = 5
NUM_TRIALS = 10000
valid_length_count = sum(map(lambda w: len(w) != WORD_LENGTH, all_words))
if valid_length_count > 0:
    print(f'Not all words have expected length {WORD_LENGTH}')
    exit()

# word_game(all_words, word_length=WORD_LENGTH, target='chase')
guesses_dist = [word_game(all_words, word_length=WORD_LENGTH, verbose=False, target='chase') for _ in range(NUM_TRIALS)]
print(sum(guesses_dist) / NUM_TRIALS)
# plt.hist(guesses_dist, bins=30)
# plt.show()








