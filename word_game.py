import os
import sys
import pickle
import random
from enum import Enum
import matplotlib.pyplot as plt


dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'english_words.pkl'), 'rb') as fr:
    all_words = pickle.load(fr)

with open(os.path.join(dir_path, 'char_frequencies.pkl'), 'rb') as fr:
    global_char_frequencies = pickle.load(fr)

WORD_LENGTH = 5
NUM_TRIALS = 10000
valid_length_count = sum(map(lambda w: len(w) != WORD_LENGTH, all_words))
if valid_length_count > 0:
    print(f'Not all words have expected length {WORD_LENGTH}')
    exit()


class Feedback(Enum):
    INCORRECT = 1,
    WRONG_PLACE = 2,
    CORRECT = 3,
    TOO_MANY_OCCURRENCES = 4


def filter_out_words(words, feedback):
    new_words = list(words)

    for idx in feedback:
        guessed_char, feedback_response, num_occurrences = None, None, None

        if feedback[idx][1] == Feedback.TOO_MANY_OCCURRENCES:
            guessed_char, feedback_response, num_occurrences = feedback[idx]
        else:
            guessed_char, feedback_response = feedback[idx]

        if feedback_response == Feedback.CORRECT:
            new_words = [word for word in new_words if word[idx] == guessed_char]
        elif feedback_response == Feedback.WRONG_PLACE:
            new_words = [word for word in new_words if word[idx] != guessed_char and guessed_char in word]
        elif feedback_response == Feedback.INCORRECT:
            new_words = [word for word in new_words if guessed_char not in word]
        elif feedback_response == Feedback.TOO_MANY_OCCURRENCES:
            new_words = [word for word in new_words if word[idx] != guessed_char and word.count(guessed_char) == num_occurrences]

    return new_words


def guess_next_word(remaining_words, strategy, verbose=True):

    if verbose:
        print(f'Using strategy: {strategy}')

    if strategy == 'random':
        guess = random.choice(remaining_words)
        if verbose:
            print(f'Random Guess: {guess}')
        return guess

    elif strategy == 'high_frequency_global':
        best_guess, max_freq = None, 0

        for word in remaining_words:
            char_dict = {}
            freq_sum = 0
            for char in word:
                if char not in char_dict:
                    char_dict[char] = True
                    freq_sum += global_char_frequencies[char]

            if freq_sum > max_freq:
                max_freq = freq_sum
                best_guess = word

        if verbose:
            print(f'Best Guess: {best_guess} (Frequency: {max_freq})')

        return best_guess

    elif strategy == 'high_frequency_remaining':
        best_guess, max_freq = None, 0

        char_freq = {}
        for word in remaining_words:
            for char in word:
                if char in char_freq:
                    char_freq[char] += 1
                else:
                    char_freq[char] = 1

        for word in remaining_words:
            char_dict = {}
            freq_sum = 0
            for char in word:
                if char not in char_dict:
                    char_dict[char] = True
                    freq_sum += char_freq[char]

            if freq_sum > max_freq:
                max_freq = freq_sum
                best_guess = word

        if verbose:
            print(f'Best Guess: {best_guess} (Frequency: {max_freq})')

        return best_guess



    elif strategy == 'low_frequency':
        best_guess, min_freq = None, sys.maxsize

        for word in remaining_words:
            char_dict = {}
            freq_sum = 0
            for char in word:
                if char not in char_dict:
                    char_dict[char] = True
                    freq_sum += global_char_frequencies[char]

            if freq_sum < min_freq:
                min_freq = freq_sum
                best_guess = word

        if verbose:
            print(f'Best Guess: {best_guess} (Frequency: {min_freq})')

        return best_guess

    elif strategy == 'most_vowels':
        vowels = ['a', 'e', 'i', 'o', 'u']
        best_guess, max_vowels = None, 0

        for word in remaining_words:
            word_vowels = [char for char in word if char in vowels]
            num_vowels = len(set(word_vowels))

            if num_vowels > max_vowels:
                max_vowels = num_vowels
                best_guess = word

        if verbose:
            print(f'Best Guess: {best_guess} (Number of Vowels: {max_vowels})')

        return best_guess

    else:
        print(f'Strategy {strategy} not implemented')
        return None


def get_feedback(guess, target_word):
    feedback = {}
    occurrences = {char: 0 for char in guess}

    for i, (guess_char, target_char) in enumerate(zip(guess, target_word)):
        if guess_char != target_char:
            if guess_char in target_word:
                occurrences[guess_char] += 1
                if occurrences[guess_char] <= target_word.count(guess_char):
                    feedback[i] = (guess_char, Feedback.WRONG_PLACE)
                else:
                    feedback[i] = (guess_char, Feedback.TOO_MANY_OCCURRENCES, target_word.count(guess_char))
            else:
                feedback[i] = (guess_char, Feedback.INCORRECT)
        else:
            feedback[i] = (guess_char, Feedback.CORRECT)

    return feedback


def word_game(vocab, verbose=True, word_length=5, target=None,
              initial=None, strategy='random', initial_strategy='random'):

    if target is not None:
        if len(target) != word_length:
            print(f'Target word {target} does not have expect word length {word_length}')
            return None
        if target not in vocab:
            print(f'Target word {target} is not in vocabulary.')
            return None

    if initial is not None:
        if len(initial) != word_length:
            print(f'Initial guess {initial} does not have expect word length {word_length}')
            return None
        if initial not in vocab:
            print(f'Initial guess {initial} is not in vocabulary.')
            return None

    random.shuffle(vocab)
    target_word = target if target else random.choice(vocab)
    remaining_words = list(vocab)

    if verbose:
        print(f'Target Word: {target_word}')

    # Initial Guess
    if initial:
        guess = initial
    else:
        guess = guess_next_word(remaining_words, initial_strategy, verbose=verbose)

    if verbose:
        print(f'Initial Guess: {guess}\n')

    num_guesses = 1

    while guess != target_word:

        if verbose:
            print(f'INCORRECT Guess: {guess}')

        prev_num_remaining_words = len(remaining_words)
        remaining_words.remove(guess)

        feedback = get_feedback(guess, target_word)
        remaining_words = filter_out_words(remaining_words, feedback)

        if verbose:
            print(f'Removing {prev_num_remaining_words - len(remaining_words)} potential word(s)...')
            print(f'Possible Word(s): {remaining_words}')

        guess = guess_next_word(remaining_words, strategy, verbose=verbose)
        num_guesses += 1
        if verbose:
            print(f'Guess #{num_guesses}: {guess}\n')

    if verbose:
        print(f'CORRECT Guess: {guess}')
        print(f'Required {num_guesses} guesses')
    return num_guesses


def main():
    # word_game(all_words, word_length=WORD_LENGTH, initial_strategy='random', strategy='high_frequency_remaining')
    guesses_dist = [word_game(all_words, word_length=WORD_LENGTH,
                              initial_strategy='most_vowels', strategy='high_frequency_global', verbose=False)
                    for _ in range(NUM_TRIALS)]
    print(sum(guesses_dist) / NUM_TRIALS)


if __name__ == '__main__':
    main()








